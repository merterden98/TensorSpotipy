import math
import sys
import spotipy
import spotipy.util as util



scope = 'user-library-read'

def main():

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print( "Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username,scope,client_id='abdd03cd5c1c4dc79d15cbf50b0641ad',client_secret='5b1d951d01464ccea685a5fc35977d33',redirect_uri='https://beta.developer.spotify.com/dashboard/applications/abdd03cd5c1c4dc79d15cbf50b0641ad')

    print(token)

    ##client_credentials_manager = SpotifyClientCredentials()
    ##spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    ##results = spotify.search(q='artist:' + "Ed Sheeran", type= 'artist')
    ##print(results)

main()