import os
import asyncio
import discord
from discord.errors import ClientException
from discord.ext.commands.core import check
import yt_dlp
from discord.ext import commands
from keep_alive import keep_alive


client = commands.Bot(command_prefix="!")

songQueue = []


async def check_queue(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    while voice.is_playing() or voice.is_paused():
        # waits till voice has stopped
        await asyncio.sleep(0)
    if songQueue != []:
        search = songQueue.pop(0)

        await youtube_download(ctx, search)
        source = discord.FFmpegOpusAudio("song.webm")
        voice.play(source)
        await check_queue(ctx)
    else:
        await voice.disconnect()
        await ctx.send("No more audio to play. Disconnected.")


async def youtube_download(ctx, search):
    # Downloads search to song.webm and returns song name
    song_there = os.path.isfile("song.webm")
    if song_there:
        os.remove("song.webm")

    ydl_opts = {
        'default_search': 'auto',
        'format': '249/250/251'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        message = "Currently downloading audio... [Commands will not work]"
        await ctx.send(message)
        ydl.download([search])
        await asyncio.sleep(0)

    for file in os.listdir("./"):
        if file.endswith(".webm"):
            songName = file
            os.rename(file, "song.webm")

    await ctx.send(f'Now Playing: {songName}')


@client.command(pass_context=True)
async def play(ctx, *, search: str):

    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice is not None:
            if voice.is_playing() or voice.is_paused():
                # Adds to queue if already playing
                songQueue.append(search)
                return await ctx.send("Added to queue.")
            else:
                await voice.disconnect()
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    except AttributeError:
        return await ctx.send("Maybe try being in a voice channel mate.")
    except ClientException:
        return

    await youtube_download(ctx, search)
    source = discord.FFmpegOpusAudio("song.webm")
    voice.play(source)
    await check_queue(ctx)


@client.command(pass_context=True)
async def leave(ctx):
    global songQueue
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is not None:
        songQueue = []
        await ctx.send("Cleaned queue.")
        await voice.disconnect()
    else:
        await ctx.send("I'm already gone.")


@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.pause()
            await ctx.send("Audio paused.")
        else:
            await ctx.send("Already paused.")
    except AttributeError:
        return await ctx.send("Bruh, I'm not even in the voice channel.")


@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_paused():
            voice.resume()
            await ctx.send("Audio resumed")
        else:
            await ctx.send("I haven't paused anything.")
    except AttributeError:
        return await ctx.send("Bruh, I'm not even in the voice channel.")


@client.command(pass_context=True)
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing() or voice.is_paused:
            voice.stop()
            await ctx.send("Audio skipped.")
        else:
            await ctx.send("I'm not even playing anything.")
    except AttributeError:
        return await ctx.send("Bruh, I'm not even in the voice channel.")


@client.command(pass_context=True)
async def options(ctx):
    text = """**List of commands:**
    **!play [search]**: Plays audio from youtube video in voice channel
    or adds search to a queue when audio is already playing or paused
    **!pause**: Pauses audio currently playing
    **!resume**: Resumes audio that is paused
    **!skip**: Skips audio that is currently playing or paused
    **!leave**: Forces bot to leave voice channel
    **!options**: Posts list of commands"""
    await ctx.send(text)

keep_alive()

client.run(os.getenv("TOKEN"))
