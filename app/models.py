from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime
from utils import generate_nanoid
from typing import Optional
from pydantic import field_validator


class Claim(SQLModel, table=True):
    u_id: str = Field(default_factory=generate_nanoid, primary_key=True, nullable=False)
    created_at: datetime = Field(default=datetime.utcnow, nullable=False)
    service_datetime: datetime = Field(default=datetime.utcnow, nullable=False)
    submitted_procedure: str = Field(nullable=False)
    quadrant: Optional[str]
    plan_group: str = Field(default='')
    subscriber_id: int = Field(default=0)
    provider_npi: int = Field(default=0)
    provider_fees: float = Field(default=0.0)
    allowed_fees: float = Field(default=0.0)
    member_coinsurance: float = Field(default=0.0)
    member_copay: float = Field(default=0.0)

    @field_validator('submitted_procedure')
    def validate_sp_field(self, v: str) -> str:
        if v[0] != 'D':
            raise ValueError("Submitted procedure must begin with a 'D'")
        return v.upper()

    @field_validator('provider_npi')
    def validate_npi(self, v: int) -> int:
        if len(str(v)) != 10:
            raise ValueError("Invalid NPI. NPI must be 10 digits long")
        return v
