import discord
from discord.ext import commands
from config import BOT_PREFIX
from animemanga import fetch_anime_info, create_anime_embed, fetch_manga_info, create_manga_embed
from database import initialize_database, save_command
from info import info
# Load bot token
with open('bot_token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Mengatur intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Initialize the database
initialize_database()

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.event
async def on_command(ctx):
    save_command(str(ctx.author.id), ctx.command.name)

@bot.command(name='anime')
async def anime(ctx, *, title: str):
    data = fetch_anime_info(title)
    if data:
        embed = create_anime_embed(data)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Anime not found.")

@bot.command(name='manga')
async def manga(ctx, *, title: str):
    data = fetch_manga_info(title)
    if data:
        embed = create_manga_embed(data)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Manga not found.")

 
@bot.command(name='info')
async def info_command(ctx):
    await info(ctx)

bot.run(TOKEN)
