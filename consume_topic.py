import uuid
import datetime

from app.consume.spotify_consumer import SpotifyConsumer
from services.analytics.opensearch.opensearch_analytics import OpenSearchClient

consumer = SpotifyConsumer(topic='playback_player', consumer_group_id='consumer_player')
opensearch = OpenSearchClient()

# Create index if not exist
opensearch.create_index('tune_insights')

try:
    while True:

        record = consumer.consume_data()

        if record:
            # Generate Random Unique ID for inserting  records
            unique_id = uuid.uuid4()

            # Convert epoch timestamp to datetime timestamp for further analytics support
            time_val = record['timestamp']//1000

            record['timestamp'] = datetime.datetime.fromtimestamp(time_val)

            opensearch.index_document(record, unique_id)

            print(f"Record {unique_id} is inserted in 'tune_insights' index")

except KeyboardInterrupt:
    pass
finally:
    consumer.stop()
    print("Consumer stopped...")
