import datetime
import logging
from logging.config import dictConfig

from config import Config
from core.rabbit_mq import publish_message

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class CheckRowsHelper:
    """

    """
    __slots__ = "app", 'worker_name'

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CheckRowsHelper'

    async def run(self, payload: dict) -> None:
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__check_row(payload['date'], payload['symbol'], payload['adjclose'], payload['close'],
                                   payload['high'], payload['low'], payload['open'], payload['volume'],
                                   payload['bars_1_symbols_date'], cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __get_last_10_close(cursor, symbol: str, date: datetime.datetime) -> None:
        sql = f"""
                  select
                      min(close)
                  from 
                      bars_1
                  where
                      bars_1.symbol = '{symbol}' and  bars_1."date" < '{date}' 
                  limit 
                      10
                  """
        return await cursor.fetchval(sql)

    async def __check_row(self, date: datetime.datetime, symbol: str, adjclose: float, close: float, high: float,
                          low: float, open: float, volume: float, bars_1_symbols_date: list, cursor) -> None:
        """
        Check row for:
            1.If record's <SYMBOL> is not present in bars_1 → put error message to error_log table with
            2.Record's <CLOSE> is bigger than Minimum of <SYMBOL> Close prices over last 10 days for a <SYMBOL>
            from bars_1 -> append the record to bars_1, else put error message to error_log table
            3.
            4.
        :param date:
        :param symbol:
        :param adjclose:
        :param close:
        :param high:
        :param low:
        :param open:
        :param volume:
        :param bars_1_symbols_date: list of sets with symbols & date from bars_1 table
        :param cursor:
        :return:
        """
        message = None
        if not [str(symbol), str(date)] in bars_1_symbols_date:
            message = {
                'date': date,
                'symbol': symbol,
                'message': f"{symbol} not present in tables_bars_1 on {date}"
            }

        elif min_close := await self.__get_last_10_close(cursor, symbol, date):
            if close and min_close < close:
                logger.info(f"Send to insert_to_bars_1")
                await publish_message(connection=self.app['mq'],
                                      message={'date': date, 'symbol': symbol, 'adjclose': adjclose, 'close': close,
                                               'high': high, 'low': low, 'open': open, 'volume': volume},
                                      routing_key='test_case.events.insert_to_bars_1',
                                      exchange_name='test_case.events',
                                      queue_name='test_case.events.insert_to_bars_1'
                                      )
            else:
                message = {
                    'date': date,
                    'symbol': symbol,
                    'message': f"{symbol} close price is not bigger than the minimum over the past 10 "
                               f"days on {date}"
                }

        if message:
            await publish_message(connection=self.app['mq'],
                                  message=message,
                                  routing_key='test_case.events.insert_to_error_logs',
                                  exchange_name='test_case.events',
                                  queue_name='test_case.events.insert_to_error_logs'
                                  )