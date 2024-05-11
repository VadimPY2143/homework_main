from fastapi import FastAPI
import sqlite3
from databases import Database
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
import asyncio

DATABASE_URL = 'sqlite:///test.db'
DATABASE = create_engine(DATABASE_URL)
metadata = MetaData()
database = Database(DATABASE_URL)

app = FastAPI()

users = Table('users',
              metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('surname', String),
              Column('job', String(10))
              )


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    return {'user': user}

