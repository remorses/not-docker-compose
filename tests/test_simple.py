from .support import *
from src.main import up



@pytest.mark.asyncio
async def test_main():
    await up()