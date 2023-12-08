from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import random
import base64
from ocr import getData, processData, assess
from speech.syllables import getWordData
from gtts import gTTS
import os
import json
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)
Bootstrap(app)

currWord = ""
wordslist = []
speechWord = ""
speechSyllables = 0
res = []

# Initialize the TTS engine
tts_engine = pyttsx3.init()

def text_to_speech(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Initialize the STT recognizer
recognizer = sr.Recognizer()

def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/handwriting/', methods=["GET", "POST"])
def handwriting():
    
    global currCharacter
    global res
    if request.method == "POST":
        reqjson = str(request.get_json())[22:]
        with open("image.png", "wb") as imgfile:
            imgfile.write(base64.b64decode(reqjson))
        writtenWord = processData(getData('image.png'))
        print("input character",writtenWord)
        print("given character",currCharacter)
        res = assess(currCharacter, writtenWord)
        return jsonify("OK")
    
    currCharacter = random.choice('abcdefghijklmnopqrstuvwxyz').lower()
    return render_template("hwp.html", word=currCharacter)
@app.route('/handwriting/results/', methods=["GET", "POST"])
def handwriting_results():
    global res
    return render_template("hwp_results.html", res=res)

@app.route('/games/')
def games():
    return render_template("games.html")

@app.route('/speech/', methods=["GET", "POST"])
def speech():
    global speechWord
    global speechSyllables
    if request.method == "POST":
        result = speech_to_text()
        outcome = 0
        if result.lower() == speechWord.lower():
            outcome = 1
        return redirect(url_for("speech_results", outcome=outcome))
    speechWord, speechSyllables = getWordData()
    return render_template("speech.html", word=speechWord)

@app.route('/speech/results/<outcome>', methods=["GET", "POST"])
def speech_results(outcome):
    if int(outcome) == 0:
        msg = "Not quite! Try again"
    else:
        msg = "Good job!"
    return render_template("speech_results.html", msg=msg)

if __name__ == "__main__":
    with open("words.txt", "r") as readfile:
        wordslist = readfile.readlines()
    app.run(debug=True)
