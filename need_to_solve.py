from webui_models.webui_llm import result_chat_model
from models.langchain_models import llm_qwen_7B
import asyncio
from fastapi import FastAPI, WebSocket
import uvicorn
from utils.util import *

app = FastAPI()

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    logger.info('开始')
    await websocket.send_text('开始')
    async for chunk in llm_qwen_7B.astream("你好。告诉我一些关于你自己的事情"):
        
        logger.info(chunk.content)
        await websocket.send_text(chunk.content)

if __name__ == '__main__':
    

    uvicorn.run(app=app, host='0.0.0.0', port=33064)


