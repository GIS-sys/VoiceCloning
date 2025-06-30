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
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации: {e}")
        return False
    except FileNotFoundError:
        print("Ошибка: ffmpeg не установлен. Установите ffmpeg для работы скрипта.")
        return False

def clone_voice(input_audio, text_to_speak, output_file="cloned_voice.wav"):
    """Клонирование голоса с использованием YourTTS"""
    # Проверяем доступность CUDA
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Используемое устройство: {device}")

    # Конвертируем входной файл в WAV 16kHz если нужно
    if not input_audio.endswith('.wav'):
        wav_file = "temp_voice.wav"
        if not convert_to_wav(input_audio, wav_file):
            raise ValueError("Не удалось конвертировать входной файл")
        input_audio = wav_file

    # Инициализируем модель YourTTS
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True).to(device)

    # Генерируем речь с клонированным голосом
    try:
        tts.tts_to_file(
            text=text_to_speak,
            speaker_wav=input_audio,
            language="en",
            file_path=output_file
        )
        
        print(f"\nРезультат сохранён в {output_file}")
        
        # Воспроизводим результат (если запущено в Jupyter)
        try:
            audio, sr = sf.read(output_file)
            return Audio(audio, rate=sr)
        except:
            pass
        
    except Exception as e:
        print(f"Ошибка при генерации речи: {e}")
        return None

if __name__ == "__main__":
    # Пример использования
    input_voice = "your_voice.mp3"  # Ваш голосовой файл
    text = "Hello! I love being a student of High School of Economics"  # Текст для озвучки
    
    if not os.path.exists(input_voice):
        print(f"Файл {input_voice} не найден. Пожалуйста, создайте его или укажите правильный путь.")
    else:
        print("Начинаем процесс клонирования голоса...")
        clone_voice(input_voice, text, "cloned_voice.wav")
        print("Готово! Проверьте файл cloned_voice.wav")
