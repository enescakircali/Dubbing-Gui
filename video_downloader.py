import yt_dlp
import sys
import re
import gradio as gr

def download_video(url, resolution, pr=gr.Progress()):
    def format_title(title):
        formatted_title = re.sub(r"[^\w\s-]", "", title)
        formatted_title = formatted_title.replace(" ", "_")
        return formatted_title

    def callable_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            current = downloaded_bytes / total_bytes if total_bytes > 0 else 0
            progress = int(50 * current)
            status = '█' * progress + ' ' * (50 - progress)
        
            downloaded_size = f'{downloaded_bytes / (1024 * 1024):.2f} MB'
            total_size = f'{total_bytes / (1024 * 1024):.2f} MB'

            pr(current, desc="Downloading Video")

            sys.stdout.write(f'\rDownloading: {current * 100:.1f}%|{status}| [{total_size} / {downloaded_size}]\r')
            sys.stdout.flush()
        elif d['status'] == 'finished':
            print(f"\n{d.get('info_dict').get('fulltitle')} download completed.")

    video_opts = {
        'format': f'bestvideo[height<={resolution.replace("p","")}]',
        "no-windows-filenames": True,
        "restrict-filenames": True,
        'quiet': True,
        "no-warnings": True,
        'progress_hooks': [callable_hook],
    }

    audio_opts = {
    'format': 'bestaudio/best',
    "no-windows-filenames": True,
    "restrict-filenames": True,
    'quiet': True,
    "no-warnings": True,
    'progress_hooks': [callable_hook],
    }


    with yt_dlp.YoutubeDL(video_opts) as ydl_video:
        info_dict = ydl_video.extract_info(url, download=False)
        video_opts["outtmpl"] = f'./temp/{format_title(info_dict.get("title", "default_title"))}.{info_dict["ext"]}'
        ydl_video = yt_dlp.YoutubeDL(video_opts)
        ydl_video.download([url])
        video_path = './temp/'+format_title(info_dict.get("title", "default_title"))+f'.{info_dict["ext"]}'

    with yt_dlp.YoutubeDL(audio_opts) as ydl_audio:
        info_dict = ydl_audio.extract_info(url, download=False)
        audio_opts["outtmpl"] = f'./temp/{format_title(info_dict.get("title", "default_title"))}.wav'
        ydl_audio = yt_dlp.YoutubeDL(audio_opts)
        ydl_audio.download([url])
        audio_path = './temp/'+format_title(info_dict.get("title", "default_title"))+f'.wav'

    return video_path

def list_video_qualities(url):
    ydl_opts = {
        'quiet': True
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    try:
        info_dict = ydl.extract_info(url, download=False)
        
        if 'entries' in info_dict:
            video_info = info_dict['entries'][0]
        else:
            video_info = info_dict

        if 'formats' in video_info:
            video_formats = [format for format in video_info['formats'] if format.get('ext') == 'mp4']
            qualities = list(set([f"{format['height']}p" for format in video_formats if format.get('height')]))
            qualities.sort(key=lambda x: int(x.split('p')[0]), reverse=True)
            return qualities
        else:
            return []

    except yt_dlp.DownloadError as e:
        print(f"Error: {e}")
        return []
