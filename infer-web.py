import gradio as gr
import argparse
import os
import torch
from locale_load import locale_auto
from video_downloader import download_video, list_video_qualities
from editor import split_function, merge_function
from audio_separator import Separator
from transcription import transcribe
from text_to_speech import speech
from config_manager import ConfigManager

parser = argparse.ArgumentParser()
parser.add_argument("--Share", help="Gives public link", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("--Lang", help="Gives public link")
args = parser.parse_args()

print("Use GPU:", torch.cuda.get_device_name(0))

locale = locale_auto(args.Lang)
locale.print()

manager = ConfigManager()
config = manager.load_config()

# manager.save_config("test","test")

if os.path.exists('./temp'):
    for file in os.listdir('./temp'):
        os.remove(os.path.join('./temp', file))
else:
    os.mkdir('./temp')

if not os.path.exists('./models'):
    os.mkdir('./models')

if not os.path.exists('./models/whisper'):
    os.mkdir('./models/whisper')

vocal_removal_path = './models/vocal_removal'
if not os.path.exists(vocal_removal_path):
    os.mkdir(vocal_removal_path)


def change_tab():
    return gr.Tabs.update(selected=1)

def toggle_dark_mode(btn):
    if btn == "☀️":
        return gr.update(value = "🌙")
    else:
        return gr.update(value = "☀️")

def get_qualities(link):
    qualities = list_video_qualities(link)
    return gr.Radio.update(choices=qualities, value=qualities[0]), gr.update(interactive=True)

def dubbing(video, source_lang, output_lang):
    if config.get("apikey") is None or config.get("apikey") == "":
        raise gr.Error("No API key. Please enter an API key from settings.")
    audio = split_function(video)

    print(audio)
    print("Vocals are being removed")
    separator = Separator(audio, model_name=config.get("Vocal_remover_model"), model_file_dir=vocal_removal_path, output_dir='./temp', use_cuda=True) # log_level='WARNING',
    primary_stem_path, secondary_stem_path = separator.separate()
    print(f'Primary stem saved at {primary_stem_path}')
    print(f'Secondary stem saved at {secondary_stem_path}')

    transcript = transcribe(f"./temp/{primary_stem_path}", model_name=config.get("whisper_model"), source_lang=source_supported_languages[source_lang], output_lang=output_supported_languages[output_lang])

    folder = speech(config.get("apikey"), transcript[0])

    output_video = merge_function(folder, f"./temp/{secondary_stem_path}", video, transcript[0])

    return transcript, output_video

download_btn = gr.Button("Download Video", interactive=False)
video = gr.Video(interactive=True)
dubbing_btn = gr.Button("Dubbing", variant="primary", interactive=False)

source_supported_languages = {
    "Auto": None,
    "🇬🇧 English (English)": "en",
    "🇹🇷 Trukish (Türkçe)": "tr",
    "🇮🇳 Malayalam (മലയാളം)": "ml",
    "🇮🇳 Telugu (తెలుగు)": "te",
    "🇮🇳 hindi (हिंदी)": "hi",
    "🇮🇳 Tamil (தமிழ்)": "ta",
    "🇮🇳 Kannada (ಕನ್ನಡ)": "kn",
    "🇮🇳 Marathi (मराठी)": "mr",
    "🇮🇳 Panjabi (ਪੰਜਾਬੀ)": "pa",
    "🇮🇳 Gujarati (ગુજરાતી)": "gu",
    "🇮🇳 Sanskrit (संस्कृतम्)": "sa",
    "🇮🇳 Assamese (অসমীয়া)": "as",
    "🇩🇪 German (Deutsch)": "de",
    "🇪🇸 Spanish (Español)": "es",
    "🇷🇺 Russian (Русский)": "ru",
    "🇰🇷 Korean (한국어)": "ko",
    "🇫🇷 French (Français)": "fr",
    "🇯🇵 Japanese (日本語)": "ja",
    "🇵🇹 Portuguese (Português)": "pt",
    "🇵🇱 Polish (Polski)": "pl",
    "🇨🇦 Catalan (Català)": "ca",
    "🇳🇱 Dutch (Nederlands)": "nl",
    "🇸🇦 Arabic (العربية)": "ar",
    "🇸🇪 Swedish (Svenska)": "sv",
    "🇮🇹 Italian (Italiano)": "it",
    "🇮🇩 Indonesian (Bahasa Indonesia)": "id",
    "🇫🇮 Finnish (Suomi)": "fi",
    "🇻🇳 Vietnamese (Tiếng Việt)": "vi",
    "🇮🇱 Hebrew (עִבְרִית)": "he",
    "🇺🇦 Ukrainian (Українська)": "uk",
    "🇬🇷 Greek (Ελληνικά)": "el",
    "🇲🇾 Malay (Bahasa Melayu)": "ms",
    "🇨🇿 Czech (Čeština)": "cs",
    "🇷🇴 Romanian (Română)": "ro",
    "🇩🇰 Danish (Dansk)": "da",
    "🇭🇺 Hungarian (Magyar)": "hu",
    "🇳🇴 Norwegian (Norsk)": "no",
    "🇹🇭 Thai (ไทย)": "th",
    "🇺🇷 Urdu (اردو)": "ur",
    "🇭🇷 Croatian (Hrvatski)": "hr",
    "🇧🇬 Bulgarian (Български)": "bg",
    "🇱🇹 Lithuanian (Lietuvių)": "lt",
    "🇱🇻 Latvian (Latviešu)": "lv",
    "🇧🇩 Bengali (বাংলা)": "bn",
    "🇷🇸 Serbian (Српски)": "sr",
    "🇦🇿 Azerbaijani (Azərbaycanca)": "az",
    "🇸🇮 Slovenian (Slovenščina)": "sl",
    "🇪🇪 Estonian (Eesti)": "et",
    "🇲🇰 Macedonian (Македонски)": "mk",
    "🇫🇷 Breton (Brezhoneg)": "br",
    "🇪🇸 Basque (Euskara)": "eu",
    "🇮🇸 Icelandic (Íslenska)": "is",
    "🇦🇲 Armenian (Հայերեն)": "hy",
    "🇳🇵 Nepali (नेपाली)": "ne",
    "🇲🇳 Mongolian (Монгол)": "mn",
    "🇧🇦 Bosnian (Bosanski)": "bs",
    "🇰🇿 Kazakh (Қазақ)": "kk",
    "🇦🇱 Albanian (Shqip)": "sq",
    "🇸🇼 Swahili (Kiswahili)": "sw",
    "🇪🇸 Galician (Galego)": "gl",
    "🇱🇰 Sinhala (සිංහල)": "si",
    "🇰🇭 Khmer (ភាសាខ្មែរ)": "km",
    "🇿🇼 Shona (ChiShona)": "sn",
    "🇾🇪 Yoruba (Yorùbá)": "yo",
    "🇸🇴 Somali (Soomaali)": "so",
    "🇿🇦 Afrikaans (Afrikaans)": "af",
    "🇫🇷 Occitan (Occitan)": "oc",
    "🇬🇪 Georgian (ქართული)": "ka",
    "🇧🇾 Belarusian (Беларуская)": "be",
    "🇹🇯 Tajik (Тоҷикӣ)": "tg",
    "🇸🇳 Sindhi (سنڌي)": "sd",
    "🇪🇹 Amharic (አማርኛ)": "am",
    "🇾🇪 Yiddish (ייִדיש)": "yi",
    "🇱🇦 Lao (ລາວ)": "lo",
    "🇺🇿 Uzbek (Oʻzbekcha)": "uz",
    "🇫🇴 Faroese (Føroyskt)": "fo",
    "🇭🇹 Haitian (Kreyòl Ayisyen)": "ht",
    "🇵🇰 Pashto (پښتو)": "ps",
    "🇹🇲 Turkmen (Türkmençe)": "tk",
    "🇳🇴 Norwegian Nynorsk (Nynorsk)": "nn",
    "🇲🇹 Maltese (Malti)": "mt",
    "🇱🇺 Luxembourgish (Lëtzebuergesch)": "lb",
    "🇲🇲 Burmese (မြန်မာ)": "my",
    "🇹🇬 Tibetan (བོད་སྐད)": "bo",
    "🇵🇭 Tagalog (Tagalog)": "tl",
    "🇲🇬 Malagasy (Malagasy)": "mg",
    "🇹🇲 Tatar (Татарча)": "tt",
    "🏴󠁵󠁳󠁨󠁩󠁿 Hawaiian (ʻŌlelo Hawaiʻi)": "haw",
    "🇨🇬 Lingala (Lingála)": "ln",
    "🇳🇬 Hausa (Hausa)": "ha",
    "🇷🇺 Bashkir (Башҡорт)": "ba",
    "🇮🇩 Sundanese (Basa Sunda)": "su",
    "🇨🇳 Chinese (中文)": "zh"
}

output_supported_languages = {
    "🇬🇧 English (English)": "en",
    "🇹🇷 Turkish (Türkçe)": "tr",
    "🇮🇳 Tamil (தமிழ்)": "ta",
    "🇮🇳 Hindi (हिंदी)": "hi",
    "🇮🇳 Malay (Bahasa Melayu)": "ms",
    "🇪🇸 Spanish (Español)": "es",
    "🇵🇹 Portuguese (Português)": "pt",
    "🇫🇷 French (Français)": "fr",
    "🇩🇪 German (Deutsch)": "de",
    "🇯🇵 Japanese (日本語)": "ja",
    "🇸🇦 Arabic (العربية)": "ar",
    "🇰🇷 Korean (한국어)": "ko",
    "🇮🇩 Indonesian (Bahasa Indonesia)": "id",
    "🇮🇹 Italian (Italiano)": "it",
    "🇳🇱 Dutch (Nederlands)": "nl",
    "🇵🇱 Polish (Polski)": "pl",
    "🇸🇪 Swedish (Svenska)": "sv",
    "🇵🇭 Filipino (Tagalog)": "tl",
    "🇷🇴 Romanian (Română)": "ro",
    "🇺🇦 Ukrainian (Українська)": "uk",
    "🇬🇷 Greek (Ελληνικά)": "el",
    "🇨🇿 Czech (Čeština)": "cs",
    "🇩🇰 Danish (Dansk)": "da",
    "🇫🇮 Finnish (Suomi)": "fi",
    "🇧🇬 Bulgarian (Български)": "bg",
    "🇭🇷 Croatian (Hrvatski)": "hr",
    "🇸🇰 Slovak (Slovenčina)": "sk",
    "🇨🇳 Chinese (中文)": "zh"
}


video2 = gr.Video(label="Dubbed Video", interactive=False)
file = gr.File(label="Subtitle", file_types=[".srt", ".vtt"], interactive=False)

with gr.Blocks(theme='enescakircali/Indian-Henna', css=".small_btn {margin: 0.6em 0em 0.55em 0; max-width: 2.5em; min-width: 2.5em !important; height: 2.4em;} footer {visibility: hidden}") as menu:
    gr.Markdown("# Start typing below and then click **Run** to see the output.")
    with gr.Tabs() as tabs:
        with gr.TabItem(label="Download/Uploud", id=0):
            with gr.Column():
                with gr.Row():
                    link = gr.Textbox(show_label=False, placeholder="YouTube Link")
                    button = gr.Button("List the Qualities")
            with gr.Row():
                    radio = gr.Radio(label="Quality", interactive=True)
                    link.submit(get_qualities, inputs=[link], outputs=[radio, download_btn])
                    button.click(get_qualities, inputs=[link], outputs=[radio, download_btn])
                    link.change(lambda: gr.Radio.update(choices=[]), outputs=[radio])
                    link.change(lambda: gr.update(interactive=False), outputs=[download_btn])
                    download_btn.render()
                    download_btn.click(download_video, inputs=[link, radio], outputs=[video])
            video.render()
            video.change(fn=lambda key: gr.update(interactive=key is not None), inputs=[video], outputs=[dubbing_btn])
            with gr.Row():
                source_lang = gr.Dropdown(choices=list(source_supported_languages.keys()), value="Auto", label="Source Language")
                output_lang = gr.Dropdown(choices=list(output_supported_languages.keys()), value="🇬🇧 English (English)", label="Output Language")
                dubbing_btn.render()
                dubbing_btn.click(change_tab, None, tabs)
                dubbing_btn.click(dubbing, inputs=[video, source_lang, output_lang], outputs=[file, video2])
        with gr.TabItem(label="Timeline", id=1):
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        gr.Markdown("Original")
                        gr.Markdown("Translated")
                    with gr.Row():
                        inp = gr.TextArea(show_label=False)
                        out = gr.TextArea(show_label=False)
                with gr.Column():
                    video2.render()
                    file.render()
        with gr.TabItem(label="Settings", id=2):
            with gr.Row():
                dark_mode = gr.Button("🌙", elem_classes="small_btn")
                dark_mode.click(toggle_dark_mode, dark_mode, dark_mode)
                dark_mode.click(None, _js="() => { document.body.classList.toggle('dark'); }")
                donate = gr.Button("☕️", elem_classes="small_btn")
                donate.click(None, _js="() => { window.open('https://www.buymeacoffee.com/enescakircali', 'Donate'); }")
            with gr.Row():
                apikey = gr.Textbox(show_label=False, value=config.get("apikey"), placeholder="Elevenlabs Apikey")
                apikey_btn = gr.Button("Get Apikey")
                apikey_btn.click(None, _js="() => { window.open('https://elevenlabs.io/speech-synthesis', 'Apikey'); }") # 4ef495196d73410e695921df3d790c80
            whisper_model = gr.Dropdown(choices=["tiny", "base", "small", "medium", "large", "large-v2"], value=config.get("whisper_model"), label="Whisper Model (Choose your model according to VRAM)")
            Vocal_remover_model = gr.Dropdown(choices=["Kim_Vocal_1", "Kim_Vocal_2"], value=config.get("Vocal_remover_model"), label="Vocal Remover Model (Kim Vocal model recommended)")
            btn = gr.Button("Save Settings")
            btn.click(fn=lambda key,key2,key3: manager.save_config({"apikey":key, "whisper_model":key2, "Vocal_remover_model":key3}), inputs=[apikey,whisper_model,Vocal_remover_model])
            btn.click(lambda: gr.Info('Your settings have been saved'))

menu.queue().launch(share=args.Share)