from fastapi import FastAPI


# Documentation with Swagger: http://localhost:8000/docs
# Documentation with Redocly: http://localhost:8000/redoc

app = FastAPI() # uvicorn main:app --reload

# Routers
# app.include_router(users.router)
# app.include_router(products.router)

# app.include_router(basic_auth_users.router)
# app.include_router(jwt_auth_users.router)

# app.include_router(users_db.router)

# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def root():
#     return "Hello FastAPI!"

# @app.get("/url")
# async def root():
#     return { "url_github": "https://github.com/eduardferre" }