import uuid
import datetime

from app.consume.spotify_consumer import SpotifyConsumer
from services.analytics.opensearch.opensearch_analytics import OpenSearchClient
from services.player.spotify_recommendation import SpotifyRecommendation
from utils.logging.logger import Logger

logger = Logger('logs/spotify_data_processing.log')

consumer = SpotifyConsumer(topic='playback_player', consumer_group_id='consumer_player')
opensearch = OpenSearchClient()

# Create index if not exist
opensearch.create_index('tune_insights')
opensearch.create_index('tune_recommendation')

try:
    song_recommendation = {
        'current_song': '',
        'is_recommended': False
    }

    while True:
        record = consumer.consume_data()

        if record:
            if not song_recommendation['is_recommended']:  # If recommendation is False then recommend new song
                recommendations = SpotifyRecommendation.recommend_song(record)
                song_recommendation['current_song'] = record['item']['name']
                song_recommendation['is_recommended'] = True
            elif song_recommendation['current_song'] != record['item']['name']:  # If recommendation is True but it's a new song then recommend new song
                recommendations = SpotifyRecommendation.recommend_song(record)
                song_recommendation['current_song'] = record['item']['name']
            else:  # Else set recommendation to empty to avoid unnecessary insert
                recommendations = {}

            # Generate Random Unique ID for inserting records
            unique_id = uuid.uuid4()

            # Convert epoch timestamp to datetime timestamp for further analytics support
            time_val = record['timestamp'] // 1000
            record['timestamp'] = datetime.datetime.fromtimestamp(time_val)

            # Write track record to an Index
            opensearch.index_document('tune_insights', record, unique_id)

            # Write recommended record to an Index
            if recommendations:
                for index, recommend in enumerate(recommendations['recommendations']):
                    opensearch.index_document('tune_recommendation', recommend, f'recommendations_{index}')

            logger.info(f"Record {unique_id} is inserted in 'tune_insights' index")

except KeyboardInterrupt:
    pass

finally:
    consumer.stop()
    logger.info("Consumer stopped...")
