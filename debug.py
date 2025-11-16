import aiohttp
import asyncio

async def main(): 
    async with aiohttp.ClientSession() as session:
            async with session.get(f'https://{input()}') as resp:
                print(resp.status)

asyncio.run(main())
