from opensearchpy import OpenSearch
from utils.config_mgmt.config_io import ConfigIO


class OpenSearchClient:

    def __init__(self):

        opensearch_connect_data = ConfigIO.read_json(ConfigIO.opensearch_connect_creds_file)
        self.client = OpenSearch(
            hosts=[{"host": opensearch_connect_data["host"], "port": opensearch_connect_data["port"]}],
            http_auth=opensearch_connect_data["auth"],
            use_ssl=True
        )

        self.index_name = None

    def create_index(self, index_name):

        self.index_name = index_name

        is_index_exist = self.client.indices.exists(index_name)

        if not is_index_exist:

            self.client.indices.create(index_name)
            print(f"Index '{index_name}' is created successfully")
        else:
            print(f"Index '{index_name}' is already exist")

    def index_document(self, json_doc, id):

        self.client.index(
            index=self.index_name,
            body=json_doc,
            id=id
        )
