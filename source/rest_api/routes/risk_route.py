from services.risk_service import evaluate_risk
from models.risk_model import RiskResponse, RiskRequest

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/evaluate-risk", response_model=RiskResponse)
def evaluate_contract_risk(request: RiskRequest):
    """Evaluate the risk level of a contract based on company and contract data.

    The request body must contain information about the contract and the company,
    including the contract value, contract duration, company status, and company
    foundation date. The underlying service is responsible for applying business
    rules to determine the risk classification and mapping the result to
    `RiskResponse`.

    The evaluation considers the following factors:
    - `company_status`: verifies whether the company is active.
    - `company_foundation_date`: determines the company's age.
    - `contract_term_months`: evaluates the duration of the contract.
    - `contract_value`: analyzes the financial exposure of the contract.

    The service combines these signals to classify the contract risk level
    as LOW, MEDIUM, or HIGH.

    Args:
        request: A `RiskRequest` object containing the required contract and
            company information for the risk evaluation.

    Returns:
        RiskResponse: A Pydantic model containing:
            - `risk_level`: The calculated risk classification (LOW, MEDIUM, HIGH).
            - `reason`: A short explanation describing why the contract received
            the assigned risk level.

    Raises:
        HTTPException: If an unexpected error occurs during the evaluation
            process, the function may raise an HTTP exception with an appropriate
            error message and status code.
    """

    result = evaluate_risk(request)
    return result
