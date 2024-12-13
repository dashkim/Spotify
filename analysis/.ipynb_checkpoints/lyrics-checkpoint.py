import pandas as pd
import requests

access_token = "1BtMJByE8lGu-mIiX5ZGIoZ7op_VQErtMCQ-FGeT8za7wVeYEQIE6LRH3L6HHWUq"

BASE_URL = "https://api.genius.com"

# Your song data
songs_train = [
    ("Shape of You", "Ed Sheeran", "Pop"),
    ("Blinding Lights", "The Weeknd", "Synth-pop"),
    ("Bohemian Rhapsody", "Queen", "Rock"),
    ("Bad Guy", "Billie Eilish", "Electropop"),
    ("Old Town Road", "Lil Nas X", "Country rap"),
    ("Someone Like You", "Adele", "Soul"),
    ("Levitating", "Dua Lipa", "Disco-pop"),
    ("Smells Like Teen Spirit", "Nirvana", "Grunge"),
    ("Humble", "Kendrick Lamar", "Hip hop"),
    ("Rolling in the Deep", "Adele", "Pop"),
    ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "Funk"),
    ("Blinding Lights", "The Weeknd", "Synth-pop"),
    ("Hotel California", "Eagles", "Rock"),
    ("Thank U, Next", "Ariana Grande", "Pop"),
    ("Sunflower", "Post Malone & Swae Lee", "Hip hop"),
    ("Stairway to Heaven", "Led Zeppelin", "Rock"),
    ("Hello", "Adele", "Pop"),
    ("Lose Yourself", "Eminem", "Hip hop"),
    ("Billie Jean", "Michael Jackson", "Pop"),
    ("Hey Jude", "The Beatles", "Rock"),
    ("Closer", "The Chainsmokers ft. Halsey", "EDM"),
    ("Shake It Off", "Taylor Swift", "Pop"),
    ("Despacito", "Luis Fonsi ft. Daddy Yankee", "Reggaeton"),
    ("Rolling in the Deep", "Adele", "Soul"),
    ("Thinking Out Loud", "Ed Sheeran", "Pop"),
    ("Happy", "Pharrell Williams", "Pop"),
    ("Royals", "Lorde", "Art pop"),
    ("Let Her Go", "Passenger", "Folk rock"),
    ("Radioactive", "Imagine Dragons", "Alternative rock"),
    ("Cheap Thrills", "Sia ft. Sean Paul", "Dancehall"),
    ("Blinding Lights", "The Weeknd", "Synth-pop"),
    ("Watermelon Sugar", "Harry Styles", "Pop"),
    ("Drivers License", "Olivia Rodrigo", "Pop"),
    ("Good 4 U", "Olivia Rodrigo", "Pop punk"),
    ("Dynamite", "BTS", "Disco-pop"),
    ("Peaches", "Justin Bieber ft. Daniel Caesar & Giveon", "R&B"),
    ("Save Your Tears", "The Weeknd", "Synth-pop"),
    ("Montero (Call Me By Your Name)", "Lil Nas X", "Pop rap"),
    ("Levitating", "Dua Lipa ft. DaBaby", "Disco-pop"),
    ("Leave The Door Open", "Bruno Mars, Anderson .Paak, Silk Sonic", "R&B"),
    ("Bad Habits", "Ed Sheeran", "Pop"),
    ("Stay", "The Kid LAROI & Justin Bieber", "Pop"),
    ("Industry Baby", "Lil Nas X & Jack Harlow", "Hip hop"),
    ("Heat Waves", "Glass Animals", "Indie pop"),
    ("Kiss Me More", "Doja Cat ft. SZA", "Pop"),
    ("Happier Than Ever", "Billie Eilish", "Alternative"),
    ("My Universe", "Coldplay & BTS", "Pop rock"),
    ("Need To Know", "Doja Cat", "R&B"),
    ("Deja Vu", "Olivia Rodrigo", "Pop"),
    ("Butter", "BTS", "Dance-pop"),
    ("Permission to Dance", "BTS", "Pop"),
    ("Shivers", "Ed Sheeran", "Pop"),
    ("Cold Heart", "Elton John & Dua Lipa", "Dance-pop"),
    ("Easy On Me", "Adele", "Pop"),
    ("Essence", "Wizkid ft. Tems", "Afrobeats"),
    ("Wants and Needs", "Drake ft. Lil Baby", "Hip hop"),
    ("Rockstar", "DaBaby ft. Roddy Ricch", "Hip hop"),
    ("Mood", "24kGoldn ft. Iann Dior", "Hip hop"),
    ("Laugh Now Cry Later", "Drake ft. Lil Durk", "Hip hop"),
    ("Blinding Lights", "The Weeknd", "Synth-pop"),
    ("Circles", "Post Malone", "Pop rock"),
    ("Don't Start Now", "Dua Lipa", "Disco-pop"),
    ("Memories", "Maroon 5", "Pop"),
    ("Señorita", "Shawn Mendes & Camila Cabello", "Pop"),
    ("Truth Hurts", "Lizzo", "Hip hop"),
    ("Someone You Loved", "Lewis Capaldi", "Pop"),
    ("Old Town Road", "Lil Nas X ft. Billy Ray Cyrus", "Country rap"),
    ("Talk", "Khalid", "R&B"),
    ("Sucker", "Jonas Brothers", "Pop"),
    ("Bad Guy", "Billie Eilish", "Electropop"),
    ("Without Me", "Halsey", "Pop"),
    ("Sunflower", "Post Malone & Swae Lee", "Hip hop"),
    ("Thank U, Next", "Ariana Grande", "Pop"),
    ("Shallow", "Lady Gaga & Bradley Cooper", "Pop"),
    ("Sicko Mode", "Travis Scott", "Hip hop"),
    ("I Like It", "Cardi B, Bad Bunny & J Balvin", "Hip hop"),
    ("God's Plan", "Drake", "Hip hop"),
    ("Girls Like You", "Maroon 5 ft. Cardi B", "Pop"),
    ("Havana", "Camila Cabello ft. Young Thug", "Pop"),
    ("Perfect", "Ed Sheeran", "Pop")
]

# Convert the song data into a DataFrame
songs = pd.DataFrame(songs_train, columns=["Title", "Artist", "Genre"])

# Function to get lyrics from Genius API
def get_song_lyrics(song_title, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Search for the song by title
    search_url = f"{BASE_URL}/search"
    params = {"q": song_title}
    search_response = requests.get(search_url, headers=headers, params=params)
    search_data = search_response.json()
    
    # Check if the song was found
    if search_data["response"]["hits"]:
        song_id = search_data["response"]["hits"][0]["result"]["id"]
        
        # Get song details
        song_url = f"{BASE_URL}/songs/{song_id}"
        song_response = requests.get(song_url, headers=headers)
        song_data = song_response.json()
        
        # Extract lyrics (if available)
        lyrics_url = song_data["response"]["song"]["url"]
        return lyrics_url
    else:
        return None

# Get lyrics for all songs and add them to the DataFrame
songs['Lyrics URL'] = songs['Title'].apply(lambda title: get_song_lyrics(title, access_token))

# Print the DataFrame with the lyrics URL for each song
print(songs)
