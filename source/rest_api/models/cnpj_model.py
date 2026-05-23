from pydantic import BaseModel
from datetime import date

class CNPJDataResponse(BaseModel):
    company_name: str
    company_status: str
    opening_date: date