import unittest
from unittest.mock import patch
from lastipy.lastfm.library import recent_tracks
from unittest.mock import Mock
from requests import HTTPError
from lastipy.track import Track 


class RecentArtistsTest(unittest.TestCase):

    dummy_user = 'dummyUser'
    dummy_api_key = '123456789'

    @patch('requests.get')
    def test_fetch_single_page(self, mock_requests_get):
        expected_tracks = [
            Track(track_name='Strawberry Fields Forever', artist='The Beatles'),
            Track(track_name='Badge', artist='Cream')
        ]

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'recenttracks': {
                'track': [
                    {
                        'name': 'Strawberry Fields Forever',
                        'artist': {
                            'name': 'The Beatles'  
                        } 
                    },
                    {
                        'name': 'Badge',
                        'artist': {
                            'name': 'Cream'
                        }
                    }
                ],
                '@attr': {
                    'totalPages': '1'
                }
            }
        }
        mock_requests_get.side_effect = [mock_response]

        fetched_tracks = recent_tracks.fetch_recent_tracks(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertCountEqual(fetched_tracks, expected_tracks)

    # @patch('requests.get')
    # def test_fetch_multiple_pages(self, mock_requests_get):
    #     expected_artists = [
    #         ScrobbledArtist(artist_name='Bee Gees', playcount=5),
    #         ScrobbledArtist(artist_name='The Beatles', playcount=10),
    #         ScrobbledArtist(artist_name='Cream', playcount=15)
    #     ]

    #     mock_responses = [Mock(), Mock(), Mock()]
    #     mock_responses[0].ok = True
    #     mock_responses[0].json.return_value = self._build_artist_json_response('Bee Gees', '5', '3')
    #     mock_responses[1].ok = True
    #     mock_responses[1].json.return_value = self._build_artist_json_response('The Beatles', '10', '3')
    #     mock_responses[2].ok = True
    #     mock_responses[2].json.return_value = self._build_artist_json_response('Cream', '15', '3')
    #     mock_requests_get.side_effect = mock_responses

    #     fetched_artists = recent_artists.fetch_recent_artists(user=self.dummy_user, api_key=self.dummy_api_key)

    #     self.assertCountEqual(fetched_artists, expected_artists)

    # @patch('requests.get')
    # def test_fetch_with_success_after_retries(self, mock_requests_get):
    #     expected_artists = [
    #         ScrobbledArtist(artist_name='Bee Gees', playcount=5),
    #         ScrobbledArtist(artist_name='Cream', playcount=15)
    #     ]

    #     mock_responses = [Mock(), Mock(), Mock()]
    #     mock_responses[0].ok = True
    #     mock_responses[0].json.return_value = self._build_artist_json_response('Bee Gees', '5', '2')
    #     mock_responses[1].ok = False
    #     mock_responses[1].raise_for_status.side_effect = HTTPError(Mock(status=500), 'Error')
    #     mock_responses[2].ok = True
    #     mock_responses[2].json.return_value = self._build_artist_json_response('Cream', '15', '2')
    #     mock_requests_get.side_effect = mock_responses

    #     fetched_artists = recent_artists.fetch_recent_artists(user=self.dummy_user, api_key=self.dummy_api_key)

    #     self.assertCountEqual(fetched_artists, expected_artists)
    
    # @patch('requests.get')
    # def test_fetch_fails_after_retries(self, mock_requests_get):
    #     mock_responses = []
    #     for _ in range(10):
    #         mock_response = Mock()
    #         mock_response.ok = False
    #         mock_response.raise_for_status.side_effect = HTTPError(Mock(status=500), 'Error')
    #         mock_responses.append(mock_response)

    #     # Add another mock response, but the code will exit after the retry limit is reached and this won't actually get fetched
    #     mock_response = Mock()
    #     mock_response.ok = False
    #     mock_response.json.return_value = self._build_artist_json_response('Cream', '15', '1')

    #     fetched_artists = recent_artists.fetch_recent_artists(user=self.dummy_user, api_key=self.dummy_api_key)

    #     self.assertEqual(fetched_artists, [])

    # def _build_artist_json_response(self, artist_name, playcount, total_pages):
    #     return { 'artists': { 'artist': [ { 'name': artist_name, 'playcount': playcount } ], '@attr': { 'totalPages': total_pages } } }