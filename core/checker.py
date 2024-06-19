import aiohttp
import asyncio


from loguru import logger
from utils.append_file import append_file


async def check_eligibility(client: aiohttp.ClientSession,
                            address: str):
    url = f"https://www.layerzero.foundation/api/allocation"
    try:
        response: aiohttp.ClientResponse = await client.get(
            url=f"{url}/{address}"
        )
        response_json = await response.json()

        if "isEligible" in response_json:
            token_amount = response_json["zroAllocation"]["asString"]
            logger.success(f"Eligible for {token_amount} $ZRO: {address}")
            async with asyncio.Lock():
                await append_file(
                    file_path="results/eligible.txt",
                    file_content=f"Eligible for {token_amount} $ZRO: {address}\n"
                )
        else:
            logger.info(f"Not eligible: {address}")
            async with asyncio.Lock():
                await append_file(
                    file_path="results/not_eligible.txt",
                    file_content=f"Not eligible: {address}\n"
                )

    except Exception as error:
        logger.error(f"While checking error has been occurred: {error}")


async def run_checker(client: aiohttp.ClientSession, address: str):
    await check_eligibility(client=client, address=address)
