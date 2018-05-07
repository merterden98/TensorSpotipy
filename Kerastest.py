from keras.models import Sequential
from keras.layers import Dense

import numpy as np
import sys
import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import json
import os
import matplotlib.pyplot as plt 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

model = Sequential()
model.add(Dense(10, input_dim=8, activation='sigmoid'))
model.add(Dense(16, activation='tanh'))
model.add(Dense(16, activation='tanh'))
model.add(Dense(1, activation='tanh'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['acc'])



def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

#spotify:user:spotify:playlist:37i9dQZEVXbq2RyStwNJ9w
#https://open.spotify.com/user/spotify/playlist/37i9dQZF1E9FOPGnofGrI5

def make_playlist(token, song_names):

    print("Making a Playlist")

    sp = spotipy.Spotify(auth=token)

    playlist_name = input("New Playlist Name\n")

    sp.user_playlist_create(sys.argv[1], playlist_name, public=True)

    playlists = sp.current_user_playlists()

        
    playlistid = []
    playlistname = []

    for things in playlists['items']:
        playlistid.append(things['id'])
        playlistname.append(things['name'])



    #pprint.pprint(playlists)
    index = playlistname.index(playlist_name)


    playlistsongs = sp.user_playlist_tracks(sys.argv[1], playlistid[index])

    sp.user_playlist_add_tracks(sys.argv[1], playlistid[index], song_names)


    







def computenet(playlist1, playlist2, token):

        l1 = []
        l2 = []
        for i in playlist1:
            l1.append(-1)
        for i in playlist2:
            l2.append(1)
        
        playlistlabels = l1 + l2
        data = playlist1 + playlist2
        data = np.asarray(data)
        playlistlabels = np.asarray(playlistlabels)
        data, playlistlabels = unison_shuffled_copies(data, playlistlabels)

        #print(data)
        model.fit(data, playlistlabels, epochs=len(data))

        sp = spotipy.Spotify(auth=token)

        playlistsongs = sp.user_playlist_tracks('spotify', '37i9dQZEVXbq2RyStwNJ9w')
        print("Starting to test Net")

        songs = []
        names = []
        for i in playlistsongs['items']:
            #print(i['track']['name'])
            names.append(i['track']['name'])
            songs.append(i['track']['id'])
    
        playlist1Features = []

        playlist = []

        features = sp.audio_features(songs)
    #pprint.pprint(features)
        for i, feature in enumerate(features):
            playlist1Features.append(feature['acousticness'])
            playlist1Features.append(feature['danceability'])
            playlist1Features.append(feature['energy'])
            playlist1Features.append(feature['instrumentalness'])
            playlist1Features.append(feature['liveness'])
            playlist1Features.append(feature['speechiness'])
            playlist1Features.append(feature['tempo'] / 160)
            playlist1Features.append(feature['valence'])
            playlist.append(playlist1Features)
            playlist1Features = []

        size = len(playlist)
        playlist = np.asarray(playlist)
        
        o1 = input("Enter the Owner of Playlist 1\n")
        o2 = input("Enter Owner of Playlist 2\n")

        #print(playlist.shape)

        result = []
        common_songs = []

        for i in range(size):
            r = model.predict(playlist[i].reshape(1,8))
            print("My guess is that the song", names[i], "would be enjoyed more by", end=' ')
            result.append(r)
            if r < 0.2 and r > -0.2:
                common_songs.append(songs[i])
            if r < 0:
                print(o1)
            else:
                print(o2)

        fig, ax = plt.subplots()

        x = range(len(playlist))
        plt.bar(x,result, align='center')

        plt.xticks(x, names)
        plt.show()

        make_playlist(token, common_songs)





def main():

    username = sys.argv[1]
    scope = 'user-read-private user-modify-playback-state user-read-recently-played user-read-playback-state playlist-read-private playlist-modify-public'
    try:
        token = util.prompt_for_user_token(username, scope,client_id='abdd03cd5c1c4dc79d15cbf50b0641ad', client_secret='5b1d951d01464ccea685a5fc35977d33', redirect_uri='https://example.com/callback/')

    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope,client_id='abdd03cd5c1c4dc79d15cbf50b0641ad', client_secret='5b1d951d01464ccea685a5fc35977d33', redirect_uri='https://example.com/callback/')


    sp = spotipy.Spotify(auth=token)


    played = sp.current_user_recently_played()

    playlists = sp.current_user_playlists()

    playlistid = []
    playlistname = []

    for things in playlists['items']:
        playlistid.append(things['id'])
        playlistname.append(things['name'])

    #playlist_name = input("Enter Playlist Name\n")

    #index = playlistname.index(playlist_name)


   # playlistsongs = sp.user_playlist_tracks(username, playlistid[index])

    playlistsongs = sp.user_playlist_tracks('spotify', '37i9dQZF1E9FOPGnofGrI5')

    songs = []
    names = []
    for i in playlistsongs['items']:
        #print(i['track']['name'])
        names.append(i['track']['name'])
        songs.append(i['track']['id'])


    playlist1Features = []

    playlist1 = []

    features = sp.audio_features(songs)
    #pprint.pprint(features)
    for i, feature in enumerate(features):
        playlist1Features.append(feature['acousticness'])
        playlist1Features.append(feature['danceability'])
        playlist1Features.append(feature['energy'])
        playlist1Features.append(feature['instrumentalness'])
        playlist1Features.append(feature['liveness'])
        playlist1Features.append(feature['speechiness'])
        playlist1Features.append(feature['tempo'] / 160)
        playlist1Features.append(feature['valence'])
        playlist1.append(playlist1Features)
        playlist1Features = []

    #print("My Playlist Features", playlist1)

    playlistsongs = sp.user_playlist_tracks('spotify', '37i9dQZF1E9WiJSwDtRFUE')


    songs = []
    names = []
    for i in playlistsongs['items']:
        #print(i['track']['name'])
        names.append(i['track']['name'])
        songs.append(i['track']['id'])

    features = sp.audio_features(songs)
    #pprint.pprint(features)

    playlist2Features = []

    playlist2 = []


    for i, feature in enumerate(features):
        playlist2Features.append(feature['acousticness'])
        playlist2Features.append(feature['danceability'])
        playlist2Features.append(feature['energy'])
        playlist2Features.append(feature['instrumentalness'])
        playlist2Features.append(feature['liveness'])
        playlist2Features.append(feature['speechiness'])
        playlist2Features.append(feature['tempo'] / 160)
        playlist2Features.append(feature['valence'])
        playlist2.append(playlist2Features)
        playlist2Features = []

    #print("Nimish's Playlist Features", playlist2)

    os.remove(f".cache-{username}")

    computenet(playlist1,playlist2, token)


main()

