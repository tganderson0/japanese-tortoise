import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import requests
from urllib.parse import urlencode
import soundfile as sf
import sounddevice as sd

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
    # payload['speedScale'] = SPEED_SCALE
    # payload['volumeScale'] = VOLUME_SCALE
    # payload['intonationScale'] = INTONATION_SCALE
    # payload['prePhonemeLength'] = PRE_PHONEME_LENGTH
    # payload['postPhonemeLength'] = POST_PHONEME_LENGTH
    params_encoded = urlencode({'speaker': speaker})
    query = requests.post(create_route(f'/synthesis?{params_encoded}'), json=payload)
    with open(WAV_FILE, 'wb') as outfile:
        outfile.write(query.content)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to discord!")

@bot.command(name="translate", help="Connects to general voice and speaks the sentance in japanese")
async def translate(ctx, *, sentence):
    to_speech(sentence, 24)
    voicechannel = discord.utils.get(ctx.guild.channels, name="Lobby")
    
    bot_voice = ctx.guild.voice_client
    author_voice = ctx.author.voice
    
    if bot_voice and bot_voice.is_connected():
        await bot_voice.move_to(author_voice.channel)
    elif author_voice and not bot_voice:
        bot_voice = await author_voice.channel.connect()
    elif not author_voice:
        await ctx.send("You must be in a voice channel")
        return

    bot_voice.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=WAV_FILE))

bot.run(TOKEN)