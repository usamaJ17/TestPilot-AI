import os
import atexit
import asyncio
import yaml
import time
from config_loader import load_and_create_config
from logs_loader import ensure_logs_file

ensure_logs_file()
config_path = load_and_create_config()

from fast import fast
from agents import manual_agent, wdio_agent


def cleanup():
    if os.path.exists(config_path):
        os.remove(config_path)


atexit.register(cleanup)


async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
