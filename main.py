import os
import discord
from discord import voice_client
from discord.ext import commands


client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):
    try:
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice.is_connected():
            await voiceChannel.connect()
    except AttributeError:
        return await ctx.send("Maybe try being in a channel mate.")
    # we'll add music playing functionality later

client.run("TOKEN")