from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import uvicorn
from pydantic import BaseModel, ValidationError, field_validator
from typing import Any
import json
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/')
def func():
    return {'message': 'hello'}


@app.websocket('/ws')
async def websocket_(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({'status': 'connected', 'message': f'{data}'})

    except WebSocketDisconnect:
        await websocket.send_json({'status': 'disconnected'})
        await websocket.close()

