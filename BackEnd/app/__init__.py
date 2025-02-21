from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.file import file_controller
from app.common.handlers.error_handler import setup_exception_handlers

import os
from dotenv import load_dotenv

# ENV 환경 변수에서 현재 환경을 가져옵니다. 기본값은 'dev'로 설정합니다.
ENV = os.getenv('ENV', 'dev')

# 로드할 .env 파일의 경로를 설정합니다.
dotenv_path = f'.env.{ENV}'

# 해당 .env 파일을 로드합니다.
load_dotenv(dotenv_path)



app = FastAPI()

webUrl = os.getenv("WEB_URL")

# cors option
origins = [
    webUrl,
    #"http://3.38.31.240:8080",
    #"https://localhost:8080",
    #"https://3.38.31.240:8080",
    #"http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# exception
setup_exception_handlers(app)

# router
app.include_router(file_controller.router, prefix="/fastapi/file", tags=["File"])
