from moviepy.editor import *
import os
import json

def split_function(video):
    if not os.path.isfile(f"./temp/{os.path.splitext(os.path.basename(video))[0]}.wav"):
        clip = VideoFileClip(video)
        clip.audio.write_audiofile(f"./temp/{os.path.splitext(os.path.basename(video))[0]}.wav", codec='pcm_s16le', write_logfile=False, logger=None)
        clip.close()
        return f"./temp/{os.path.splitext(os.path.basename(video))[0]}.wav"
    else:
        return f"./temp/{os.path.splitext(os.path.basename(video))[0]}.wav"

def merge_function(folder, background_audio_path, video, file):
    audios = []
    output_video = VideoFileClip(video)
    background_audio = AudioFileClip(background_audio_path)
    audios.append(background_audio)
    with open(f'./temp/{os.path.splitext(os.path.basename(file))[0]}.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for segment in data['segments']:
        start_time = segment['start']
        end_time = segment['end']
        audio_id = segment['id']

        audio = AudioFileClip(f'{folder}/{audio_id}.wav')

        audio = audio.set_start(start_time)
        audios.append(audio)

    output_video.audio = CompositeAudioClip(audios)
    output_video.write_videofile(f'./temp/{os.path.splitext(os.path.basename(video))[0]}_output.mp4', fps=output_video.fps)
    output_video.close()
    background_audio.close()
    return f'./temp/{os.path.splitext(os.path.basename(video))[0]}_output.mp4'