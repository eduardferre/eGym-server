import sys
import os


# Add the parent directory of your project to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append("/Users/eduardfer/Desktop/TFG TELEMÀTICA/eGym-server")

import uvicorn
from utils.logger import logging
from fastapi import FastAPI, Request
from src.main.routers import transactions
from src.main.services import logger_middleware
from src.main.routers import usersTO, exercisesTO, routinesTO
from src.main.routers import users, posts, comments, routines


logging.info("Started!")

# Documentation with Swagger: http://localhost:8000/docs
# Documentation with Redocly: http://localhost:8000/redoc

app = FastAPI()  # uvicorn main:app --reload


# @app.middleware("http")
# async def modify_request_response_middleware(request: Request, call_next):
#     logging.info(f"{request.method} {request.url}")
#     logging.info(request.path_params)
#     response = await call_next(request)
#     logging.info(response)
#     logging.info(response.status_code)
#     return response


# Routers
app.include_router(transactions.router)

app.include_router(usersTO.router)
app.include_router(exercisesTO.router)
app.include_router(routinesTO.router)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(routines.router)


if __name__ == "__main__":
    # Initialization
    uvicorn.run(
        "main:app",
        host="192.168.1.143",
        port=8000,
        reload=True,
        # ssl_keyfile="./key.pem",
        # ssl_certfile="./cert.pem",
    )
