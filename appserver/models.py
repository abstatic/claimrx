import sqlalchemy
from sqlmodel import Field, SQLModel
from datetime import datetime
from appserver.utils import generate_nanoid
from typing import Optional, List
from pydantic import field_validator


class ClaimBase(SQLModel):
    u_id: str = Field(default_factory=generate_nanoid, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # TODO adopt this in other places
    # currency: str = Field(default='USD')
    service_date: datetime
    submitted_procedure: str = Field()
    quadrant: Optional[str]
    plan_group: str = Field(default='')
    subscriber_id: int
    provider_npi: int = Field(index=True)
    provider_fees: float = Field(default=0.0)
    allowed_fees: float = Field(default=0.0)
    member_coinsurance: float = Field(default=0.0)
    member_copay: float = Field(default=0.0)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('subscriber_id', 'provider_npi', 'plan_group', 'submitted_procedure', name='uniq_constr'),
    )

    @field_validator('submitted_procedure', mode='before')
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


class Claim(ClaimBase, table=True):
    net_fee: float = Field(default=0.0)


# Response Models
class ClaimRead(ClaimBase):
    @field_validator('provider_fees', 'allowed_fees', 'member_coinsurance', 'member_copay')
    @classmethod
    def validate_member_copy(cls, v: float) -> str:
        return "$" + str(v)

    provider_fees: float = Field(default=0.0)
    allowed_fees: float = Field(default=0.0)
    member_coinsurance: float = Field(default=0.0)
    member_copay: float = Field(default=0.0)


class ClaimReadResponse(SQLModel):
    status: str
    claim: ClaimRead


class ClaimCreateResponse(SQLModel):
    status: str
    u_ids: List[int]
    claim: List[ClaimRead]


class ClaimListReadResponse(SQLModel):
    status: str
    claim: List[Claim]


class ProviderEntry(SQLModel):
    provider_npi: int
    total_net_fee: float


class TopProviderResponse(SQLModel):
    status: str
    top_providers: List[ProviderEntry]
