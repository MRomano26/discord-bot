import os
import discord
from discord.ext import commands


client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):
    try:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    except AttributeError:
        return await ctx.send("Maybe try being in a channel mate.")

client.run("TOKEN")