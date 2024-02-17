import discord
import creds as creds
from tft_data import store_summoner_info
from discord.ext import commands

#initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
    print('Ready')
    print('-------------')


@bot.command()
async def check(ctx, *, summoner_name: str):
    #await ctx.send("Hi")
    data = await store_summoner_info(summoner_name)
    await ctx.send(data)

bot.run(f'{creds.token}')


