import os
import torch
from TTS.api import TTS
import soundfile as sf
import subprocess


# Constants
OUTPUT_FILE_BASE = "output_{0}_{1}.wav"
TEMP_WAV_FILE = "temp_voice.wav"

DEFAULT_SAMPLE_RATE = 22050
DEFAULT_INPUT_VOICE_FILE = "your_voice.mp3"
DEFAULT_LANGUAGE = "ru"
DEFAULT_TEXT = "1 2 3 4"


def input_with_default(label="Input", default=""):
    i = input(f"{label} ({default}): ")
    if i.strip() == "":
        return default
    return i


def convert_to_wav(input_file: str, output_file: str, sample_rate: int) -> bool:
    """
    input_file:  relative path to input file (f.e. "./your_voice.mp3")
    output_file: relative path to output file with .wav extension (f.e. "./temp_voice.wav")
    sample_rate: integer for sample rate of input file (f.e. 16000)
    """
    try:
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-ar', str(sample_rate),
            '-ac', '1',
            '-y', output_file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"Error while converting file {input_file} to {output_file} with sample rate = {sample_rate}: {e}")
        return False


def clone_voice(input_audio: str, input_sample_rate: int, text_to_speak: str, output_file: str, language: str):
    """
    input_audio:       relative path to input file (f.e. "./your_voice.mp3")
    input_sample_rate: integer for sample rate of input file (f.e. 16000)
    text_to_speak:     text which will be pronounced by the cloned voice
    output_file:       relative path to output file with .wav extension (f.e. "./temp_voice.wav")
    language:          one of allowed laguage codes ("ru"/"en") of current working language
    """
    # Check cuda
    if torch.cuda.is_available():
        device = 'cuda'
        print("GPU was detected. It will be used to speed up the computations")
    else:
        device = 'cpu'
        print("Defaulting to CPU (no GPU was detected)")

    # Preparing input data
    if not input_audio.endswith('.wav'):
        wav_file = TEMP_WAV_FILE
        if not convert_to_wav(input_audio, wav_file, input_sample_rate):
            raise ValueError("Couldn't convert input file!")
        input_audio = wav_file

    # Main speech processing
    try:
        # Initialize model
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=True,
            config_path=None,
            vocoder_path=None,
            gpu=(device == 'cuda'),
        )

        # Generate
        tts.tts_to_file(
            text=text_to_speak,
            speaker_wav=input_audio,
            language=language,
            file_path=output_file,
        )

        # Done!
        print(f"\nSuccess! The result has been saved in {output_file}")

    except Exception as e:
        print(f"Critical error!")
        print(traceback.format_exc())


if __name__ == "__main__":
    # Inputs
    input_voice_file = input_with_default("Relative path to input file", DEFAULT_INPUT_VOICE_FILE)
    language = input_with_default("Select language, available for now are [ru, en]", DEFAULT_LANGUAGE)
    text = input_with_default("Text to pronounce with generated voice in selected language", DEFAULT_TEXT)
    input_sample_rate = input_with_default("Sample rate of input file (if you don't know what it is - just press enter)", DEFAULT_SAMPLE_RATE)

    # Calculate from inputs
    output_file = OUTPUT_FILE_BASE.format(os.path.basename(input_voice_file), language)

    if not os.path.exists(input_voice_file):
        print(f"File to clone ({input_voice_file}) does not exist")
    else:
        print(f"Cloning file {input_voice_file} in language {language}")
        clone_voice(
            input_voice_file,
            input_sample_rate,
            text,
            output_file,
            language,
        )
