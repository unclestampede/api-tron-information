import pytest

from app.db.interface import DBFacadeInterface
from tests import test_data


class TestTronDB:
    @pytest.mark.asyncio
    async def test_add_address_info(self, db_facade: DBFacadeInterface) -> None:
        address_info = await db_facade.add_address_info(new_tron_data=test_data.ADD_INFO_EXAMPLE)
        assert address_info.address == test_data.ADD_INFO_EXAMPLE.address
        assert address_info.balance == test_data.ADD_INFO_EXAMPLE.balance
        assert address_info.energy == test_data.ADD_INFO_EXAMPLE.energy
        assert address_info.bandwidth == test_data.ADD_INFO_EXAMPLE.bandwidth

    @pytest.mark.asyncio
    async def test_get_address_info(self, db_facade: DBFacadeInterface) -> None:
        added_address_info = await db_facade.add_address_info(new_tron_data=test_data.ADD_INFO_EXAMPLE)
        received_address_info = await db_facade.get_multiple_address_info(
            address_list=[test_data.ADD_INFO_EXAMPLE.address], limit=1000, offset=0
        )

        assert added_address_info == received_address_info[0]

    @pytest.mark.asyncio
    async def test_get_address_count(self, db_facade: DBFacadeInterface) -> None:
        received_address_info = await db_facade.get_multiple_address_info(address_list=[], limit=1000, offset=0)
        address_count = await db_facade.get_address_count(address_list=None)

        assert len(received_address_info) == address_count
