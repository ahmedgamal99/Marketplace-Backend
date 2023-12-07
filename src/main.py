from fastapi import FastAPI
from src.routers.authentication import auth_router
from src.routers.posts import posts
from src.routers.transactions import transactions

app = FastAPI()

app.include_router(prefix="/prefix", router=auth_router)
app.include_router(prefix="/posts", router=posts)
app.include_router(prefix="/transactions", router=transactions)
