# Whisper-audio-transcription-translation
# Whisper Audio Transcription and Translation API

This project provides a FastAPI-based web service for audio transcription and translation. It uses OpenAI's Whisper model for transcription and Google Translate API for translation into multiple languages.

---

## Features
- **Audio Transcription**: Convert audio files to English text using Whisper.
- **Text Translation**: Translate the transcribed text into any specified language.
- **FastAPI Integration**: Easy-to-use API endpoints for transcription and translation.

---

## Prerequisites
- Python 3.8 or higher
- Whisper library
- Googletrans library
- FastAPI and Uvicorn for the API

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/thakurdishanttt/Whisper-audio-transcription-translation-.git
   cd Whisper-audio-transcription-translation-
Create a Virtual Environment


python -m venv venv
source venv/bin/activate        # For Linux/Mac
venv\Scripts\activate           # For Windows
Install Dependencies


pip install -r requirements.txt
Download Whisper Model The small Whisper model is loaded automatically, but ensure your environment has the necessary dependencies for Whisper.

Usage
Start the FastAPI Server Run the following command to start the API:



uvicorn main:app --reload
The API will be available at: http://127.0.0.1:8000

API Endpoint

POST /transcribe-and-translate/

Description: Upload an audio file to transcribe it to English and translate it into the specified target language.

Request Parameters:

file: The uploaded audio file (e.g., .mp3, .wav).
target_language: Language code for translation (e.g., hi for Hindi, fr for French).
Example cURL Request:


curl -X POST "http://127.0.0.1:8000/transcribe-and-translate/" \
-H "Content-Type: multipart/form-data" \
-F "file=@example_audio.mp3" \
-F "target_language=hi"
Example Response
json

{
  "transcription": "This is the transcribed text from the audio.",
  "translation": "यह ऑडियो से ट्रांसक्राइब किया गया पाठ है।",
  "target_language": "hi"
}
Project Structure
graphql

.
├── main.py                # Main FastAPI application file
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
