import pytest
from httpx import AsyncClient

from tests import test_data


class TestTron:
    @pytest.mark.asyncio
    async def test_add_address_info(self, client: AsyncClient) -> None:
        response = await client.post(f"/tron/{test_data.ADDRESS_EXAMPLE}/information")
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_add_updated_address_info(self, client: AsyncClient) -> None:
        response = await client.post(f"/tron/{test_data.ADDRESS_EXAMPLE}/information")
        assert response.status_code == 201
        response = await client.post(f"/tron/{test_data.ADDRESS_EXAMPLE}/information")
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_add_address_info_not_exist(self, client: AsyncClient) -> None:
        response = await client.post(f"/tron/{test_data.NOT_EXIST_ADDRESS_EXAMPLE}/information")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_add_invalid_address_info(self, client: AsyncClient) -> None:
        response = await client.post(f"/tron/{test_data.INVALID_ADDRESS_EXAMPLE}/information")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_multiple_address_info(self, client: AsyncClient) -> None:
        response = await client.get("/tron/information")
        assert response.status_code == 200

        assert len(response.json()) == 0

    @pytest.mark.asyncio
    async def test_get_one_address_info(self, client: AsyncClient) -> None:
        response = await client.post(f"/tron/{test_data.ADDRESS_EXAMPLE}/information")
        assert response.status_code == 201

        response = await client.get("/tron/information", params={"limit": 1})
        assert response.status_code == 200

        assert len(response.json()) == 1
