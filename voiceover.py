from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import re

text = 'Hello everyone. Welcome to this video. Today we will do a simple text-to-speech module with python. We are using the GitHub module called TTS.'

voiceoverDir = 'Voiceovers'

def remove_emoji(string):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def create_voice_over(fileName, text):
    filePath = f'{voiceoverDir}/temp/{fileName}_temp.mp3'
    tts = gTTS(remove_emoji(text), lang='en', tld='co.uk')
    
    tts.save(filePath)

    audio = AudioSegment.from_mp3(filePath)
    final = speedup(audio, playback_speed=1.2)
    finalFilePath = f"{voiceoverDir}/{fileName}.mp3"
    final.export(finalFilePath, format="mp3")
    
    return finalFilePath

