from sqlmodel import SQLModel, create_engine, Session
import os
from appserver.utils import getLogger

log = getLogger(__name__)

sqlite_file_name = "claimrx.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
postgres_url = f"postgresql://postgres:postgres@localhost/claimrx"

# connect to postgres only when running in docker compose mode
# else just use sqllite ; in localhost we can use postgres
if os.getenv("DATABASE_URL", "") != "":
    postgres_url = os.getenv("DATABASE_URL")
else:
    postgres_url = sqlite_url

log.info(f"Postgresql url is : {postgres_url}")
engine = create_engine(postgres_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
