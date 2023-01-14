import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToBars1:
    """
    Insert to bars_1 tavle class
    """
    __slots__ = 'app', 'worker_name'

    def __init__(self, app):
        self.app = app
        self.worker_name = 'InsertToBars1'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload:
        :return:
        """
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_bars_1(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert_to_bars_1(data, cursor) -> None:
        sql = f"""
            insert into bars_1(date, symbol, adjclose, close, high, low, open, volume)
            values('{data["date"]}', '{data["symbol"]}', {data["adjclose"]}, {data["close"]}, {data["high"]}, 
                    {data["low"]}, {data["open"]}, {data["volume"]})         
            """

        await cursor.execute(sql)
