import uvicorn
import logging
from fastapi import FastAPI
from routers import usersTO, exercisesTO, routinesTO
from routers import users


logging.basicConfig(
    # filename="logs.log",
    format="%(asctime)s | %(module)s.py (LINE %(lineno)d) - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

logging.info("Started!")


# Documentation with Swagger: http://localhost:8000/docs
# Documentation with Redocly: http://localhost:8000/redoc

app = FastAPI()  # uvicorn main:app --reload

# Routers
app.include_router(usersTO.router)
app.include_router(exercisesTO.router)
app.include_router(routinesTO.router)

app.include_router(users.router)


# Router: root
@app.get("/")
async def root():
    return "Welcome to eGym!"


if __name__ == "__main__":
    # Initialization
    uvicorn.run(app, host="localhost", port=8000)
