# How to install

```bash
conda create -n voice_clone python=3.9
conda activate voice_clone
conda install pytorch==2.1.0 torchaudio==2.1.0 -c pytorch
pip install numpy==1.22 --upgrade
pip install --upgrade TTS
pip install IPython
pip install transformers==4.49 --upgrade
```

Then fix error in /home/giswarm/miniconda3/envs/voice_clone/lib/python3.9/site-packages/bangla/__init__.py (remove "| None" from specific line)

# How to use

Put voice you need to clone as "your_voice.mp3" in the root of this project. Then run

```bash
python main.py
```

After that you will have output_en.wav and output_ru.wav files - cloned voices saying some default text
