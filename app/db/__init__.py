from fastapi import Depends

from app.db.facade import DBFacade
from app.db.interface import DBFacadeInterface


def get_db_facade(db_facade: DBFacade = Depends(DBFacade)) -> DBFacadeInterface:
    """Зависимость для получения фасада БД"""
    return db_facade
