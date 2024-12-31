import discord
from discord.ext import commands, tasks
from config import BOT_PREFIX
from animemanga import fetch_anime_info, fetch_manga_info, create_anime_embed, create_manga_embed
from storage import save_channel, get_channel

# Import setup untuk command info
from server import setup as setup_info

# Load bot token
with open('bot_token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Mengatur intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    check_new_episodes.start()

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

@bot.command(name='setnotif')
@commands.has_permissions(administrator=True)
async def setnotif(ctx, channel: discord.TextChannel):
    save_channel(str(ctx.guild.id), channel.id)
    await ctx.send(f'Notifikasi akan dikirim ke {channel.mention}.')

@tasks.loop(hours=1)
async def check_new_episodes():
    for guild in bot.guilds:
        channel_id = get_channel(str(guild.id))
        if channel_id:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send("Checking for new episodes...")  # Implementasikan logika notifikasi di sini

# Menambahkan command info
setup_info(bot)

bot.run(TOKEN)