from typing import List
import uvicorn
from fastapi import FastAPI, Request, Depends, File, UploadFile
from appserver.db import create_db_and_tables, get_db
from sqlmodel import Session
from sqlalchemy import func, select
from appserver.utils import getLogger, preprocess_params
from middleware import ProcessTimeMiddleware
from datetime import datetime
from appserver.models import (ClaimBase, Claim, ClaimRead, ClaimReadResponse, ClaimCreateResponse,
                              ClaimListReadResponse, TopProviderResponse, ProviderEntry)
from contextlib import asynccontextmanager
from slowapi import Limiter
from slowapi.util import get_remote_address

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
# Rate limiting
limiter = Limiter(
    get_remote_address,
    default_limits=["2 per minute", "1 per second"],
    storage_uri="memory://",
    strategy="moving-window"
)
# Dependency
db_sesh = Depends(get_db)


@app.get("/")
async def root():
    return {"message": "Welcome to ClaimRx"}


# API for ingesting JSON
@app.post("/claim/add")
async def claims_ingest(claims: List[dict], db: Session = db_sesh) -> ClaimCreateResponse:
    """
    This method processes claims,
    :param claims: list of dict, since keys can be in any format
    :param db: db inject
    :return: return u_ids and claim objects which are constructed
    """
    processed = []
    claims_created = []
    for c in claims:
        c = preprocess_params(c)

        # start with claim base
        c = ClaimBase(**c)
        c.created_at = datetime.now()

        # transform to table mapped class and push to db
        db_claim = Claim.model_validate(c)
        db_claim.net_fee = c.provider_fees + c.member_copay + c.member_coinsurance - c.allowed_fees
        db.add(db_claim)
        db.commit()
        claims_created.append(ClaimRead.model_validate(c))
        processed.append(c.u_id)

    # TODO it'd be good to have annotated type for this, better documentation
    return ClaimCreateResponse(status="success", u_ids=processed, claim=claims_created)


# API for ingesting from a file
@app.post("/claim/upload/file")
async def claims_upload():
    return {"message": "Thanks for uploading the file"}


@app.get("/claim/get/{u_id}")
async def claims_get(u_id: str, db: Session = db_sesh) -> ClaimReadResponse:
    """
    Given a claim id return the claim info
    :param u_id: unique id of claim
    :param db:
    :return: json object containing
    """
    ins = db.get(Claim, u_id)
    if ins is not None:
        ins = ClaimRead(**ins.model_dump())
        resp = ClaimReadResponse(status="success", claim=ins)
        return resp

# API for returning top10 providers by aggregated net_fees generated
@app.get("/providers/top")
@limiter.limit("10 per min")
async def providers_top10(request: Request, db: Session = db_sesh) -> TopProviderResponse:
    """
    Returns the top10 providers by aggregate of net_fee
    :param request: required for ratelimiting
    :param db: db injection
    :return: list of provider id
    """

    """
    syntax:
    SELECT column_1, function_name(column_2)
    FROM table_name
    WHERE [condition]
    GROUP BY column_name
    ORDER BY column_name;
    # aggregate on netfee and group_by provider_id
    """
    sum_net_fee = func.sum(Claim.net_fee).label('total_net_fee')
    query = select(Claim.provider_npi, sum_net_fee) \
        .group_by(Claim.provider_npi) \
        .order_by(sum_net_fee.desc()) \
        .limit(10)
    res = db.exec(query)

    top_providers = []
    for row in res:
        top_providers.append(ProviderEntry(provider_npi=row[0], total_net_fee=row[1]))

    return TopProviderResponse(status="success", top_providers=top_providers)

# debugging
@app.get("/claims")
async def get_claims(db: Session = db_sesh) -> ClaimListReadResponse:
    """
    Return all claims in DB as a list. Only for debugging
    :param db:
    :return: List of ClaimRead objects
    """
    return ClaimListReadResponse(status="success", claim=db.query(Claim).all())


# for debugging
if __name__ == "__main__":
    uvicorn.run('appserver.main:app', host='127.0.0.1', port=8000, reload=True)
