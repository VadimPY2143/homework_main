from fastapi import FastAPI, Path, Query
import uvicorn
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

metadata.create_all(DATABASE)

DATABASE.connect()


@app.on_event('startup')
async def startup():
    await database.connect()



@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/users/{user_id}')
async def read_user(user_id: int = Path(..., title="user's id", description='This is the id of current user'),
                    text: str = Query('', title = "user's description",description = "This is the user's description")):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    return {'user': user_id,
            'text': text}
