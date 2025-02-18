from typing import List, Optional

from sqlalchemy import BigInteger, asc, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app import models
from app.db import tables


class TronDAO:
    """DAO для работы с таблицей TRON"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_address_count(self, address_list: Optional[List[str]]) -> int:
        """Получение количества адресов TRON"""

        query = select(func.count(tables.TronInfo.address))

        if address_list:
            query = query.where(tables.TronInfo.address.in_(address_list))

        return (await self._session.execute(query)).scalar()

    async def find_info_by_address(self, address: str) -> Optional[models.TronInfoGet]:
        """Поиск информации о кошельке по адресу TRON"""

        query = select(tables.TronInfo).where(tables.TronInfo.address == address)
        db_candidate = (await self._session.execute(query)).scalar()

        if not db_candidate:
            return None

        return models.TronInfoGet.model_validate(db_candidate)

    async def get_multiple_address_info(
        self, address_list: Optional[List[str]], limit: int, offset: int
    ) -> List[models.TronInfoGet]:
        """Получение списка данных по кошелькам TRON"""

        query = select(tables.TronInfo).limit(limit).offset(cast(offset, BigInteger))

        if address_list:
            query = query.where(tables.TronInfo.address.in_(address_list))

        query = query.order_by(asc(tables.TronInfo.updated))
        db_address_info_list = (await self._session.execute(query)).scalars().all()

        result = [models.TronInfoGet.model_validate(db_address_info) for db_address_info in db_address_info_list]

        return result

    async def add_address_info(self, new_tron_data: models.TronInfoCreate) -> models.TronInfoGet:
        """Добавление информации по адресу кошелька TRON"""

        new_address_info = tables.TronInfo(**new_tron_data.model_dump())
        self._session.add(new_address_info)
        await self._session.flush()
        await self._session.refresh(new_address_info)

        return models.TronInfoGet.model_validate(new_address_info)

    async def update_address_info(self, new_tron_data: models.TronInfoCreate) -> models.TronInfoGet:
        """Обновление информации по адресу кошелька"""

        update_query = (
            update(tables.TronInfo)
            .where(tables.TronInfo.address == new_tron_data.address)
            .values(**new_tron_data.model_dump(exclude_unset=True))
        )
        await self._session.execute(update_query)
        await self._session.flush()

        return await self.find_info_by_address(address=new_tron_data.address)
