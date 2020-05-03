import logging
import spotipy
from lastipy.spotify import token
from lastipy.spotify.parse_spotify_tracks import parse_tracks
import json


#TODO test
def search_for_tracks(spotify, username, query):
    """Returns a list of tracks for the given query"""

    json_response = spotify.search(q=query)
    logging.debug("All search results for query " + query + ": " + json.dumps(json_response))

    converted_tracks = []
    if json_response['tracks']:
        converted_tracks = parse_tracks(json_response['tracks']['items'])
    logging.info("Track results for query " + query + ": " + str(converted_tracks))
    return converted_tracks