from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime
from appserver.utils import generate_nanoid
from typing import Optional
from typing_extensions import Annotated
from pydantic import field_validator


class Claim(SQLModel, table=True):
    u_id: str = Field(default_factory=generate_nanoid, primary_key=True, nullable=False)
    created_at: str
    service_date: str
    submitted_procedure: str
    quadrant: Optional[str]
    plan_group: str = Field(default='')
    subscriber_id: int
    provider_npi: int
    provider_fees: float = Field(default=0.0)
    allowed_fees: float = Field(default=0.0)
    member_coinsurance: float = Field(default=0.0)
    member_copay: float = Field(default=0.0)

    @field_validator('submitted_procedure')
    @classmethod
    def validate_sp_field(cls, v: str) -> str:
        if v[0] != 'D':
            raise ValueError("Submitted procedure must begin with a 'D'")
        return v.upper()

    @field_validator('provider_npi')
    @classmethod
    def validate_npi(cls, v: int) -> int:
        if len(str(v)) != 10:
            raise ValueError("Invalid NPI. NPI must be 10 digits long")
        return v
