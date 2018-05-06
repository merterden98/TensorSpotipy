import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import json
import os
import sys
from json.decoder import JSONDecoder



import numpy as np



class ANN(object):
    def __init__(self):
        self.w1 = np.random.randn(7,4)
        self.w2 = np.random.randn(4,1)
        self.Etotal = 0

    
    def forwardprop(self, inputs):
            self.inputs = inputs
            self.z1 = np.dot(inputs, self.w1)
            self.a1 = activation(self.z1)
            self.z2 = np.dot(self.a1, self.w2)
            self.a2 = activation(self.z2)
            self.guess = np.argmax(self.a2)


        
    def predict(self, inputs):
            self.inputs = inputs
            self.z1 = np.dot(inputs, self.w1)
            self.a1 = activation(self.z1)
            self.z2 = np.dot(self.a1, self.w2)
            self.a2 = activation(self.z2)
            self.guess = np.argmax(self.a2)
            return self.a2

    def error(self, expected, epoch):
            self.Etotal += (np.sum((self.a2-expected)**2))/2
    
    
        
    def deltaF(self,expected):
        self.dE = ((self.a2 - expected)).reshape(1,1)
        #print("dE", self.dE)
        dO = activationprime(self.z2)
        self.deltaO = np.multiply(self.dE,dO).transpose()
        #print(self.deltaO)


        
    def deltaHi(self):
        dEo = activationprime(self.z1)
        deltaH = np.dot(self.w2, self.deltaO)
        self.deltaH = np.multiply(deltaH.transpose(), dEo)
        self.deltaH = self.deltaH.transpose()
        
 
       
    def backpropagate(self, expected, epoch):
        #print(expected)
        self.error(expected, epoch)
        self.deltaF(expected)
        self.deltaHi()
        self.z1 = self.z1.reshape(1,4)
        
        learningR = 1
        
        if self.Etotal / (epoch + 1) < 0.25:
            learningR = 0.1
        
        weightUp = (learningR * np.dot(self.deltaO, self.z1)).transpose()
        self.w2 = self.w2 - weightUp
        self.inputs = self.inputs.reshape(1,7)
        weightUp = (learningR * np.dot(self.deltaH, self.inputs)).transpose()
        self.w1 = self.w1 - weightUp
    





def activation(val):
          return 1.0 / (1 + np.exp(-val))
#        return np.tanh(val)
    
def activationprime(val):
        return activation(val)*(1-activation(val))
#        return 1 - activation(val)**2

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def test_net(net, token):

    sp = spotipy.Spotify(auth=token)
    playlistsongs = sp.user_playlist_tracks('spotifycharts', '37i9dQZEVXbMDoHDwVN2tF')
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
        playlist1Features.append(feature['valence'])
        playlist.append(playlist1Features)
        playlist1Features = []

    size = len(playlist)
    playlist = np.asarray(playlist)

    o1 = input("Enter the Owner of Playlist 1\n")
    o2 = input("Enter Owner of Playlist 2\n")

    for i in range(size):
        r = net.predict(playlist[i])
        print("My guess is that the song", names[i], "would be enjoyed more by", end=' ')
        if r < 0.5:
            print(o1)
        else:
            print(o2)

    
    

def begin_net(playlist1, playlist2, token):

        l1 = []
        l2 = []
        net = ANN()
        for i in playlist1:
            l1.append(0)
        for i in playlist2:
            l2.append(1)
        
        playlistlabels = l1 + l2
        data = playlist1 + playlist2
        data = np.asarray(data)
        playlistlabels = np.asarray(playlistlabels)
        data, playlistlabels = unison_shuffled_copies(data, playlistlabels)
        print("Combined these playlists have ", len(playlistlabels), " songs")
        print("Playlist 1 has", len(l1), "songs and playlist 2 has", len(l2), "songs")
        
        i = input("Enter Training Amount\n")


        for z in range(int(i)):
            net.forwardprop(data[z])
            if playlistlabels[z] == 0:
                net.backpropagate(([0]), z)
            else:
                net.backpropagate(([1]), z)

        test_net(net, token)




def main():

    username = sys.argv[1]
    scope = 'user-read-private user-modify-playback-state user-read-recently-played user-read-playback-state playlist-read-private'
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

    playlist_name = input("Enter Playlist Name\n")

    index = playlistname.index(playlist_name)


    playlistsongs = sp.user_playlist_tracks(username, playlistid[index])


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
        playlist1Features.append(feature['valence'])
        playlist1.append(playlist1Features)
        playlist1Features = []

    #print("My Playlist Features", playlist1)

    playlistsongs = sp.user_playlist_tracks('22vm5ow6xk7mhwlami4urvmiq', '5y5oebtuSnNvIKLDFwQ7GF')


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
        playlist2Features.append(feature['valence'])
        playlist2.append(playlist2Features)
        playlist2Features = []

    #print("Nimish's Playlist Features", playlist2)

    os.remove(f".cache-{username}")
    begin_net(playlist1, playlist2, token)



    



main()