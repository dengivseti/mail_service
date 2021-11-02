import dotenv
import time
import asyncio


dotenv.load_dotenv("server.env")

from fastapi import FastAPI
from users.api import user_router
from domains.api import domain_router
from api.api import api_router
from mails.api import mail_router
from db import database, metadata, engine
from pika_client import PikaClient
from loguru import logger
from mails.services import send_emails

metadata.create_all(engine)


class API(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_int_value = 0
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    async def log_incoming_message(cls, message: dict):
        global check_int_value
        logger.error(f"Incoming message : {message}")
        await send_emails(message)


app = API()
app.state.database = database


app.include_router(user_router)
app.include_router(domain_router)
app.include_router(mail_router)
app.include_router(api_router)


@app.on_event("startup")
async def startup() -> None:
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task

    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
