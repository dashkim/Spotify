import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns

def load_music(name):
    script_dir = os.path.dirname(os.path.realpath(__file__)) 
    data_path = os.path.join(script_dir, 'data', f'{name}_Data') 
    print(f"Data path: {data_path}")  

    music_files = [f for f in os.listdir(data_path) if f.startswith('StreamingHistory_music') and f.endswith('.json')]
    all_data = []

    for file in music_files:
        file_path = os.path.join(data_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    music = pd.DataFrame(all_data)
    music['minutesPlayed'] = music['msPlayed'] / 60000  
    music = music.sort_values(by='endTime', ascending=True)

    return music

def load_searches(name):

    script_dir = os.path.dirname(os.path.realpath(__file__)) 
    data_path = os.path.join(script_dir, 'data', f'{name}_Data') 
    print(f"Data path: {data_path}")

    search_files = [f for f in os.listdir(data_path) if f.startswith('SearchQueries') and f.endswith('.json')]
    all_data = []

    for file in search_files:
        file_path = os.path.join(data_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    searches = pd.DataFrame(all_data)
    return searches


def format_playtime(ms):
    minutes = ms / 60000  
    hours = minutes / 60 
    if hours >= 1:
        return f"{hours:.2f} hours"
    else:
        return f"{minutes:.2f} minutes"


def get_artist_data(name):

    music = load_music(name)
    
    most_played_artist = music.groupby(['artistName'])['msPlayed'].sum().idxmax()
    total_playtime_artist = music.groupby(['artistName'])['msPlayed'].sum().max()

    most_popular_artist = music.groupby(['artistName']).size().idxmax()
    total_plays_artist = music.groupby(['artistName']).size().max()

    music['endTime'] = pd.to_datetime(music['endTime'])
    most_recent_play_artist = music.groupby(['artistName'])['endTime'].max()

    last_played_artist = most_recent_play_artist[most_recent_play_artist < music['endTime'].max() - pd.Timedelta(days=30)]
    forgotten_artists = music.groupby(['artistName']).size().loc[last_played_artist.index]
    forgotten_artists = forgotten_artists.sort_values(ascending=False).head(3)

    music['month'] = music['endTime'].dt.to_period('M')
    recent_months_artist = music.groupby(['month', 'artistName']).size().unstack().fillna(0)
    recent_months_diff_artist = recent_months_artist.diff(axis=1)

    gaining_artists = recent_months_diff_artist.max(axis=1).idxmax()
    losing_artists = recent_months_diff_artist.min(axis=1).idxmin()

    music['msPlayed'] = music['msPlayed'] / 1000

    average_artist_playtime = music.groupby(['artistName'])['msPlayed'].mean()
    longest_artist_playtime = average_artist_playtime.idxmax()
    longest_artist_time = average_artist_playtime.max()

    artist_data = {
        'most_played_artist': (most_played_artist, format_playtime(total_playtime_artist)),
        'most_popular_artist': (most_popular_artist, total_plays_artist),
        'forgotten_artists': [(artist) for artist in forgotten_artists.index],
        'gaining_artists': (gaining_artists),
        'losing_artists': (losing_artists),
        'average_artist_playtime': format_playtime(average_artist_playtime.mean()), 
        'longest_playtime_artist': (longest_artist_playtime, format_playtime(longest_artist_time))  
    }
    
    return artist_data



def get_song_data(name):

    music = load_music(name)
    
    most_played_song_by_minutes = music.groupby('trackName')['minutesPlayed'].sum().reset_index()
    most_played_song_by_minutes = most_played_song_by_minutes.sort_values(by='minutesPlayed', ascending=False)

    most_played_song = most_played_song_by_minutes.iloc[0]

    total_minutes = most_played_song['minutesPlayed']
    total_hours = total_minutes / 60  

    formatted_playtime = f"{total_hours:.2f} hours"

    most_popular_song = music.groupby(['trackName', 'artistName']).size().idxmax()
    total_plays = music.groupby(['trackName', 'artistName']).size().max()

    music['endTime'] = pd.to_datetime(music['endTime'])
    most_recent_play = music.groupby(['trackName', 'artistName'])['endTime'].max()

    last_played = most_recent_play[most_recent_play < music['endTime'].max() - pd.Timedelta(days=30)]
    forgotten_songs = music.groupby(['trackName', 'artistName']).size().loc[last_played.index]
    forgotten_songs = forgotten_songs.sort_values(ascending=False).head(3)

    music['month'] = music['endTime'].dt.to_period('M')
    recent_months = music.groupby(['month', 'trackName', 'artistName']).size().unstack().fillna(0)
    recent_months_diff = recent_months.diff(axis=1)

    gaining_songs = recent_months_diff.max(axis=1).idxmax()
    losing_songs = recent_months_diff.min(axis=1).idxmin()

    artist_streams = music.groupby(['artistName'])['msPlayed'].sum()
    most_streamed_artist = artist_streams.idxmax()
    total_streams = artist_streams.max()

    average_playtime = music['msPlayed'].mean()

    avg_playtime = music.groupby(['trackName', 'artistName'])['msPlayed'].mean()
    longest_songs = avg_playtime.idxmax()
    longest_song_time = avg_playtime.max()

    music['msPlayed'] = music['msPlayed'] / 1000

    song_data = {
        'most_played_song': (most_played_song['trackName'], formatted_playtime),  
        'most_popular_song': (most_popular_song[0], most_popular_song[1], total_plays),
        'forgotten_songs': [(track, artist) for track, artist in forgotten_songs.index],
        'gaining_songs': (gaining_songs[0], gaining_songs[1]),
        'losing_songs': (losing_songs[0], losing_songs[1]),
        'most_streamed_artist': (most_streamed_artist, total_streams),
        'average_playtime': average_playtime / 1000,  
        'longest_playtime_song': (longest_songs[0], longest_songs[1], longest_song_time / 1000)  
    }
    
    return song_data


def get_genre_data(name):
    # Spotify did not include this. pass for now, do not implement until api is functional
    return [0]


def get_dsci_data(name):
    music = load_music(name)
    music['endTime'] = pd.to_datetime(music['endTime'])

    music['date'] = music['endTime'].dt.date 
    daily_minutes = music.groupby('date')['minutesPlayed'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='date', y='minutesPlayed', data=daily_minutes, color='skyblue')
    plt.xticks(range(0, len(daily_minutes), 25), rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Minutes Played')
    plt.title(f'Minutes Played Per Day')
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0) 
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8') 
    plt.close()

    # Do more once think of it. 

    return img_base64 
    