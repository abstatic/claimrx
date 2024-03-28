from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print("App is starting up")
    # await create_db_and_tables()

@app.on_event("shutdown")
async def on_shutdown():
    print("App is shutting down")
    # gracefully close the DB connection

@app.get("/")
async def root():
    return {"message": "Welcome to ClaimRx"}


# API for ingesting JSON
@app.get("claims/ingest")
async def claims_ingest():
    return {"message": "Welcome to ClaimRx"}


# API for ingesting CSV
# API for given U_ID return the row of claim, along with the netfee
# API for returning top10 providers by aggregated net_fees generated