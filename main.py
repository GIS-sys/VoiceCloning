import os
import torch
from TTS.api import TTS
import soundfile as sf
import subprocess
from IPython.display import Audio

def convert_to_wav(input_file, output_file, sample_rate=16000):
    """Конвертация аудиофайла в WAV формата 16kHz"""
    try:
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-ar', str(sample_rate),
            '-ac', '1',
            '-y', output_file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return False

def clone_voice(input_audio, text_to_speak, output_file="cloned_voice.wav", language="ru"):
    """Клонирование голоса с исправленной версией XTTS"""
    # Проверяем доступность CUDA
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Используемое устройство: {device}")

    # Конвертируем входной файл
    if not input_audio.endswith('.wav'):
        wav_file = "temp_voice.wav"
        if not convert_to_wav(input_audio, wav_file):
            raise ValueError("Не удалось конвертировать входной файл")
        input_audio = wav_file

    try:
        # Инициализация модели с правильными параметрами
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=True,
            config_path=None,
            vocoder_path=None,
            gpu=False if device == 'cpu' else True
        )

        # Генерация речи
        tts.tts_to_file(
            text=text_to_speak,
            speaker_wav=input_audio,
            language=language,
            file_path=output_file
        )
        
        print(f"\nУспешно! Результат сохранён в {output_file}")
        
        # Воспроизведение результата
        try:
            audio, sr = sf.read(output_file)
            return Audio(audio, rate=sr)
        except:
            pass
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return None

if __name__ == "__main__":
    # Установите правильные версии библиотек перед запуском:
    print("""
    Перед запуском выполните:
    pip install TTS==0.20.2 torch==2.1.0 torchaudio==2.1.0 transformers==4.29.2
    """)

    input_voice = "your_voice.mp3"
    
    # Русский пример
    if os.path.exists(input_voice):
        print("Клонирование на русском...")
        clone_voice(input_voice, 
                   "Привет, это мой клонированный голос. Как вам такое?", 
                   "output_ru.wav",
                   language="ru")
        
        # Английский пример
        print("Клонирование на английском...")
        clone_voice(input_voice,
                   "Hello! This is my cloned voice speaking English",
                   "output_en.wav",
                   language="en")
    else:
        print(f"Файл {input_voice} не найден")
