import threading
from flask import Flask, render_template, request
import subprocess
import random
import json
from keras.models import load_model
import numpy as np
import pickle
from nltk.stem import WordNetLemmatizer
from urllib import response
from flask_cors import CORS, cross_origin
import nltk
import schedule
import time
import json
# import weather
# import apiservice
# import mergedata
# import training
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask_socketio import SocketIO, emit
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
nltk.download('popular')
lemmatizer = WordNetLemmatizer()
model = load_model('model.h5')


intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result



def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

class FileChangedHandler(FileSystemEventHandler):
    def __init__(self):
        self.updated = False
        self.updating =False
        super().__init__()
    def on_modified(self, event):
        if event.src_path.endswith('data.json'):
            print('data.json is modified')
            if self.updating:
                self.updating = False
                print('data.json saved')
                print('Stopping Flask API...')
                subprocess.Popen('taskkill /f /fi "imagename eq app.py"', shell=True)
                time.sleep(10)
                print('Starting Flask API...')
                subprocess.Popen('python app.py', shell= True)
                print('"python app.py"')
            else:
                self.updating = True
                print('data.json updating')
    def on_closed(self, event):
        if event.src_path.endswith('data.json') and self.updating:
            self.updating =False
            print('Stopping Flask API...')
            subprocess.Popen('taskkill /f /fi "imagename eq python.exe"', shell=True)
            time.sleep(1)
            print('Starting Flask API...')
            subprocess.Popen('python app.py', shell=True)
            print('"python app.py"')
def start_observer():
    observer = Observer()
    observer.schedule(FileChangedHandler(), path='E:\Chatbot-app\C2SE07Cap2-BE-ChatBot\\', recursive=True)
    observer.start()

    # Chạy observer trong khi Flask Server đang chạy
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
app = Flask(__name__)
CORS(app)
socket= SocketIO(app)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/get")
@cross_origin(supports_credentials=True)
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(FileChangedHandler(), path='E:\Chatbot-app\C2SE07Cap2-BE-ChatBot\\', recursive=True)
    observer.start()
    socket.run(app)

    observer.stop()
    observer.join()
