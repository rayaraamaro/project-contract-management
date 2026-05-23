import requests
from fastapi import APIRouter, HTTPException
from services.cnpj_info_service import get_cnpj_data
from models.cnpj_model import CNPJDataResponse

router = APIRouter(prefix="", tags=["CNPJ"])

@router.get("/{cnpj:path}", response_model=CNPJDataResponse)
def get_cnpj_summary(cnpj: str):
    """Return a summarized CNPJ profile using BrasilAPI.

    The `cnpj` path parameter may be provided with or without formatting
    (e.g., "00.000.000/0001-91" or "00000000000191"). The underlying service
    is responsible for normalizing the value (digits only), calling BrasilAPI,
    and mapping the response to `CNPJDataResponse`.

    Success responses include:
      - `razao_social` (company_name)
      - `empresa_status` (company_status)
      - `data_abertura` (opening_date as ISO date)

    This route also converts upstream errors into standardized HTTP responses:
      * 400 Bad Request → invalid CNPJ format/content, following the upstream
        error body structure.
      * 404 Not Found → CNPJ not found.
      * 500 Internal Server Error → unexpected local errors.
      * 502 Bad Gateway → other HTTP errors returned by the upstream service.
      * 504 Gateway Timeout → local timeout/connection issues.

    Args:
        cnpj: The CNPJ identifier captured from the URL path. May include
            punctuation (e.g., dots, slashes, dashes).

    Returns:
        CNPJDataResponse: A Pydantic model with the company’s name, status,
        and opening date.

    Raises:
        HTTPException: If any error occurs, the function raises an appropriate
            `HTTPException` with a standardized `detail` payload:
              - 400 with {"error","message","type"} for bad requests.
              - 404 with {"error","message","type"} when not found.
              - 500 for unexpected local exceptions.
              - 502 for other upstream HTTP errors.
              - 504 for network timeouts/connection errors.
    """

    try:
        return get_cnpj_data(cnpj)

    except requests.exceptions.HTTPError as http_err:
        status = http_err.response.status_code
        error_body = {}
        try:
            error_body = http_err.response.json()
        except Exception:
            pass

        if status == 400:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": error_body.get("name", "BadRequestError"),
                    "message": error_body.get("message", "CNPJ inválido."),
                    "type": error_body.get("type", "bad_request"),
                },
            )

        if status == 404:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": error_body.get("name", "NotFoundError"),
                    "message": error_body.get("message", "CNPJ não encontrado."),
                    "type": error_body.get("type", "not_found"),
                },
            )

        raise HTTPException(
            status_code=502,
            detail={"error": "UpstreamError", "message": str(http_err)},
        )

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as net_err:
        raise HTTPException(
            status_code=504,
            detail={"error": "NetworkTimeout", "message": str(net_err)},
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error": "InternalServerError", "message": str(exc)},
        )