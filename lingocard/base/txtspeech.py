from gtts import gTTS 
import uuid
import os
from django.conf import settings

def txtToSpeach(text,lang):
    tts=gTTS(text=text,lang=lang,slow=False)
    filename=f"tts_audio_{uuid.uuid4()}.mp3"
    audio_path=os.path.join(settings.MEDIA_ROOT,'audio',filename)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    tts.save(audio_path)
    

    return audio_path

# print(txtToSpeach('hello every one','en'))
