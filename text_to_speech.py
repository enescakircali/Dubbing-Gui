import os
import json
from elevenlabs import generate, set_api_key, save

def speech(api, file):
    set_api_key(api)

    if not os.path.exists(f"./temp/{os.path.splitext(os.path.basename(file))[0]}"):
        os.makedirs(f"./temp/{os.path.splitext(os.path.basename(file))[0]}")

    with open(f'./temp/{os.path.splitext(os.path.basename(file))[0]}.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for segment in data['segments']:
        audio = generate(
        text=segment["translated_text"],
        voice="Bella",
        model="eleven_multilingual_v2"
        )
        save(audio, f'./temp/{os.path.splitext(os.path.basename(file))[0]}/{segment["id"]}.wav')
    return f"./temp/{os.path.splitext(os.path.basename(file))[0]}"