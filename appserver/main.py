from typing import List
import uvicorn
from fastapi import FastAPI, Request, Depends, File, UploadFile
from appserver.db import create_db_and_tables, get_db
from sqlmodel import Session
from appserver.utils import getLogger, preprocess_params
from middleware import ProcessTimeMiddleware
from datetime import datetime
import time
from appserver.models import ClaimBase, Claim, ClaimRead
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
async def root():
    return {"message": "Welcome to ClaimRx"}


# API for ingesting JSON
@app.post("/claim/add")
async def claims_ingest(claims: List[dict], db: Session = db_sesh):
    processed = []
    claims_created = []
    for c in claims:
        c = preprocess_params(c)

        # start with claim base
        c = ClaimBase(**c)
        c.created_at = datetime.now()

        # transform to table mapped class and push to db
        db_claim = Claim.model_validate(c)
        db.add(db_claim)
        db.commit()
        claims_created.append(ClaimRead.model_validate(c))
        processed.append(c.u_id)

    # TODO it'd be good to have annotated type for this, better documentation
    return {"status": f"success", "u_ids": f"{processed}", "claims": f"{claims_created}"}


# API for ingesting from a file
@app.post("/claim/upload/file")
async def claims_upload():
    return {"message": "Thanks for uploading the file"}


@app.get("/claim/get/{u_id}")
async def claims_get(u_id: str, db: Session = db_sesh):
    """
    Given a claim id return the claim info
    :param u_id: unique id of claim
    :param db:
    :return: json object containing
    """
    ins = db.get(Claim, u_id)
    if ins is not None:
        ins = ClaimRead(**ins.model_dump())
        return {"status": "success", "claim": ins}
    else:
        return {"status": "failed"}


# API for returning top10 providers by aggregated net_fees generated
@app.get("/providers/top10")
async def providers_top10():
    return {"message": "return top 10 providers"}


# debugging
@app.get("/claims")
async def get_claims(db: Session = db_sesh) -> List[ClaimRead]:
    """
    Return all claims in DB as a list. Only for debugging
    :param db:
    :return: List of ClaimRead objects
    """
    return db.query(Claim).all()


# for debugging
if __name__ == "__main__":
    uvicorn.run('appserver.main:app', host='127.0.0.1', port=8000, reload=True)
