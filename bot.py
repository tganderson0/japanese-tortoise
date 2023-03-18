import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import requests
from urllib.parse import urlencode
import soundfile as sf
import sounddevice as sd
import asyncio

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

WAV_FILE = 'output.wav'

def create_route(route):
    return f'http://localhost:50021{route}'

def to_speech(text, speaker):
    params_encoded = urlencode({'text': text, 'speaker': speaker})
    payload = requests.post(create_route(f'/audio_query?{params_encoded}'))
    payload = payload.json()
    params_encoded = urlencode({'speaker': speaker})
    query = requests.post(create_route(f'/synthesis?{params_encoded}'), json=payload)
    with open(WAV_FILE, 'wb') as outfile:
        outfile.write(query.content)

def translate_en_to_jp(message):
    r = requests.post('http://127.0.0.1:5000/translate', json={
    'q': message,
    'source': 'auto',
    'target': 'ja',
    'format': 'text',
    'api_key': ''
    })

    return r.json()['translatedText']

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to discord!")

@bot.command(name="translate", help="Format: <!speak voice message...> Try 42 for a sexy guy")
async def translate(ctx, voice=None, *, sentence=None):
    if voice is None:
        await ctx.reply(f"You need to supply a voice")
        return
    try:
        int(voice)
    except:
        await ctx.reply("Voice needs to be an integer")
        return
    if sentence is None:
        await ctx.reply("Crickets are chirping...")
        return
    try:
        translated_sentence = translate_en_to_jp(sentence)
        to_speech(translated_sentence, voice)
    except:
        await ctx.reply(f"Voice {voice} is not a valid option- try a lower number")
        return
    
    bot_voice = ctx.guild.voice_client
    author_voice = ctx.author.voice
    
    if bot_voice and bot_voice.is_connected():
        await bot_voice.move_to(author_voice.channel)
    elif author_voice and not bot_voice:
        bot_voice = await author_voice.channel.connect()
    elif not author_voice:
        await ctx.reply("You must be in a voice channel")
        return

    if bot_voice.is_playing():
        bot_voice.stop()
    bot_voice.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=WAV_FILE))
    
    # await asyncio.sleep(300)
    # await bot_voice.disconnect()

bot.run(TOKEN)