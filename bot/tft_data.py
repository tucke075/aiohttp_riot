import aiohttp
import asyncio
import creds

summoner_info = []
async def create_urls(summoner_name):
    async with aiohttp.ClientSession() as session:
        summoner_url = f'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={creds.api_key}' 
        response = await session.get(summoner_url)
        summoner_info.append(await response.json())
        return summoner_info
    


#async def create_puuid_url(puuid):

asyncio.run(create_urls('rweopunk'))
#print(summoner_info)