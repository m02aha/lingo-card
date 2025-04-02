import dropbox
from gtts import gTTS 
import uuid
import io
import os

def txtToSpeach(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Use BytesIO to save the audio in memory
    audio_buffer = io.BytesIO()
    tts.save(audio_buffer)  # Save to the buffer
    audio_buffer.seek(0)  # Move to the beginning of the BytesIO buffer

    filename = f"tts_audio_{uuid.uuid4()}.mp3"
    dbx = dropbox.Dropbox(os.environ.get('DROPBOX_ACCESS_TOKEN'))

    # Upload the audio file to Dropbox
    dbx.files_upload(audio_buffer.read(), f'/lingo_card/audio/{filename}')

    return f'/lingo_card/audio/{filename}'  # Return the path to the file
# print(txtToSpeach('hello every one','en'))
