import requests

from utils.config_mgmt.config_io import ConfigIO


class SpotifyPlayer:

    @staticmethod
    def get_playback_state():
        """
        Get information about the user’s current playback state, including track or episode, progress, and active device
        :return: None
        """
        token_data = ConfigIO.read_json(ConfigIO.token_file)

        api_url = "https://api.spotify.com/v1/me/player"

        headers = {
            "Authorization": f"Bearer {token_data['access_token']}"
        }

        try:
            while True:
                response = requests.get(url=api_url, headers=headers)

                if response.status_code == 204:
                    print('Playback not available')
                else:
                    playback_data = response.json()
                    print(type(playback_data), playback_data)

        except KeyboardInterrupt:
            pass


