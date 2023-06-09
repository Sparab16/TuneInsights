import requests
import time
from utils.config_mgmt.config_io import ConfigIO
from app.produce.spotify_producer import SpotifyProducer
from services.authorization.spotify_authenticator import SpotifyAuthenticator
from utils.logging.logger import Logger

logger = Logger('logs/spotify_player.log')


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
                                       value=response.content,
                                       key=playback_data['device']['id'])
                    logger.info("Playback data successfully sent to Kafka topic")
                    print(playback_data)

                elif response.status_code == 401:
                    error = response.json()['error']['message']
                    if error == 'The access token expired':
                        SpotifyAuthenticator.get_refresh_token()
                        headers = {
                            "Authorization": f"Bearer {token_data['access_token']}"
                        }
                else:
                    print('Playback not there. Please start some track')

                time.sleep(0.5)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.error(f"Failed to get playback state with the following error: {str(e)}")
        finally:
            producer.stop()
            logger.info("Producer stopped")
