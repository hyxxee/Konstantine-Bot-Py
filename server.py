import psutil
import discord
from discord.ext import commands

@commands.command(name='info')
async def info(ctx):
    # Mendapatkan informasi CPU dan RAM
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent

    # Mendapatkan suhu CPU (opsional, hanya bekerja jika perangkat mendukung)
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else "N/A"
    except Exception:
        cpu_temp = "N/A"

    # Membuat embed untuk ditampilkan
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=False)
    embed.add_field(name="RAM Usage", value=f"{ram_usage}%", inline=False)
    embed.add_field(name="CPU Temperature", value=f"{cpu_temp}°C", inline=False)
    embed.set_footer(text="Requested by " + ctx.author.name, icon_url=ctx.author.avatar.url)

    # Mengirimkan embed
    await ctx.send(embed=embed)

# Fungsi untuk menambahkan command ke bot
def setup(bot):
    bot.add_command(info)
