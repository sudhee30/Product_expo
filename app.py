from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import os

app = Flask(__name__)
CORS(app)

# Function to convert audio to text
def convert_audio_to_text(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Audio unintelligible"
    except sr.RequestError:
        return "API request error"

@app.route('/record', methods=['POST'])
def record_audio():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file_path = 'recorded_audio.wav'
    audio_file.save(file_path)
    text = convert_audio_to_text(file_path)
    os.remove(file_path)  # Clean up
    return jsonify({'report': text})

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files.get('file')
    if not audio_file:
        return jsonify({'error': 'No file provided'}), 400

    file_path = 'uploaded_audio.wav'
    audio_file.save(file_path)
    text = convert_audio_to_text(file_path)
    os.remove(file_path)  # Clean up
    return jsonify({'report': text})

if __name__ == '__main__':
    app.run(debug=True)
