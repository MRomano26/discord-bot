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

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I'm already gone.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("I'm not even playing something.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("I haven't paused anything.")
    
client.run("TOKEN")