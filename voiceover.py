import torch
from TTS.api import TTS

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    tts = TTS("tts_models/en/multi-dataset/tortoise-v2").to(device)
    tts.tts_to_file(text=text, file_path=filePath)
    return filePath