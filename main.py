import os
import discord
from discord.errors import ClientException
import yt_dlp
from discord.ext import commands
from keep_alive import keep_alive


client = commands.Bot(command_prefix="!")


@client.command()
async def play(ctx, url: str):

    try:
        voiceChannel = ctx.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice is not None:
            await voice.disconnect()
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    except AttributeError:
        return await ctx.send("Maybe try being in a voice channel mate.")
    except ClientException:
        return

    song_there = os.path.isfile("song.webm")
    if song_there:
        os.remove("song.webm")

    ydl_opts = {
        'default_search': 'auto',
        'format': '249/250/251'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
    voice.play(discord.FFmpegOpusAudio("song.webm"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        await voice.disconnect()
    else:
        await ctx.send("I'm already gone.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Already paused.")
    except AttributeError:
        return await ctx.send("Bruh, I'm not even in the voice channel.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("I haven't paused anything.")
    except AttributeError:
        return await ctx.send("Bruh, I'm not even in the voice channel.")

keep_alive()
client.run("OTA4NDczMTg5NTE5MjIwNzM2.YY2Plg.dHszeKQlKCW_i_Ttkz9fpbHeJ1M")
# client.run(os.getenv("TOKEN"))
