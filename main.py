import asyncio

from contextlib import asynccontextmanager
from llama_cpp import Llama
from openai import AsyncOpenAI
from fastapi import FastAPI, Body, Request, Depends
from fastapi.responses import StreamingResponse

from config import settings
from schema import OpenAIResponse


SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = Llama(
        model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=2,
        verbose=False,
        chat_format="llama-3",
    )
    app.state.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    yield

# user_input = input("질문을 입력하세요:").strip()

app = FastAPI()

# 요청 객체(request)에서 llm 객체를 접근할 수 있게 해주는 의존성 함수
def get_llm(request: Request):
    return request.app.state.llm

def get_openai_client(request: Request):
    return request.app.state.openai_client


@app.post("/chats")
async def generate_chat_handler(
    user_input: str = Body(..., embed=True),
    llm = Depends(get_llm),
):
    async def event_generator():
        result = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            max_tokens=256,
            temperature=0.7,
            stream=True,
        )
        for chunk in result:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                yield token
                await asyncio.sleep(0.1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )

@app.post("/openai")
async def openai_handler(
    user_input: str = Body(..., embed=True),
    openai_client = Depends(get_openai_client),
):
    
    async def event_generator():
        async with openai_client.responses.stream(
            model="gpt-4.1-mini",
            input=user_input,
            text_format=OpenAIResponse,
        ) as stream:
            async for event in stream:
                # 텍스트 토큰
                if event.type == "response.output_text.delta":
                    yield event.delta

                # 연결 종료
                elif event.type == "response.completed":
                    break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )