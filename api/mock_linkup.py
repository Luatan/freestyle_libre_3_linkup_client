import json

from api.api import Api
from connection import Connection


class MockLinkup(Api):

    def __init__(self):
        super().__init__()
        print("Using Mock Class - No Api Calls are made")

    def login(self, username, password):
        if self.token:
            return
        response_data = json.load(open("api/mock_response/login.json", "r"))
        headers = self.get_headers()
        self.token = response_data["data"]["authTicket"]["token"]
        return response_data

    def get_connections(self) -> Connection:
        response_data = json.load(open("api/mock_response/get_connections.json", "r"))
        headers = self.get_headers()
        connection = response_data['data'][0]
        json_data = response_data['data'][0]
        return Connection(json_data['patientId'], json_data['country'], json_data['firstName'],
                          json_data['lastName'],
                          json_data['targetLow'], json_data['targetHigh'])

    def get_graph(self, connection_id):
        response_data = json.load(open("api/mock_response/get_graph.json", "r"))
        headers = self.get_headers()
        return response_data['data']['graphData']

    def get_min_version(self) -> str:
        response_data = json.load(open("api/mock_response/get_config_base.json", "r"))
        return response_data['data']['minVersion']
