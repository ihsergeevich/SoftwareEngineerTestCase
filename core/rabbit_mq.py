import orjson
from aio_pika import Message, ExchangeType


async def publish_message(connection, message: dict, routing_key: str, exchange_name: str, queue_name: str) -> None:
    """
    Publish message to RabbitMQ with routing_key, exchange_name, queue_name
    :param connection:
    :param message:
    :param routing_key:
    :param exchange_name:
    :param queue_name:
    :return: None
    """
    channel = await connection.channel()
    exchange = await channel.declare_exchange(exchange_name, type=ExchangeType.DIRECT, durable=True)

    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange, routing_key=routing_key)

    message_body = orjson.dumps(message)
    message = Message(message_body)

    await exchange.publish(message, routing_key=routing_key)
    await channel.close()

