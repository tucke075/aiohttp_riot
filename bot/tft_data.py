import aiohttp
import asyncio
import creds



#PURPOSE: Makes an API call to store the id's associated with the summoner name along with other details such as level
#PARAMS: Is the variable that is being plugged into the API call to search for
async def store_summoner_info(summoner_name):
    summoner_info = []
    async with aiohttp.ClientSession() as session:
        summoner_url = f'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={creds.api_key}' 
        response = await session.get(summoner_url)
        summoner_info = await response.json()
        recent_games = await get_recent_games(summoner_info)

        #return summoner_info
        return recent_games
    
async def get_recent_games(summoner_info):
    games = []
    async with aiohttp.ClientSession() as session:
        puuid = summoner_info['puuid']
        games_url = f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={creds.api_key}'
        response = await session.get(games_url)
        games = await response.json()
        return games


#async def create_puuid_url(puuid):

#asyncio.run(create_urls('rweopunk'))
#print(summoner_info)