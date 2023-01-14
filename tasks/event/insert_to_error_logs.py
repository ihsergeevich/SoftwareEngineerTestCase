import logging
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class InsertToErrorLogs:
    """
    Class for insert to error_logs table
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'InsertToErrorLogs'

    async def run(self, payload: dict) -> None:
        """
        Get cursor and start insert func
        :param payload:
        :return:
        """
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            await self.__insert_to_error_log(payload, cursor)
        logger.info(f"Finish: {self.worker_name}")

    @staticmethod
    async def __insert_to_error_log(data, cursor):
        sql = f"""
            insert into error_log(date, symbol, message)
            values('{data["date"]}', '{data["symbol"]}', '{data["message"]}')         
            """
        await cursor.execute(sql)
