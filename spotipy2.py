
#import spotipy.oauth2 as oauth2
import spotipy.util as util
import spotipy
import pprint
import sys

# scope = None
# client_id = 'abdd03cd5c1c4dc79d15cbf50b0641ad'
# client_secret = '5b1d951d01464ccea685a5fc35977d33'
# redirect_uri = 'https://example.com/callback/'

# client_credentials_manager = oauth2.SpotifyClientCredentials(client_id='abdd03cd5c1c4dc79d15cbf50b0641ad', client_secret='5b1d951d01464ccea685a5fc35977d33')
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# search_str = 'Syd'
# result = sp.search(search_str)
# pprint.pprint(result)

def main():

    username = sys.argv[1]
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope, client_id='abdd03cd5c1c4dc79d15cbf50b0641ad', client_secret='5b1d951d01464ccea685a5fc35977d33', redirect_uri='https://example.com/callback/')
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_artists(limit=50)
    for i, item in enumerate(results['items']):
            print(i, item['name'])




main()