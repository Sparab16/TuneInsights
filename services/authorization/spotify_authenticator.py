import base64
import json
import urllib.parse
import requests
import webbrowser
from utils.logging.logger import Logger
from utils.config_mgmt.config_io import ConfigIO

logger = Logger('logs/spotify_authenticator.log')


class SpotifyAuthenticator:
    """
    A class for authenticating with the Spotify API.
    """

    @staticmethod
    def get_auth_token():
        """
        Get the authorization token from the user and update the token file.
        """
        try:
            spotify_connect_data = ConfigIO.read_json(ConfigIO.spotify_connect_file)

            authorize_url = 'https://accounts.spotify.com/authorize?'

            auth_url = authorize_url + urllib.parse.urlencode({
                'response_type': 'code',
                'client_id': spotify_connect_data["client_id"],
                'scope': spotify_connect_data["scopes"],
                'redirect_uri': spotify_connect_data["redirect_uri"],
            })

            webbrowser.open_new(url=auth_url)

            authorization_code = input('Enter the authorization code from the redirect URI: ')

            token_data = ConfigIO.read_json(ConfigIO.token_file)
            token_data["auth_token"] = authorization_code
            ConfigIO.write_json(token_data, ConfigIO.token_file)

            logger.info("Authentication token successfully updated")
        except Exception as e:
            logger.error(f"Failed to get the authorization token with the following error: {str(e)}")

    @staticmethod
    def get_access_token():
        """
        Get the access token using the authorization code and update the token file.
        """
        try:
            spotify_connect_data = ConfigIO.read_json(ConfigIO.spotify_connect_file)
            token_data = ConfigIO.read_json(ConfigIO.token_file)

            access_url = "https://accounts.spotify.com/api/token"

            data = {
                "grant_type": "authorization_code",
                "code": token_data["auth_token"],
                "redirect_uri": spotify_connect_data["redirect_uri"]
            }

            client_credentials = f"{spotify_connect_data['client_id']}:{spotify_connect_data['client_secret']}"

            headers = {
                "Authorization": "Basic " + base64.b64encode(client_credentials.encode("utf-8")).decode("utf-8")
            }

            response = requests.post(url=access_url, data=data, headers=headers)

            access_response = json.loads(response.content.decode("utf-8"))

            token_data["access_token"] = access_response["access_token"]
            token_data["refresh_token"] = access_response["refresh_token"]

            ConfigIO.write_json(token_data, ConfigIO.token_file)

            logger.info("Access token successfully updated")
        except Exception as e:
            logger.error(f"Failed to get the access token with the following error: {str(e)}")

    @staticmethod
    def get_refresh_token():
        """
        Refresh the access token using the refresh token and update the token file.
        """
        try:
            spotify_connect_data = ConfigIO.read_json(ConfigIO.spotify_connect_file)
            token_data = ConfigIO.read_json(ConfigIO.token_file)

            access_url = "https://accounts.spotify.com/api/token"

            data = {
                "grant_type": "refresh_token",
                "refresh_token": token_data["refresh_token"]
            }

            client_credentials = f"{spotify_connect_data['client_id']}:{spotify_connect_data['client_secret']}"

            headers = {
                "Authorization": "Basic " + base64.b64encode(client_credentials.encode("utf-8")).decode("utf-8")
            }

            response = requests.post(url=access_url, data=data, headers=headers)

            access_response = json.loads(response.content.decode("utf-8"))
            token_data["access_token"] = access_response["access_token"]

            ConfigIO.write_json(token_data, ConfigIO.token_file)

            logger.info("Refresh token successfully updated")
        except Exception as e:
            logger.error(f"Failed to refresh the access token with the following error: {str(e)}")
