from typing import List, Optional

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.database import get_session
from app.db.dao import TronDAO
from app.db.interface import DBFacadeInterface


class DBFacade(DBFacadeInterface):
    """Фасад для работы с базой данных"""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session
        self._tron_dao = TronDAO(session=session)

    async def commit(self) -> None:
        """Commit изменений"""

        await self._session.commit()

    async def is_db_alive(self) -> bool:
        """Проверка работы БД"""

        try:
            await self._session.execute(text("SELECT 1"))
        except Exception:
            return False
        return True

    async def get_address_count(self, address_list: Optional[List[str]]) -> int:
        """Получение количества адресов TRON"""

        return await self._tron_dao.get_address_count(address_list=address_list)

    async def find_info_by_address(self, address: str) -> Optional[models.TronInfoGet]:
        """Поиск информации о кошельке по адресу TRON"""

        return await self._tron_dao.find_info_by_address(address=address)

    async def get_multiple_address_info(
        self, address_list: Optional[List[str]], limit: int, offset: int
    ) -> List[models.TronInfoGet]:
        """Получение списка данных по кошелькам TRON"""

        return await self._tron_dao.get_multiple_address_info(address_list=address_list, limit=limit, offset=offset)

    async def add_address_info(self, new_tron_data: models.TronInfoCreate) -> models.TronInfoGet:
        """Добавление информации по адресу кошелька TRON"""

        return await self._tron_dao.add_address_info(new_tron_data=new_tron_data)

    async def update_address_info(self, new_tron_data: models.TronInfoCreate) -> models.TronInfoGet:
        """Обновление информации по адресу кошелька"""

        return await self._tron_dao.update_address_info(new_tron_data=new_tron_data)
