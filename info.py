# info.py
import discord
from discord.ext import commands
import psutil

# Fungsi untuk command info
async def info(ctx):
    # Get CPU usage information
    cpu_usage = psutil.cpu_percent(interval=1)  # Gets CPU usage in percentage
    cpu_temperature = None
    try:
        # Try to get CPU temperature if available
        cpu_temperature = psutil.sensors_temperatures().get('coretemp', [])
        if cpu_temperature:
            cpu_temperature = cpu_temperature[0].current
    except Exception as e:
        cpu_temperature = "N/A"

    # Get RAM usage information
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total / (1024 ** 3)  # Convert from bytes to GB
    used_ram = ram_info.used / (1024 ** 3)  # Convert from bytes to GB
    ram_percentage = ram_info.percent

    # Create the embed with the information
    embed = discord.Embed(title="System Information", color=discord.Color.blue())
    embed.add_field(name="CPU Usage", value=f"{cpu_usage}%")
    embed.add_field(name="CPU Temperature", value=f"{cpu_temperature}°C" if cpu_temperature != "N/A" else "N/A")
    embed.add_field(name="Memory Usage", value=f"{used_ram:.2f} GB / {total_ram:.2f} GB ({ram_percentage}%)")
    
    # Send the embed
    await ctx.send(embed=embed)