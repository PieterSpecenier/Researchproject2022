import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import socket
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
import pylab
import librosa
import librosa.display
import numpy as np
import pandas as pd
mapper = ['Hiphop', 'Pop', 'Rock', 'Sertanejo']
modellyrics = tf.keras.models.load_model('researchproject/lyricsrecognitionmodel.h5')
modelmusic = tf.keras.models.load_model('researchproject/musicGenreRecognitionModel.h5')

classes = ['Blues','Classical','Country','Disco','Hiphop', 'Jazz','Metal','Pop','Reggae','Rock']
num_mfcc = 13
n_fft = 2048
hop_length = 512
sample_rate = 22050
samples_per_track = sample_rate * 30
num_segment = 10
samples_per_segment = int(samples_per_track / num_segment)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
CORS(app)

endpoint = "/api/v1"

app.config['ALLOWED_AUDIO_EXTENSIONS'] = ["mp3", "wav"]

dir_path = os.path.join(os.path.dirname(__file__), "../Data")

@app.route("/")
def index():
    return f"Please use {endpoint}"

@app.route(endpoint + "/audio", methods=['POST'])
def audio():
    print("audio function is being called")
    if request.method == 'POST':
        print("request.files: ", request.files)
        if 'audio' not in request.files:
            print("file not found")
            return jsonify("No uploaded file found"), 400
        audio_file = request.files['audio']
        file_name = audio_file.filename
        # check that the uploaded file is a correct audio file
        print("audio_file: ", audio_file.filename)
        if not file_name.endswith(".wav"):
            valid_exts = ', '.join(app.config['ALLOWED_AUDIO_EXTENSIONS'])
            print("no valid file found")
            return jsonify(f"No valid uploaded file found. Valid extensions: {valid_exts}"), 400
        
        filename = f"{uuid.uuid4()} {audio_file.filename}"
        filepath = os.path.join(dir_path, filename)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        audio_file.save(os.path.abspath(filepath))

        song_path = filepath
        prediction = predict_genre(song_path)
        artist_database = pd.read_csv('researchproject/artists-data.csv')
        artist_database = artist_database.drop_duplicates(subset = 'Link', keep ='first')
        lyrics_database = pd.read_csv('researchproject/lyrics-data.csv')
        lyrics_database.rename(columns={'ALink':'Link'}, inplace=True)
        artistLyrics_database = pd.merge(lyrics_database,artist_database, on='Link')
        specific_columns = artistLyrics_database[['Artist', 'SName', 'Genre','Lyric', 'Popularity','Idiom']]
        dataset = specific_columns[specific_columns.Lyric.notnull()]
        dataset = dataset.drop(columns=['Idiom','Popularity','Lyric'])
        dataset = dataset[dataset['Genre'] == prediction]
        dataset = dataset.sample(3)
        print(dataset[0:3])
        dataset = dataset.to_dict()
        print(dataset)


        if os.path.exists(os.path.abspath(filepath)):
            os.remove(os.path.abspath(filepath))
            print(f"Deleted file: {filename}")
        else:
            print("File does not exist")

        return jsonify(dataset), 200
    else:
        return jsonify("Only POST requests are allowed"), 405

@app.route(endpoint + "/lyrics", methods=['POST'])
def lyrics():
    if request.method == 'POST':
        print(request.data.decode('utf-8'))
        lyrics = request.data.decode('utf-8')
        tokenizer = Tokenizer(num_words= None)
        tokenizer.fit_on_texts(lyrics)
        sequences = tokenizer.texts_to_sequences(lyrics)
        X_encoded = pad_sequences(sequences, maxlen=100, padding='post')
        prediction_data = modellyrics.predict(X_encoded)
        index = np.argmax(prediction_data.sum(axis=0))
        genre = mapper[index]
        artist_database = pd.read_csv('researchproject/artists-data.csv')
        artist_database = artist_database.drop_duplicates(subset = 'Link', keep ='first')
        lyrics_database = pd.read_csv('researchproject/lyrics-data.csv')
        lyrics_database.rename(columns={'ALink':'Link'}, inplace=True)
        artistLyrics_database = pd.merge(lyrics_database,artist_database, on='Link')
        specific_columns = artistLyrics_database[['Artist', 'SName', 'Genre','Lyric', 'Popularity','Idiom']]
        dataset = specific_columns[specific_columns.Lyric.notnull()]
        dataset = dataset.drop(columns=['Idiom','Popularity','Lyric'])
        dataset = dataset[dataset['Genre'] == genre]
        dataset = dataset.sample(3)
        print(dataset[0:3])
        dataset = dataset.to_dict()
        print(dataset)
        return jsonify(dataset), 200


def predict_genre(song_path):
    x, sr = librosa.load(song_path, sr = sample_rate)
    class_predictions = []
    prediction_per_part = []
    for n in range(num_segment):
                start = samples_per_segment * n
                finish = start + samples_per_segment
                mfcc = librosa.feature.mfcc(x[start:finish],
                sample_rate, n_mfcc = num_mfcc, n_fft = n_fft,   
                hop_length = hop_length)
                mfcc = mfcc.T
                mfcc = mfcc.reshape(1, mfcc.shape[0], mfcc.shape[1])
            
                array = modelmusic.predict(mfcc)*100
                array = array.tolist()
    #find maximum percentage class predicted
    class_predictions.append(array[0].index(max(array[0])))
    occurence_dict = {}
    for i in class_predictions:
                if i not in occurence_dict:
                    occurence_dict[i] = 1
                else:
                    occurence_dict[i] +=1
    max_key = max(occurence_dict, key=occurence_dict.get) 
    prediction_per_part.append(classes[max_key])

    prediction = max(set(prediction_per_part), key = prediction_per_part.count)
    print(prediction)
    return prediction
    
if __name__ == '__main__':
    # run the app locally
    app.run(host="0.0.0.0", port=5000, debug=False)