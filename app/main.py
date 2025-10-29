from fastapi import FastAPI
from sqlalchemy import text
import time
from app.database import engine
from sqlalchemy.exc import OperationalError
from app.routes import router
from app.models import Base
import logging
import sys



app = FastAPI(title="Library app")


logger = logging.getLogger("uvicorn.error")


def wait_for_db(retries = 3, delay = 3):
    """
    Ensuring that this service doesnt crash if posgress starts first, and is not ready for connections.
    """
    for attempt in range(1, retries+1):
        try: 
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Connection to DB established.")
            return
        
        except OperationalError as exc:
            logger.warning(f"Attempt {attempt} / {retries} failed, wating {delay} sec")
            if attempt == retries:
                logger.error("Failed to connect to DB, closing application.")
                sys.exit(1)
            
            time.sleep(delay)


wait_for_db(retries=3, delay=3)

Base.metadata.create_all(bind = engine)

app.include_router(router)



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
