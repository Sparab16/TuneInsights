import requests
import time
import json

from utils.config_mgmt.config_io import ConfigIO
from app.produce.spotify_producer import SpotifyProducer


class SpotifyPlayer:
    """
    SpotifyPlayer class for retrieving information about the user's current playback state from Spotify API.
    """

    @staticmethod
    def get_playback_state():
        """
        Retrieves information about the user's current playback state, including track or episode, progress, and active device.

        Returns:
            None
        """

        # Initialize Producer
        producer = SpotifyProducer()

        # Read token configuration
        token_data = ConfigIO.read_json(ConfigIO.token_file)

        api_url = "https://api.spotify.com/v1/me/player"

        headers = {
            "Authorization": f"Bearer {token_data['access_token']}"
        }

        try:
            while True:
                response = requests.get(url=api_url, headers=headers)

                if response.status_code == 200:
                    playback_data = response.json()

                    # Send data to kafka topic
                    producer.send_data(topic_name='playback_player',
                                            value=json.dumps(response.json()),
                                            key=playback_data['device']['id'])
                    print(playback_data)
                # time.sleep(2)

        except KeyboardInterrupt:
            pass
        except requests.exceptions.RequestException as e:
            print("Error Occurred during API request: ", str(e))
        except Exception as e:
            print("Error Occurred: ", str(e))
