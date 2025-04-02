from gtts import gTTS 
import uuid
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def txtToSpeach(text,lang):
    tts=gTTS(text=text,lang=lang,slow=False)
    filename=f"tts_audio_{uuid.uuid4()}.mp3"
     # Save the audio to a ContentFile and then to Dropbox
    audio_content = ContentFile(tts.save(filename))
    audio_path = default_storage.save(f'audio/{filename}', audio_content)

    return audio_path

# print(txtToSpeach('hello every one','en'))
