from datetime import date
from models.risk_model import RiskRequest, RiskResponse

def evaluate_risk(request: RiskRequest):
    """Evaluate the overall risk level of a contract.

    This function analyzes company and contract attributes using helper
    validation rules and determines the final risk classification.

    The final decision follows this priority:
      - HIGH if the company status is not active.
      - MEDIUM if any moderate risk condition is detected.
      - LOW if no risk conditions are found.

    Args:
        request: A `RiskRequest` object containing company status, company
            foundation date, contract value, and contract duration.

    Returns:
        RiskResponse: A Pydantic model containing the final `risk_level`
        and a short explanation (`reason`).
    """
    
    status_risk = check_company_status(request.company_status)
    age_risk = check_company_age(request.company_foundation_date)
    term_risk = check_contract_term(request.contract_term_months)
    value_risk = check_contract_value(request.contract_value)
    
    risk = [status_risk, age_risk, term_risk, value_risk]
    
    if status_risk == "HIGH":
        return RiskResponse(
            risk_level="HIGH",
            reason="Company status is not active"
            )
    elif "MEDIUM" in risk:
        return RiskResponse(
            risk_level="MEDIUM",
            reason="One or more contract or company conditions indicate moderate risk"
            )
    else:
        return RiskResponse(
            risk_level="LOW",
            reason="No risk conditions detected"
            )

def check_company_status(company_status):
    """Check whether the company status indicates high risk.

    A company that is not marked as active is considered high risk.

    Args:
        company_status: The company registration status.

    Returns:
        str | None: Returns `"HIGH"` if the company is not active,
        otherwise `None`.
    """
    if company_status != "ATIVA":
        return "HIGH"
    return None

def check_company_age(company_foundation_date):
    """Evaluate the company age to detect potential risk.

    Companies operating for less than one year are considered
    moderately risky.

    Args:
        company_foundation_date: The company's opening date.

    Returns:
        str | None: Returns `"MEDIUM"` if the company is younger
        than one year, otherwise `None`.
    """
    
    today = date.today()
    company_age = (today - company_foundation_date).days

    if company_age < 365:
        return "MEDIUM"
    return None

def check_contract_term(contract_term_months):
    """Assess the contract duration as a potential risk factor.

    Long-term contracts (48 months or more) are considered
    moderate risk.

    Args:
        contract_term_months: The duration of the contract in months.

    Returns:
        str | None: Returns `"MEDIUM"` for long-term contracts,
        otherwise `None`.
    """
    
    if contract_term_months >= 48:
        return "MEDIUM"
    return None

def check_contract_value(contract_value):
    """Evaluate the financial exposure of the contract.

    Contracts with a value equal to or greater than 200,000
    are considered moderate risk.

    Args:
        contract_value: The monetary value of the contract.

    Returns:
        str | None: Returns `"MEDIUM"` if the contract value
        exceeds the defined threshold, otherwise `None`.
    """
    
    if contract_value >= 200000:
        return "MEDIUM"
    return None