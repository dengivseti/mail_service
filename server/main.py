import dotenv

dotenv.load_dotenv("server.env")

from fastapi import FastAPI

from users.api import user_router
from domains.api import domain_router
from db import database, metadata, engine

app = FastAPI()

metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(user_router)
app.include_router(domain_router)
