from gtts import gTTS 
import uuid
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def txtToSpeach(text,lang):
   tts = gTTS(text=text, lang=lang, slow=False)
    
    # Use BytesIO to save the audio in memory
    audio_buffer = io.BytesIO()
    tts.save(audio_buffer)  # Save to the buffer
    audio_buffer.seek(0)  # Move to the beginning of the BytesIO buffer

    filename = f"tts_audio_{uuid.uuid4()}.mp3"
    
    # Save the audio to Dropbox using the default storage
    audio_path = default_storage.save(f'audio/{filename}', ContentFile(audio_buffer.read()))

    return audio_path
# print(txtToSpeach('hello every one','en'))
