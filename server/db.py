import os
import dotenv
import databases
import sqlalchemy
from ormar import ModelMeta

DATABASE_URL = os.getenv("DATABASE_URL")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)


class MainMeta(ModelMeta):
    metadata = metadata
    database = database
