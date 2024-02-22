import aiohttp
#import asyncio
import creds



#PURPOSE: Makes an API call to store the id's associated with the summoner name along with other details such as level
#PARAMS: Is the variable that is being plugged into the API call to search for
async def store_summoner_info(summoner_name):
    summoner_info = []
    async with aiohttp.ClientSession() as session:
        summoner_url = f'https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={creds.api_key}' 
        response = await session.get(summoner_url)
        summoner_info = await response.json()
        worst_game = await get_recent_games(summoner_info)
        return worst_game
    
async def get_recent_games(summoner_info):
    games = []
    async with aiohttp.ClientSession() as session:
        puuid = summoner_info['puuid']
        games_url = f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={creds.api_key}'
        response = await session.get(games_url)
        games = await response.json()
        bad_games = await store_bad_games(games,puuid)
        formatted_game = await format_game(bad_games)
        return formatted_game
    
async def store_bad_games(games,puuid):
    bad_games = []
    async with aiohttp.ClientSession() as session:
        for game in games:
            #make an api call for each game 
            match_id = game
            current_match_url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={creds.api_key}'
            async with session.get(current_match_url) as response:
                response = await session.get(current_match_url)
                if response.status == 200:
                    response = await response.json()
                    game_info = response['info']
                    for participant in game_info['participants']:
                        if participant['puuid'] == puuid and participant['placement'] >= 5:
                            
                            important_info = {
                                'match_id': match_id,
                                'puuid' : puuid,
                                'placement' : participant['placement'],
                                'augments': participant.get('augments', []),
                                'game_info': {
                                    'endOfGameResult': game_info['endOfGameResult'],
                                    'game_datetime': game_info['game_datetime'],
                                    'game_length': game_info['game_length'],
                                    'game_version': game_info['game_version'],
                                }
                                #'participant_info': participant
                            }
                            bad_games.append(important_info)
        #should have list of all the placements >5 saved from recent 20 games
        #check the worst of it
        #any 8th will work for now
        for bad_game in bad_games:
            if puuid == bad_game['puuid']:
                if bad_game['placement'] == 8:
                    worst_game = bad_game
                elif bad_game['placement'] == 7:
                    worst_game = bad_game
                elif bad_game['placement'] == 6:
                    worst_game = bad_game
                elif bad_game['placement'] == 5:
                    worst_game = bad_game             
    return worst_game


async def format_game(game):
    formatted_info = []
    placement_val = str(game['placement'])
    augments_val = ', '.join(game['augments'])
    game_info = f"Placement: {placement_val}, your augments were {augments_val}"
    formatted_info.append(game_info)
    return formatted_info

            



            
            



#async def create_puuid_url(puuid):

#asyncio.run(create_urls('rweopunk'))
#print(summoner_info)