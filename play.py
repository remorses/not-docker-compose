import asyncio
import fire
import time
from src.exec import exec


async def amain():
    await asyncio.gather(
        exec('sleep 3 && echo end'),
        exec('sleep 4 && echo end && echo end && echo end'),
        exec('sleep 2 && echo end && echo end'),
        exec('sleep 1 && echo end'),
    )

def main():
    s = time.time()
    asyncio.run(amain())
    e = time.time()
    print(f'{(e - s)} secs')

fire.Fire(main)