import logging
import os
from logging.config import dictConfig

from config import Config

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)


class BaseTask:
    """
    Base event task class
    """
    __slots__ = 'app', 'worker_name'

    async def run(self, payload: dict) -> None:
        """
        Get cursor, info from db and save answers
        :param payload:
        :return:
        """
        logger.info(f"Start: {self.worker_name}")
        async with self.app['db'].acquire() as cursor:
            task_num, answer = await self.get_info(cursor)
            await self.save(task_num, answer)
        logger.info(f"Finish: {self.worker_name}")

    async def get_info(self, cursor) -> (str, list):
        raise 'Method not implemented'

    @staticmethod
    async def save(task_num: str, answer: list) -> None:
        """
        Save answer to txt file
        :param task_num:
        :param answer:
        :return:
        """
        filename = f"/workers/answers/{task_num}.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            if isinstance(answer, list):
                for a in answer:
                    f.write(f'{a}\n')
            else:
                f.write(f'{answer}\n')

            f.close()
