import re
import requests
from datetime import datetime, date
from models.cnpj_model import CNPJDataResponse

def normalize_cnpj(cnpj: str) -> str:
    """Normalize a CNPJ string by removing any non-digit characters.

        This function strips punctuation such as dots, slashes, and dashes,
        returning only the numeric digits present in the CNPJ input. It does
        not validate the length or check verification digits.

        Args:
            cnpj: The CNPJ string, possibly containing punctuation or whitespace.

        Returns:
            A string containing only the digits of the provided CNPJ.
            Example: `"12.345.678/0001-90"` → `"12345678000190"`.
        """
    return re.sub(r"\D", "", cnpj or "")

def get_cnpj_data(cnpj: str) -> CNPJDataResponse:
    """Fetch summarized CNPJ data from BrasilAPI.

        This function:
        1) Normalizes the input CNPJ (digits only).
        2) Calls BrasilAPI's CNPJ endpoint.
        3) Maps the response to a `CNPJDataResponse` with:
            - `company_name` (from `razao_social`)
            - `company_status` (from `descricao_situacao_cadastral`)
            - `opening_date` (from `data_inicio_atividade`, parsed as `date`)

        If the opening date cannot be parsed (unexpected format), it will be
        returned as `None`. Network and HTTP errors are propagated to the caller.

        Args:
            cnpj: The CNPJ identifier string, with or without formatting.

        Returns:
            CNPJDataResponse: A Pydantic model containing the company's
            name, status, and opening date (as a `date` or `None`).

        Raises:
            requests.exceptions.RequestException: For network-related errors
                (e.g., timeouts, connection issues).
            requests.exceptions.HTTPError: If the response status is an error
                (e.g., 4xx/5xx). The caller can inspect `response.status_code`
                and `response.json()` from the exception's response.
            ValueError: If any local parsing error is raised explicitly by future
                validations (currently, date parsing failures are tolerated and
                return `None` instead).
    """
    formatted_cnpj = normalize_cnpj(cnpj)

    url = f"https://brasilapi.com.br/api/cnpj/v1/{formatted_cnpj}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    company_name = data.get("razao_social")
    company_status = data.get("descricao_situacao_cadastral")
    raw_opening_date = data.get("data_inicio_atividade")

    opening_date: date | None = None
    if raw_opening_date:
        try:
            opening_date = datetime.strptime(raw_opening_date, "%Y-%m-%d").date()
        except Exception:
            opening_date = None

    return CNPJDataResponse(
        company_name=company_name or "",
        company_status=company_status or "",
        opening_date=opening_date,
    )
