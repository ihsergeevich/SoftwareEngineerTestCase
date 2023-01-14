import argparse
import asyncio
import traceback
from logging.config import dictConfig

import asyncpg
import orjson
import logging

from aiohttp.web import Application
from aio_pika import connect_robust

from config import Config
from tasks.event.calculate_average_absolute_daily_percent_change import CalculateAverageAbsoluteDailyPercentChange
from tasks.event.calculate_the_average_dollar_volume import CalculateTheAverageDollarVolume
from tasks.event.check_row_handler import CheckRowsHelper
from tasks.event.get_percent_by_last_40_t_for_symbol import GetPercentByLast40tForSymbol
from tasks.event.insert_to_bars_1 import InsertToBars1
from tasks.event.insert_to_error_logs import InsertToErrorLogs
from tasks.event.rank_stocks_by_positive_volume import RankStocksByPositiveVolume
from tasks.periodic.check_rows import CheckRows

dictConfig(Config.LOGGING)
logger = logging.getLogger(__name__)

TASKS = {
    'test_case.events.get_percent': GetPercentByLast40tForSymbol,
    'test_case.events.calculate_average_dollar_volume': CalculateTheAverageDollarVolume,
    'test_case.events.calculate_average_percent': CalculateAverageAbsoluteDailyPercentChange,
    'test_case.events.rank_stocks_by_positive_volume': RankStocksByPositiveVolume,
    'test_case.events.insert_to_error_logs': InsertToErrorLogs,
    'test_case.events.insert_to_bars_1': InsertToBars1,
    'test_case.events.check_rows_helper': CheckRowsHelper,

    'test_case.periodic.check_rows': CheckRows,

}


class Consumer:
    """
    Producer get periodic and events tasks from RabbitMQ
    """
    def __init__(self, loop, queue=None):
        self.app = Application()
        self.loop = loop
        self.queue = queue
        self.rabbit_url = f"amqp://{Config.RABBIT['username']}:{Config.RABBIT['password']}@{Config.RABBIT['host']}:{Config.RABBIT['port']}/"  # noqa
        self.periodic_tasks = []

    async def run(self):
        await self.setup_db()
        await self.setup_mq()
        connection = await connect_robust(self.rabbit_url, loop=loop)

        logger.info(f"Queue: {self.queue}")
        logger.info(f"Exist queue: {self.queue in TASKS}")

        if self.queue and self.queue in TASKS:
            logger.info("Single work option")
            self.periodic_tasks.append(self.loop.create_task(self._consume(connection, self.queue)))

        else:
            logger.info("Multiple work option")
            for queue_name in TASKS:
                self.periodic_tasks.append(self.loop.create_task(self._consume(connection, queue_name)))

    async def setup_db(self):
        self.app['db'] = await asyncpg.create_pool(**Config.POSTGRES)

    async def setup_mq(self):
        self.app['mq'] = await connect_robust(self.rabbit_url, loop=loop)

    async def _consume(self, connection, queue_name):
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.consume(self.on_message)

    async def on_message(self, message):
        logger.info(f"\n\nReceived message {message.routing_key}")
        try:
            if 'test_case.periodic' in message.routing_key:
                await message.ack()
            task = TASKS.get(message.routing_key)(self.app)
            await task.run(orjson.loads(message.body))
            logger.info(f"Success task {message.routing_key}")
            if 'test_case.events' in message.routing_key:
                await message.ack()
        except Exception as e:
            logger.info(f"Error {e} while serving task {message.routing_key}")
            traceback.print_exc()
            await message.ack()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', nargs='?', default='test_case.events.get_percent', const=True, dest='queue')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    worker = Consumer(loop, queue=args.queue.strip())
    loop.run_until_complete(worker.run())

    try:
        loop.run_forever()
    finally:
        loop.close()
