import aio_pika
import json
from uuid import uuid4
from time import sleep
from aio_pika.channel import Channel
from aio_pika.queue import Queue
from aio_pika.message import Message
from aio_pika.exceptions import QueueEmpty

from src.xml.xmlmaker import make_xml


mq_url = "amqp://rmuser:rmpassword@rabbitmq"

connection = None
channel = None


class RMQ:
    channel: Channel = None
    queue: Queue = None

    async def make_queue(self, func):
        self.queue = await self.channel.declare_queue("export", auto_delete=False, durable=True)

        try:
            async with self.queue.iterator() as q_iter:
                async for message in q_iter:
                    await func(message)
        except QueueEmpty:
            print("queue is empty")

    async def send(self, data):
        message = Message(
            body=json.dumps(data).encode(),
            content_type="application/json",
            correlation_id=(uuid4())
        )
        await self.channel.default_exchange.publish(message, "export")


async def make_connection(loop):
    global connection
    global channel
    while not connection:
        try:
            connection = await aio_pika.connect_robust(mq_url, loop=loop)
            channel = await connection.channel()
        except Exception as e:
            sleep(5)
            print("Failed to connect. Retry in 5 seconds.")

    return channel

mq = RMQ()
