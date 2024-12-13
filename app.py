from flask import Flask, render_template, request
import os
import json
import pandas as pd
from analysis.analysis import get_song_data, get_artist_data, get_genre_data, get_dsci_data 



app = Flask(__name__)

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Artists page route
@app.route('/artists/<name>')
def artists(name):

    artist_data = get_artist_data(name)
        
    return render_template('artists.html', 
                           name=name, 
                           most_played_artist=artist_data['most_played_artist'],
                           most_popular_artist=artist_data['most_popular_artist'],
                           forgotten_artists=artist_data['forgotten_artists'],
                           gaining_artists=artist_data['gaining_artists'],
                           losing_artists=artist_data['losing_artists'],
                           longest_playtime_artist=artist_data['longest_playtime_artist'],
                           average_artist_playtime=artist_data['average_artist_playtime'])

# Songs page route
@app.route('/songs/<name>')
def songs(name):

    song_data = get_song_data(name)
    
    return render_template('songs.html', 
                           name=name, 
                           most_played_song=song_data['most_played_song'],
                           most_popular_song=song_data['most_popular_song'],
                           forgotten_songs=song_data['forgotten_songs'],
                           gaining_songs=song_data['gaining_songs'],
                           losing_songs=song_data['losing_songs'],
                           most_streamed_artist=song_data['most_streamed_artist'],
                           average_playtime=song_data['average_playtime'],
                           longest_playtime_song=song_data['longest_playtime_song'])


# Genre Page Route
@app.route('/genres/<name>')
def genres(name):
    return render_template('genres.html', name=name)

# DSCI page route
@app.route('/dsci/<name>')
def dsci(name):

    img_base64 = get_dsci_data(name)
    return render_template('dsci.html', name=name, img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
