import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import json
import config
from PyLyrics import *
from pymongo import MongoClient
from nltk.corpus import stopwords
import re


import warnings
warnings.filterwarnings('ignore')

ccm = SpotifyClientCredentials(
    client_id = config.spotify_id,
    client_secret = config.spotify_secret
)
sp = spotipy.Spotify(client_credentials_manager = ccm)

client = MongoClient()
music_db = client.music_db
songs = music_db.song_collection

def getTracks(album):
    url = "http://lyrics.wikia.com/api.php?action=lyrics&artist={0}&fmt=xml".format(album.artist())
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    for al in soup.find_all('album'):
        if al.text.lower().strip() == album.name.strip().lower():
            currentAlbum = al
            break
    try:
        songs = [song.text for song in currentAlbum.findNext('songs').findAll('item')]
    except:
        songs = []

    return songs

def songsOnSpotify(artist, album):
    results = sp.search(q = "artist:"+artist+" album:" + album, type='album')
    #print(results)
    if len(results['albums']['items']) > 0:
        album_id = results['albums']['items'][0]['uri']
        #print('Album: '+album)
    else:
        print('Artist: '+artist+' Album: '+album+' NOT ON SPOTIFY')
        return [], []
    on_spotify_names = []
    on_spotify_uris = []
    tracks = sp.album_tracks(album_id)
    for track in tracks['items']:
        """
        Check for features in track name and remove because
        lyrics wikia does not include features in track name
        and therefore would not be able to find a match to Spotify

        TO DO: Maybe add featured artists later on
        """
        if 'feat.' in track['name']:
            name = track['name'][:track['name'].index('feat.')-2]
            on_spotify_names.append(name)
        else:
            name = track['name']
            on_spotify_names.append(name)
        on_spotify_uris.append(track['uri'])
    return on_spotify_names, on_spotify_uris

def verifyArtists(artists):
    for artist in artists:
        try:
            albums = PyLyrics.getAlbums(singer=artist)
        except:
            print(artist + ' NOT FOUND')
            pass
    print('DONE ')
    print(str(len(artists))+' Artists')


def getAllSongs(artists):
    for artist in artists:
        print(artist)
        try:
            albums = PyLyrics.getAlbums(singer=artist)
        except:
            print(artist + ' NOT FOUND')
            pass
        for a in albums:
            tracks = getTracks(a)
            spot_tracks, spot_uris = songsOnSpotify(artist,a.name)
            spot_tracks = [st.lower() for st in spot_tracks]
            #print(spot_tracks)
            for track in tracks:
                try:
                    song_dict = dict()
                    song_dict['artist'] = artist
                    song_dict['album'] = a.name
                    song_dict['year'] = int(a.year[1:-1])
                    song_dict['track_name'] = track
                    song_dict['lyrics'] = PyLyrics.getLyrics(artist,track)
                    if track.lower() in spot_tracks:
                        features = sp.audio_features(spot_uris[spot_tracks.index(track.lower())])
                        for feature in features[0].keys():
                            song_dict[feature] = features[0][feature]
                    songs.insert_one(song_dict)
                except:
                    print(track + ' LYRICS NOT FOUND')
                    pass
    print('ALL SONGS DONE')

def clearCollection(songs):
    songs.delete_many({})
    print('COLLECTION EMPTY')
