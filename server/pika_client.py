import pika
import os
import json
import uuid

from loguru import logger
from aio_pika import connect_robust


class PikaClient:
    def __init__(self, process_callable):
        self.amqp_login = os.getenv("AMQP_LOGIN")
        self.amqp_password = os.getenv("AMQP_PASSWORD")
        self.credentials = pika.PlainCredentials(self.amqp_login, self.amqp_password)
        self.publish_queue_name = os.getenv("QUEUE_NAME")
        self.amqp_host = os.getenv("AMQP_HOST")
        logger.warning(self.amqp_host)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost", credentials=self.credentials, heartbeat=0
            )
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(
            queue=self.publish_queue_name, durable=True
        )
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        logger.info("Pika connection initialized")

    async def consume(self, loop):
        connection = await connect_robust(
            host="localhost",
            login=self.amqp_login,
            password=self.amqp_password,
            port=5672,
            loop=loop,
        )
        channel = await connection.channel()
        queue = await channel.declare_queue(self.publish_queue_name, durable=True)
        await queue.consume(self.process_incoming_message, no_ack=False)
        logger.info("Established pika async listener")
        return connection

    async def process_incoming_message(self, message):
        message.ack()
        body = message.body
        logger.info("Received message")
        if body:
            await self.process_callable(json.loads(body))

    def send_message(self, message: dict):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message),
        )
