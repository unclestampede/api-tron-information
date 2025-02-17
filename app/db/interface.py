from abc import ABC, abstractmethod
from typing import List, Optional

from app import models


class DBFacadeInterface(ABC):
    """Интерфейс для работы с базой данных"""

    @abstractmethod
    async def commit(self) -> None:
        """Commit изменений"""

    @abstractmethod
    async def is_db_alive(self) -> bool:
        """Проверка работы БД"""

    @abstractmethod
    async def get_address_count(self, address_list: Optional[List[str]]) -> int:
        """Получение количества адресов TRON"""

    @abstractmethod
    async def find_info_by_address(self, address: str) -> Optional[models.TronInfoGet]:
        """Поиск информации о кошельке по адресу TRON"""

    @abstractmethod
    async def get_multiple_address_info(
        self, address_list: Optional[List[str]], limit: int, offset: int
    ) -> List[models.TronInfoGet]:
        """Получение списка данных по кошелькам TRON"""

    @abstractmethod
    async def add_address_info(self, new_tron_data: models.TronInfoCreate) -> models.TronInfoGet:
        """Добавление информации по адресу кошелька TRON"""

    @abstractmethod
    async def update_address_info(self, new_tron_data: models.TronInfoCreate) -> models.TronInfoGet:
        """Обновление информации по адресу кошелька"""
