import whisper
import os
import json
from deep_translator import GoogleTranslator
from whisper.utils import get_writer

def transcribe(audio, model_name="large-v2", source_lang=None, output_lang="en"):
  model = whisper.load_model(model_name, download_root="./models/whisper")
  whisper.DecodingOptions(language=source_lang, fp16='false')
  result = model.transcribe(audio)

  word_options = {
  "highlight_words": True,
  "max_line_count": 50,
  "max_line_width": 3
  }

  # Save as an JSON file
  json_writer = get_writer("json", "./temp")
  json_writer(result, audio, word_options)
  
  # Read the given JSON data
  with open(f'./temp/{os.path.splitext(os.path.basename(audio))[0]}.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

  # Translate each segment
  for segment in data['segments']:
    original_text = segment['text']
    segment['translated_text'] = GoogleTranslator(source='auto', target=output_lang).translate(original_text)

  # Write the translated JSON data
  with open(f'./temp/{os.path.splitext(os.path.basename(audio))[0]}.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

  # Save as an SRT file
  srt_writer = get_writer("srt", "./temp")
  srt_writer(result, audio, word_options)

  # Save as a VTT file
  vtt_writer = get_writer("vtt", "./temp")
  vtt_writer(result, audio, word_options)

  return [f"./temp/{os.path.splitext(os.path.basename(audio))[0]}.srt", f"./temp/{os.path.splitext(os.path.basename(audio))[0]}.vtt"]