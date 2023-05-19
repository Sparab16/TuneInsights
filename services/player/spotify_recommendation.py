import requests
from utils.config_mgmt.config_io import ConfigIO


class SpotifyRecommendation:
    @staticmethod
    def _get_artist_ids(record):
        """
        Extracts the artist IDs from the record.

        Args:
            record (dict): The record containing artist information.

        Returns:
            list: A list of artist IDs.
        """
        artists_list = record['item']['artists']
        artist_ids = [artist['id'] for artist in artists_list]
        return artist_ids

    @staticmethod
    def _get_track_id(record):
        """
        Extracts the track ID from the record.

        Args:
            record (dict): The record containing track information.

        Returns:
            str: The track ID.
        """
        return record['item']['id']

    @staticmethod
    def _create_recommended_pairs(recommended_data):
        """
        Creates a dictionary of recommended song pairs.

        Args:
            recommended_data (dict): The recommended song data.

        Returns:
            dict: A dictionary of recommended song pairs.
        """
        recommendations = []

        for track in recommended_data['tracks']:
            if track['name'] != '':
                recommendations.append({
                    'name': track['name'],
                    'spotify_link': track['external_urls']['spotify'],
                    'popularity': track['popularity'],
                    'album_name': track['album']['name']
                })

        return {'recommendations': recommendations}

    @staticmethod
    def recommend_song(record):
        """
        Recommends songs based on the given record.

        Args:
            record (dict): The record containing artist and track information.

        Returns:
            dict: A dictionary of recommended song pairs.
        """

        # Read token configuration
        token_data = ConfigIO.read_json(ConfigIO.token_file)

        # Get artist and track IDs from the record
        seed_artists = SpotifyRecommendation._get_artist_ids(record)
        seed_tracks = SpotifyRecommendation._get_track_id(record)

        api_url = "https://api.spotify.com/v1/recommendations"
        headers = {
            "Authorization": f"Bearer {token_data['access_token']}"
        }

        query_params = {
            'limit': 5,
            'seed_artists': seed_artists,
            'seed_tracks': seed_tracks
        }

        response = requests.get(url=api_url, params=query_params, headers=headers)

        if response.status_code == 200:
            recommended_data = response.json()
            return SpotifyRecommendation._create_recommended_pairs(recommended_data)

