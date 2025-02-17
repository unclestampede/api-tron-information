from tronpy import AsyncTron

from app import settings


async def get_tron_session() -> AsyncTron:
    async with AsyncTron(network=settings.NETWORK) as tron_session:
        yield tron_session
