import argparse
import asyncio
import logging
from logging.config import dictConfig

from aio_pika import connect

from config import Config
from core.rabbit_mq import publish_message

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)

TASKS = {
    'events': [
        'test_case.events.get_percent',
        'test_case.events.calculate_average_dollar_volume',
        'test_case.events.calculate_average_percent',
        'test_case.events.rank_stocks_by_positive_volume'
    ],
    'periodic': [
        'test_case.periodic.check_rows'
    ]
}


class Producer:
    """
    Producer publish periodic and events tasks to RabbitMQ
    """

    def __init__(self, loop, task_type):
        self.loop = loop
        self.rabbit_url = f"amqp://{Config.RABBIT['username']}:{Config.RABBIT['password']}@{Config.RABBIT['host']}:{Config.RABBIT['port']}/"  # noqa
        self.periodic_tasks = []
        self.task_type = task_type

    async def run(self) -> None:
        for task in TASKS[self.task_type]:
            logger.info(f"start task: {task}")
            self.periodic_tasks.append(self.loop.create_task(self._publishing_task(task)))

    async def _publishing_task(self, task: str) -> None:
        """
        RabbitMQ task publisher
        :param task: task queue name
        :return:
        """
        connection = await connect(url=self.rabbit_url, loop=self.loop)
        logger.info(f"publish_message for task: {task}")
        await publish_message(connection=connection,
                              message={},
                              routing_key=task,
                              exchange_name='.'.join(task.split('.')[0:2]),
                              queue_name=task)

        await connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    parser = argparse.ArgumentParser()
    parser.add_argument('-tt', default='events')
    args = parser.parse_args()

    worker = Producer(loop, args.tt)
    loop.run_until_complete(worker.run())

    try:
        loop.run_forever()
    finally:
        loop.close()
