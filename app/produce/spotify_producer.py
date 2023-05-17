from kafka import KafkaProducer

from utils.config_mgmt.config_io import ConfigIO


class SpotifyProducer:
    """
    SpotifyProducer class for producing messages to Kafka topics.
    """

    def __init__(self):
        """
        Initializes the SpotifyProducer class and creates a KafkaProducer instance.
        """
        self.producer = KafkaProducer(**SpotifyProducer.get_config())

    @staticmethod
    def get_config():
        """
        Retrieves Kafka configuration from the config file.

        Returns:
            dict: Kafka configuration dictionary.
        """
        kafka_connect_creds_data = ConfigIO.read_json(ConfigIO.kafka_connect_creds_file)

        config = dict()

        # Kafka server connection configs
        config['bootstrap_servers'] = kafka_connect_creds_data["bootstrap_servers"]
        config["security_protocol"] = "SASL_SSL"
        config["sasl_mechanism"] = "PLAIN"
        config["sasl_plain_username"] = kafka_connect_creds_data["sasl_plain_username"]
        config["sasl_plain_password"] = kafka_connect_creds_data["sasl_plain_password"]

        # # Data serialization configs
        config["key_serializer"] = str.encode
        # config["value_serializer"] = bytes

        return config

    def send_data(self, topic_name, key, value):
        """
        Sends a message to the specified Kafka topic.

        Args:
            topic_name (str): Name of the Kafka topic.
            key: Key for the message.
            value: Value of the message.

        Returns:
            None
        """
        self.producer.send(topic=topic_name, key=key, value=value)

    def stop(self):
        try:
            self.producer.close()
        except Exception as e:
            print(e)
