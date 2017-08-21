
# Song Similarities

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from similarity import *
import ast
import json


app = Flask(__name__)
app.config["DEBUG"] = True

filename = '../song_metrics.csv'
song_stats = pd.read_csv(filename)

artists = list(song_stats['artist'].unique())

album_init = list(song_stats[song_stats['artist']=='KRS-One']['album'].unique())
track_init = list(song_stats[song_stats['album']=='Return of the Boom Bap']['track_name'].unique())

spot_with_topics = ['artist','album','track_name', 'valence', 'speechiness', 'tempo', 'liveness', 'loudness',
        'instrumentalness','year', 'energy', 'danceability',
        'Thoughts/Brotherhood','Love/Feelings', 'Sexual', 'Gangs/Money', 'Ice Cube?',
        'Weighted Complexity']

spotify = ['artist','album','track_name', 'valence', 'speechiness', 'tempo', 'liveness', 'loudness',
        'instrumentalness', 'year', 'energy', 'danceability',
        'Weighted Complexity']

topics = ['artist','album','track_name','Thoughts/Brotherhood','Love/Feelings', 'Sexual', 'Gangs/Money', 'Ice Cube?',]

def select_data(params):
    cols = []
    if params == "Topics":
        cols = topics
    elif params == "Spotify":
        cols = spotify
    else:
        cols = spot_with_topics

    filename = '../song_metrics.csv'
    song_stats = pd.read_csv(filename)
    song_stats = song_stats[cols]
    song_stats = song_stats.dropna()
    return song_stats, cols

@app.route('/', methods=["GET", "POST"])
def index():

    return render_template("index.html", artists=artists, album_init=album_init, track_init=track_init)

@app.route("/selectparams", methods=['POST'])
def select_params():
    ret = ''
    data = request.json
    params = data['params']

    song_stats, cols = select_data(params)

    album_init = list(song_stats[song_stats['artist']=='KRS-One']['album'].unique())
    track_init = list(song_stats[song_stats['album']=='Return of the Boom Bap']['track_name'].unique())

    ret = dict()
    albums = ''
    tracks = ''

    for entry in album_init:
        albums += '<option value="{}">{}</option>'.format(entry,entry)

    for entry in track_init:
        tracks += '<option value="{}">{}</option>'.format(entry,entry)

    ret['albums'] = albums
    ret['tracks'] = tracks

    return jsonify(ret)

@app.route("/selectalbums", methods=['POST'])
def select_album():
    ret = ''
    data = request.json
    #print(data)
    artist = data['artist']
    params = data['params']

    song_stats, cols = select_data(params)

    ret = ''

    for entry in list(song_stats[song_stats['artist']==artist]['album'].unique()):
        ret += '<option value="{}">{}</option>'.format(entry,entry)

    return jsonify(ret)

@app.route("/selecttracks", methods=['POST'])
def select_track():
    ret = ''
    data = request.json
    #print(data)
    album = data['album']
    params = data['params']

    song_stats, cols = select_data(params)

    for entry in list(song_stats[song_stats['album']==album]['track_name']):
        ret += '<option value="{}">{}</option>'.format(entry,entry)
    return jsonify(ret)

@app.route("/similar", methods=['POST'])
def select_similar():
    ret = ''
    data = request.json
    track = data["track"]
    params = data["params"]
    count = int(data["count"])

    song_stats, cols = select_data(params)

    ret = dict()
    headers = '<th class="text-left">Rank</th>'
    for col in cols:
        headers += '<th class="text-left">{}</th>'.format(col)

    ret['headers'] = headers

    info = ''
    similar_songs = get_similar_songs(song_stats, track, count)
    count = 1
    for x in similar_songs:
        print(count)
        info += '<tr id={}><td class="text-left">{}</td>'.format(count, count)
        for col in cols:
            try:
                x[col] = round(x[col],3)
            except:
                pass
            info += '<td class="text-left">{}</td>'.format(x[col])
        info += '</tr>'
        count+=1

    ret['data'] = info
    return jsonify(ret)

app.run(port=5000,debug=True)
