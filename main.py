import aiohttp
import asyncio


from core.checker import run_checker
from fake_useragent import UserAgent
from loguru import logger
from os import mkdir
from os.path import exists


logger.remove()
logger.add("layerzero.log",
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
           level="INFO",
           colorize=True)


async def main():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            verify_ssl=None,
            ssl=False,
            use_dns_cache=False,
            ttl_dns_cache=300,
            limit=None
        ),
        headers={
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "referrer": "https://www.layerzero.foundation/eligibility/",
            "content-type": "application/json",
            "user-agent": UserAgent().random
        }
    ) as client:
        tasks: list[asyncio.Task] = [
            asyncio.create_task(run_checker(client=client, address=address))
            for address in wallets
        ]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    if not exists("results"):
        mkdir("results")

    print(f"LayerZero Checker made by | munchen\n"
          f"Telegram Channel: https://t.me/lifechange_drops\n")

    with open(file="wallets.txt", mode="r", encoding="utf-8") as file:
        wallets = [row.rstrip() for row in file]

    if not wallets:
        logger.error("Wallets have not been found in wallets.txt")
        exit(1)

    logger.success(f"Found {len(wallets)} wallets in wallets.txt")
    print(f"Found {len(wallets)} wallets in wallets.txt\n")

    asyncio.run(main())

    print(f"Successfully checked {len(wallets)} wallets!\n")
    input("Press Enter to exit...")
