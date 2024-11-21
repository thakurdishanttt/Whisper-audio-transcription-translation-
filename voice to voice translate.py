from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import whisper
from googletrans import Translator
from gtts import gTTS
import os
import shutil
import uvicorn

app = FastAPI()

# Step 1: Speech-to-Text using Whisper AI
def speech_to_text(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    return result["text"]

# Step 2: Translation using Google Translate
def translate_text(text, target_lang):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Step 3: Text-to-Speech using gTTS
def text_to_speech(text, lang_code, output_path):
    tts = gTTS(text=text, lang=lang_code)
    tts.save(output_path)

@app.post("/translate-audio/")
async def translate_audio(file: UploadFile = File(...), target_lang: str = "es"):
    # Save uploaded audio file temporarily
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Convert speech to text (in English)
        transcribed_text = speech_to_text(audio_path)
        
        # Translate text to target language
        translated_text = translate_text(transcribed_text, target_lang)
        
        # Convert translated text to speech
        output_audio_path = f"output_{file.filename}.mp3"
        text_to_speech(translated_text, target_lang, output_audio_path)
        
        # Return the audio file
        return FileResponse(
            output_audio_path,
            media_type="audio/mpeg",
            filename=output_audio_path
        )
    
    finally:
        # Cleanup temporary files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
if __name__ == "__main__":
    # Run FastAPI app with title "Speech-to-Speech Translation API"
    app.title = "Speech-to-Speech Translation API"
    uvicorn.run(app, host="127.0.0.1", port=8000)