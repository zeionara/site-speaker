import os
import time
import traceback
import wave
from urllib.request import Request, urlopen

from pydub import AudioSegment

from site_speaker.utils.files import get_extension, replace_extension, read_as_text
from site_speaker.utils.string import normalize_spaces, stringify_number
from site_speaker.utils.text import split_text

HEADERS = {
    'Host': 'cloud.speechpro.com',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://cloud.speechpro.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://cloud.speechpro.com/service/tts',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
}
URL = "https://cloud.speechpro.com/api/tts/synthesize/demo"


class CrtAdapter:
    def __init__(self, voice_name: str = 'Vladimir_n', after_chunk_delay: int = 2, after_file_delay: int = 10):
        self.voice_name = voice_name
        self.after_chunk_delay = after_chunk_delay
        self.after_file_delay = after_file_delay

    def generate_audio(self, input_file_path: str, output_file_path: str, max_n_chars: int = 500):
        target_extension = get_extension(output_file_path)
        if target_extension == 'mp3':
            output_file_path = replace_extension(output_file_path, 'wav')
        elif target_extension == 'wav':
            pass
        else:
            raise ValueError(f'Format {target_extension} is not supported!')

        print(f'Handling file {input_file_path}...')
        start_file = time.time()
        input_text = normalize_spaces(read_as_text(input_file_path))
        combined_text = split_text(input_text, max_length=max_n_chars)

        with wave.open(output_file_path, 'wb') as output_file_handler:
            output_file_handler.setnchannels(1)
            output_file_handler.setsampwidth(2)
            output_file_handler.setframerate(22050)

            n_chunks = len(combined_text)
            for idx, val in enumerate(combined_text):
                start = time.time()
                val = val.replace('"', "'").replace('~', 'тильда').replace('/', '').replace('\\', '').replace('\t', ' ').replace('\n', ' ')
                body = f'{{"voice_name":"{self.voice_name}","text_value":"{val}"}}'
                req = Request(URL, body.encode(), HEADERS)
                if len(val) > 0:
                    while True:
                        try:
                            response = urlopen(req).read()
                            output_file_handler.writeframes(response[1000:])
                            break
                        except Exception:
                            print(f'Error querying url {URL} with body {body}')
                            print(traceback.format_exc())
                            print(f'Retrying after {self.after_chunk_delay} seconds...')
                            time.sleep(self.after_chunk_delay)
                    time.sleep(self.after_chunk_delay)
                print(f'Handled {stringify_number(idx + 1)} chunk (out of {n_chunks}) in {time.time() - start:.3f} seconds')
        time.sleep(self.after_file_delay)
        print(f'Handled file {input_file_path} in {time.time() - start_file:.3f} seconds')

        if target_extension == 'mp3':
            AudioSegment.from_wav(output_file_path).export(replace_extension(output_file_path, target_extension), format=target_extension)
            os.remove(output_file_path)
