from fastapi import FastAPI, Request, Depends
from .db import create_db_and_tables, get_db
from sqlmodel import Session
from .utils import getLogger
import time

log = getLogger(__name__)
app = FastAPI()

# Dependency
db_sesh = Depends(get_db)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
def on_startup():
    log.debug("App is starting up")
    create_db_and_tables()


@app.on_event("shutdown")
async def on_shutdown():
    log.debug("App is shutting down")
    # gracefully close the DB connection


@app.get("/")
async def root(db: Session = db_sesh):
    return {"message": "Welcome to ClaimRx"}


# API for ingesting JSON
@app.get("claims/ingest")
async def claims_ingest():
    return {"message": "Welcome to ClaimRx"}


# API for ingesting from a file
@app.get("claims/upload/file")
async def claims_upload():
    return {"message": "Thanks for uploading the file"}


# API for given U_ID return the row of claim, along with the netfee
@app.get("claims/get/{u_id}")
async def claims_get(u_id: int): # , response_model=Claim
    return {"message": f"message received {u_id}"}


# API for returning top10 providers by aggregated net_fees generated
@app.get("providers/top10")
async def providers_top10():
    return {"message": "return top 10 providers"}

