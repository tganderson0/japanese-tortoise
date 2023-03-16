import requests
from urllib.parse import urlencode
import soundfile as sf
import sounddevice as sd
import time
import discord

# SPEED_SCALE=1
# VOLUME_SCALE=4.0
# INTONATION_SCALE=1.5
# PRE_PHONEME_LENGTH=1.0
# POST_PHONEME_LENGTH=1.0
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

def play_voice(device_id):
    data, fs = sf.read(WAV_FILE, dtype='float32')

    # data = data.reshape((data.shape[0], 1))
    
    # print(data.shape)
    
    sd.play(data, fs, device=device_id)
    sd.wait()


if __name__ == '__main__':
    to_speech('ジェフ、あなたは宿題をするのに忙しいです よくやった', 0)
    # while True:
    play_voice(9)
        # time.sleep(2)