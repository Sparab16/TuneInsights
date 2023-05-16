import json


class ConfigIO:

    spotify_connect_file = "configs/authorization/spotify_connect.json"
    token_file = "configs/authorization/token.json"
    kafka_connect_creds_file = "configs/authorization/kafka_connect_creds.json"

    @staticmethod
    def read_json(file_path):
        with open(file_path) as file:
            return json.loads(file.read())

    @staticmethod
    def write_json(json_val, file_path):
        with open(file_path, 'w') as file:
            json.dump(json_val, file, ensure_ascii=False, indent=4)
