import requests
from utils.config_mgmt.config_io import ConfigIO
from utils.logging.logger import Logger

logger = Logger('logs/spotify_recommendation.log')


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
        try:
            artists_list = record['item']['artists']
            artist_ids = [artist['id'] for artist in artists_list]
            return artist_ids
        except Exception as e:
            logger.error(f"Failed to retrieve artists id from record with following error: {str(e)}")

    @staticmethod
    def _get_track_id(record):
        """
        Extracts the track ID from the record.

        Args:
            record (dict): The record containing track information.

        Returns:
            str: The track ID.
        """
        try:
            return record['item']['id']
        except Exception as e:
            logger.error(f"Failed to retrieve id from record with following error: {str(e)}")

    @staticmethod
    def _create_recommended_pairs(recommended_data):
        """
        Creates a dictionary of recommended song pairs.

        Args:
            recommended_data (dict): The recommended song data.

        Returns:
            dict: A dictionary of recommended song pairs.
        """
        try:
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
        except Exception as e:
            logger.error(f"Failed to create recommended pairs due to following error: {str(e)}")

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

        try:
            response = requests.get(url=api_url, params=query_params, headers=headers)

            if response.status_code == 200:
                recommended_data = response.json()
                return SpotifyRecommendation._create_recommended_pairs(recommended_data)
            else:
                logger.error(f"Failed to retrieve recommendations. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to recommend songs with the following error: {str(e)}")

        return None
