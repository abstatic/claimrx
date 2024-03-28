from sqlmodel import Field, SQLModel, create_engine


class Claim(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service_datetime
    submitted_procedure
    quadrant
    plan
    subscriber_id
    provider_npi
    provider_fees
    allowed_fees
    member_coinsurance
    member_copay

