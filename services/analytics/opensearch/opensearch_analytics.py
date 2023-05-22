from utils.logging.logger import Logger

from opensearchpy import OpenSearch
from utils.config_mgmt.config_io import ConfigIO

logger = Logger('logs/opensearch_analytics.log')


class OpenSearchClient:
    """
    A class representing an OpenSearch client.

    It provides methods for creating an index and indexing documents in OpenSearch.
    """

    def __init__(self):
        """
        Initialize the OpenSearch client and authenticate with the provided credentials.
        """
        opensearch_connect_data = ConfigIO.read_json(ConfigIO.opensearch_connect_creds_file)
        try:
            # Create the OpenSearch client with the provided credentials
            self.client = OpenSearch(
                hosts=[{"host": opensearch_connect_data["host"], "port": opensearch_connect_data["port"]}],
                http_auth=opensearch_connect_data["auth"],
                use_ssl=True
            )
            logger.info(f'Client authenticated with status {self.client.ping()}')
        except Exception as e:
            logger.error(f"Client is not able to authenticate with the following error: {str(e)}")

    def create_index(self, index_name):
        """
        Create an index in OpenSearch if it doesn't already exist.

        :param index_name: The name of the index to create.
        """
        try:
            # Check if the index already exists
            is_index_exist = self.client.indices.exists(index_name)

            if not is_index_exist:
                # Create the index if it doesn't exist
                self.client.indices.create(index_name)
                logger.info(f"Index '{index_name}' is created successfully")
            else:
                logger.info(f"Index '{index_name}' already exists")
        except Exception as e:
            logger.error(f"Error occurred while creating an index: {str(e)}")

    def index_document(self, index_name, json_doc, id):
        """
        Index a document in OpenSearch.

        :param index_name: The name of the index to insert the document into.
        :param json_doc: The JSON document to index.
        :param id: The unique identifier for the document.
        """
        try:
            # Index the document in OpenSearch
            self.client.index(
                index=index_name,
                body=json_doc,
                id=id
            )

            logger.info(f"Record '{id}' is inserted in the '{index_name}' index")
        except Exception as e:
            logger.error(f"Failed to insert the record due to the following error: {str(e)}")
