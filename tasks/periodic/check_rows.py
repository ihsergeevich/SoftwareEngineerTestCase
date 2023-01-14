import asyncio
import logging
from logging.config import dictConfig

from config import Config
from core.rabbit_mq import publish_message

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class CheckRows:
    """
    Takes next batch of 20 000 rows from bars_2. For each row
    among these pulled 20 000 rows
    """
    __slots__ = 'app', 'limit', 'worker_name'

    def __init__(self, app):
        self.app = app
        self.limit = 20000
        self.worker_name = 'CheckRows'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start __process/__delete_rows_from_bars_2 funcs
        :param payload:
        :return:
        """

        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__process(cursor)
            await self.__delete_rows_from_bars_2(cursor)
        logger.info(f"Finish: {self.worker_name}")

    async def __process(self, cursor) -> None:
        """
        Get all symbols from bars_1 table
        Get all symbols from bars_2 table
        Publish message for CheckRowHelper to RabbitMQ
        If now rows in bars_2 table -> publish
        error_log message to RabbiMQ
        :param cursor:
        :return:
        """
        bars_1_symbols_date = await self.__get_all_symbols_from_bars_1(cursor)
        if rows := await self.__get_rows_from_bars_2(cursor):
            tasks = []
            _loop = asyncio.get_event_loop()
            for row in rows:
                tasks.append(_loop.create_task(publish_message(connection=self.app['mq'],
                                                               message={
                                                                   'date': row['date'],
                                                                   'symbol': row['symbol'],
                                                                   'adjclose': row['adjclose'],
                                                                   'close': row['close'],
                                                                   'high': row['high'],
                                                                   'low': row['low'],
                                                                   'open': row['open'],
                                                                   'volume': row['volume'],
                                                                   'bars_1_symbols_date': bars_1_symbols_date},
                                                               routing_key='test_case.events.check_rows_helper',
                                                               exchange_name='test_case.events',
                                                               queue_name='test_case.events.check_rows_helper'
                                                               )))
                if len(tasks) == 1500:
                    await asyncio.gather(*tasks)
                    tasks = []

        else:
            message = {
                'message': "No values available in bars_2"
            }
            await publish_message(connection=self.app['mq'],
                                  message=message,
                                  routing_key='test_case.events.insert_to_error_logs',
                                  exchange_name='test_case.events',
                                  queue_name='test_case.events.insert_to_error_logs'
                                  )

    @staticmethod
    async def __get_all_symbols_from_bars_1(cursor):
        sql = """
            select
                symbol,
                "date"
            from 
                bars_1
            """

        return [[x['symbol'], x['date']] for x in await cursor.fetch(sql)]

    async def __get_rows_from_bars_2(self, cursor):
        sql = f"""
            select 
                *
            from 
                bars_2
            limit 
                {self.limit} 
            """

        return await cursor.fetch(sql)

    async def __delete_rows_from_bars_2(self, cursor):
        sql = f"""
            with rows AS (
              select
                symbol,
                "date"
              from
                bars_2 b
              limit {self.limit}
            )
            delete from bars_2 b2 
            where (symbol, "date") in (select symbol, "date" from rows)
            """

        await cursor.execute(sql)
