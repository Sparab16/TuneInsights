import json
import struct

from kafka import KafkaConsumer
from utils.config_mgmt.config_io import ConfigIO


class SpotifyConsumer:

    def __init__(self, topic, consumer_group_id):
        self.consumer = KafkaConsumer(topic, group_id=consumer_group_id, **SpotifyConsumer.get_config())

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
        config["key_deserializer"] = bytes.decode
        config["value_deserializer"] = bytes.decode

        # Consumer Group
        config["auto_offset_reset"] = "latest"

        return config

    def consume_data(self):

        records_dict = self.consumer.poll(timeout_ms=2000, max_records=10000)

        records_list = list(
            records_dict.values())

        if len(records_list) > 0:

            records_list = records_list[0]  # Get the list of records

            for record in records_list:
                cleaned_value = record.value.replace("\x00", '{}')  # In some cases we were seeing value='\x00'
                # which is causing problems

                json_doc = json.loads(cleaned_value)

                if len(json_doc.items()) > 0:
                    print(record.partition, record.offset, json_doc)
        else:
            print("No records exist at time. Will check for new records in 2 seconds..")

    def stop(self):
        try:
            self.consumer.close()
        except Exception as e:
            print(e)
