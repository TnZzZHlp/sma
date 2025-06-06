import time
from fastapi import FastAPI, File
from fastapi.responses import StreamingResponse
from src.ai.solution import generate_solution
from src.ai.check import generate_check

app = FastAPI()


@app.get("/")
async def root():
    # 返回当前时间
    return {"time": time.time()}


@app.post("/ai/solution")
async def get_solution(image: bytes = File()):

    async def stream():
        for chunk in generate_solution(
            image,
        ):
            if chunk.text:
                yield chunk.text
            else:
                raise Exception("错误：生成响应时发生异常")

    try:
        # 生成响应
        return StreamingResponse(stream(), media_type="text/plain")

    except Exception as e:
        return {"error": str(e)}


@app.post("/ai/check")
async def get_check(image: bytes = File()):

    async def stream():
        for chunk in generate_check(
            image,
        ):
            if chunk.text:
                yield chunk.text
            else:
                raise Exception("错误：生成响应时发生异常")

    try:
        # 生成响应
        return StreamingResponse(stream(), media_type="text/plain")

    except Exception as e:
        return {"error": str(e)}
