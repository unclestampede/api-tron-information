from typing import List, Optional

from fastapi import Depends, HTTPException
from loguru import logger
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound, BadAddress

from app import models
from app.db import DBFacadeInterface, get_db_facade
from app.tron_session import get_tron_session


class TronService:
    def __init__(
        self, db_facade: DBFacadeInterface = Depends(get_db_facade), tron_session: AsyncTron = Depends(get_tron_session)
    ):
        self._db_facade = db_facade
        self._tron_session = tron_session

    async def get_address_count(self, address_list: Optional[List[str]]) -> int:
        """Получение количества адресов TRON"""

        logger.debug(f"Запрос на получение количества адресов TRON, входные данные: {address_list=}")

        address_count = await self._db_facade.get_address_count(address_list=address_list)
        logger.debug(f"Количество адресов: {address_count}")

        return address_count

    async def get_multiple_address_info(
        self, address_list: Optional[List[str]], limit: int, offset: int
    ) -> List[models.TronInfoGet]:
        """Получение списка данных по кошелькам TRON"""

        logger.debug(f"Запрос на получение списка действий, параметры: {limit=} {offset=} {address_list=}")

        address_info_list = await self._db_facade.get_multiple_address_info(
            address_list=address_list, limit=limit, offset=offset
        )
        logger.debug(f"Действия получены: {address_info_list=}")

        return address_info_list

    async def add_address_info(self, address: str) -> models.TronInfoGet:
        """Добавление информации по адресу кошелька TRON"""

        logger.debug(f"Запрос на получении информации о кошельке {address}")

        new_tron_data = await self._get_tron_address_info(address=address)
        if not await self._db_facade.find_info_by_address(address=address):
            new_address_info = await self._db_facade.add_address_info(new_tron_data=new_tron_data)
        else:
            new_address_info = await self._db_facade.update_address_info(new_tron_data=new_tron_data)

        await self._db_facade.commit()

        logger.info(f"Создана новая запись в БД: {new_address_info=}")
        return new_address_info

    async def _get_tron_address_info(self, address: str) -> models.TronInfoCreate:
        """Получении информации об адресе"""
        try:
            account_info = await self._tron_session.get_account(address)
            resource = await self._tron_session.get_account_resource(address)

            balance = account_info.get("balance", 0) / 1000000
            energy = resource.get("EnergyLimit", 0)
            bandwidth = resource.get("freeNetLimit", 0)

            return models.TronInfoCreate(address=address, balance=balance, energy=energy, bandwidth=bandwidth)
        except BadAddress:
            logger.warning(f"Указан невалидный адрес {address}")
            raise HTTPException(status_code=400, detail="Указан невалидный адрес")
        except AddressNotFound:
            logger.warning(f"Указан несуществующий адрес {address}")
            raise HTTPException(status_code=404, detail="Указан несуществующий адрес")
