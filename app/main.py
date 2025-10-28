from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine





app = FastAPI(title="Lib app")


@app.get("/")
def index():
    return {"msg" : "ok"}


@app.get("/db-check")
def db_check():

    try : 
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {"msg" : "conn ok"}

    except Exception as exc :

        return {"exc" : f'{exc}'}
