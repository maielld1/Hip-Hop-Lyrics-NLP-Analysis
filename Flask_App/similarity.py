import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


def get_similar_songs(df, track_name, num):
    song_stats = df
    track = song_stats[song_stats['track_name']==track_name]
    track = track[track.columns[3:]]
    dist_and_index=[]
    for row in song_stats.iterrows():
        index, data = row
        other_song = data.tolist()
        sim = cosine_similarity(track.values.tolist()[0],other_song[3:])
        dist_and_index.append((sim,index))
    sort_distances = sorted(dist_and_index,reverse=True)[:num+1]
    sim_songs = []
    for x in sort_distances:
        sim_songs.append(song_stats.loc[x[1]])
    return sim_songs
