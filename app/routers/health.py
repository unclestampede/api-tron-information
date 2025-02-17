from fastapi import APIRouter, Depends, Response

from app.locales.ru import EndpointLocales
from app.services.health import HealthService

router = APIRouter()


@router.get(
    "/health",
    status_code=204,
    summary=EndpointLocales.HEALTH_SUMMARY,
    response_description=EndpointLocales.HEALTH_DESCRIPTION,
    responses={},
)
@router.head(
    "/health",
    status_code=204,
    summary=EndpointLocales.HEALTH_SUMMARY,
    response_description=EndpointLocales.HEALTH_DESCRIPTION,
    responses={},
)
async def health_check(
    health_service: HealthService = Depends(),
) -> Response:
    await health_service.check_health()
    return Response(status_code=204)
