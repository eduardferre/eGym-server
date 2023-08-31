import uvicorn
from fastapi import FastAPI
from routers import usersTO, exercisesTO, routinesTO
from routers import users


# Documentation with Swagger: http://localhost:8000/docs
# Documentation with Redocly: http://localhost:8000/redoc

app = FastAPI() # uvicorn main:app --reload

# Routers
app.include_router(usersTO.router)
app.include_router(exercisesTO.router)
app.include_router(routinesTO.router)

app.include_router(users.router)

@app.get("/")
async def root():
    return "Hello FastAPI!"

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)