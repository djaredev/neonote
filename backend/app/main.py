from fastapi import FastAPI
from app.api.router import api_router
from app.core.db import create_db_and_tables

create_db_and_tables()

app = FastAPI()


app.include_router(api_router)
