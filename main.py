import warnings
import whisper
from googletrans import Translator
from fastapi import FastAPI, UploadFile, HTTPException, Query
import uvicorn
import os

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize FastAPI app
app = FastAPI()

# Load Whisper model
print("Loading Whisper model...")
model = whisper.load_model("small", device="cpu")


def transcribe_audio(file_path, device="cpu"):
    """
    Transcribes an audio file into English using Whisper.

    Args:
        file_path (str): Path to the audio file.
        device (str): Device to use for transcription ("cpu" or "cuda").

    Returns:
        str: Transcribed text in English.
    """
    print(f"Transcribing audio file: {file_path}")
    result = model.transcribe(file_path, language="en")
    return result["text"]


def translate_text(text, target_language):
    """
    Translates English text into a specified language using Googletrans.

    Args:
        text (str): Text in English to translate.
        target_language (str): Language code for the target language (e.g., 'hi' for Hindi).

    Returns:
        str: Translated text in the target language.
    """
    print(f"Translating text to {target_language}...")
    translator = Translator()
    translated = translator.translate(text, src="en", dest=target_language)
    return translated.text


@app.post("/transcribe-and-translate/")
async def transcribe_and_translate(file: UploadFile, target_language: str = Query(default="hi", description="Target language code for translation (e.g., 'hi' for Hindi, 'fr' for French)")):
    """
    Endpoint to upload an audio file, transcribe it to English, and translate to a specified language.

    Args:
        file (UploadFile): The uploaded audio file.
        target_language (str): Language code for the translation (default is Hindi).

    Returns:
        dict: Transcription in English and Translation in the specified language.
    """
    try:
        # Save the uploaded file temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Step 1: Transcribe the audio file
        english_text = transcribe_audio(file_path, device="cpu")

        # Step 2: Translate the text to the specified language
        translated_text = translate_text(english_text, target_language)

        # Clean up the temporary file
        os.remove(file_path)

        return {
            "transcription": english_text,
            "translation": translated_text,
            "target_language": target_language,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
