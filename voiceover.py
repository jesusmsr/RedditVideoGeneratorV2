from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup

text = 'Hello everyone. Welcome to this video. Today we will do a simple text-to-speech module with python. We are using the GitHub module called TTS.'

voiceoverDir = 'Voiceovers'

def create_voice_over(fileName, text):
    filePath = f'{voiceoverDir}/temp/{fileName}_temp.mp3'
    tts = gTTS(text, lang='en', tld='co.uk')
    
    tts.save(filePath)

    audio = AudioSegment.from_mp3(filePath)
    final = speedup(audio, playback_speed=1.2)
    finalFilePath = f"{voiceoverDir}/{fileName}.mp3"
    final.export(finalFilePath, format="mp3")
    
    return finalFilePath

