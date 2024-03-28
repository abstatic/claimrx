from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "claimrx.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
postgres_url = f"postgresql://postgres:postgres@localhost/claimrx"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
