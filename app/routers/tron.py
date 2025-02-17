from typing import List

from fastapi import APIRouter, Depends, Path, Query, Response

from app import models, utils
from app.services import TronService

router = APIRouter()


@router.get(
    "/tron/information",
    response_model=List[models.TronInfoGet],
    status_code=200,
    summary="",
    response_description="",
    responses={},
)
async def get_multiple_address_info(
    response: Response,
    address_list: List[str] = Query([], description="", alias="addresses"),
    limit: int = Query(30, description="", ge=1, le=100),
    offset: int = Query(0, description="", ge=0, le=9000000000000000000),
    tron_service: TronService = Depends(),
) -> List[models.TronInfoGet]:
    utils.add_pagination_headers_to_response(
        response=response,
        count=await tron_service.get_address_count(address_list=address_list),
        limit=limit,
        offset=offset,
    )
    return await tron_service.get_multiple_address_info(address_list=address_list, limit=limit, offset=offset)


@router.post(
    "/tron/{address}/information",
    response_model=models.TronInfoGet,
    status_code=201,
    summary="",
    response_description="",
    responses={},
)
async def add_address_info(
    address: str = Path(..., description=""),
    tron_service: TronService = Depends(),
) -> models.TronInfoGet:
    return await tron_service.add_address_info(address=address)
