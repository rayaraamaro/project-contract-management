from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class RiskRequest(BaseModel):
    contract_value: Decimal
    contract_term_months: int
    company_status: str
    company_foundation_date: date
    
class RiskResponse(BaseModel):
    risk_level: str
    reason: str