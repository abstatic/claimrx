from typing import List
import uvicorn
from fastapi import FastAPI, Request, Depends, File, UploadFile
from db import create_db_and_tables, get_db
from sqlmodel import Session
gitfrom utils import getLogger
from middleware import ProcessTimeMiddleware, TransformJSONMiddleware
import time
from models import Claim
from contextlib import asynccontextmanager
log = getLogger(__name__)

# config before and after app start/stop
@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting ClaimRx")
    create_db_and_tables()
    yield
    log.info("Stopping ClaimRx")

app = FastAPI(title="ClaimRx", summary="Claim Processing Service", lifespan=lifespan, debug=True)
app.add_middleware(ProcessTimeMiddleware)
# Dependency
db_sesh = Depends(get_db)


@app.get("/")
async def root(db: Session = db_sesh):
    return {"message": "Welcome to ClaimRx"}


# API for ingesting JSON
@app.post("/claim/add")
async def claims_ingest(request: Request, claims: List[dict]):
    request_body = await request.json()
    body2 = await request.body()
    return {"message": f"Welcome to ClaimRx {request_body} {claims}"}


# API for ingesting from a file
@app.post("/claim/upload/file")
async def claims_upload():
    return {"message": "Thanks for uploading the file"}


# API for given U_ID return the row of claim, along with the netfee
@app.get("/claim/get/{u_id}")
async def claims_get(u_id: int): # , response_model=Claim
    return {"message": f"message received {u_id}"}


# API for returning top10 providers by aggregated net_fees generated
@app.get("providers/top10")
async def providers_top10():
    return {"message": "return top 10 providers"}

# for debugging
if __name__ == "__main__":
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, reload=True)