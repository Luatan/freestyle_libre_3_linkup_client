import json
import logging

import requests

from api.api import Api
from connection import Connection


class Linkup(Api):

    def __init__(self):
        super().__init__()
        print(f"Using the real thing - Api calls are made to {self.api_host}")

    def login(self, username, password):
        if self.token:
            return
        data = {
            "email": username,
            "password": password
        }
        response = requests.post(self.api_host + "/auth/login", json=data, headers=self.get_headers(False))
        if response.status_code != 200:
            logging.error(response.content)
            exit(1)
        response_data = json.loads(response.content)
        if "error" in response_data:
            logging.error(response_data["error"])
            exit(1)
        self.token = response_data["data"]["authTicket"]["token"]
        print(self.token)
        return response_data

    def get_min_version(self) -> str:
        response = requests.get(self.api_host + "/config/base", headers=self._headers)
        if response.status_code != 200:
            logging.error(response.content)
            exit(1)
        response_data = json.loads(response.content)
        return response_data['data']['minVersion']

    def get_connections(self) -> Connection:
        response = requests.get(self.api_host + "/connections", headers=self.get_headers())
        if response.status_code != 200:
            logging.error(response.content)
            exit(1)
        response_data = json.loads(response.content)
        json_data = response_data['data'][0]
        return Connection(json_data['patientId'], json_data['country'], json_data['firstName'],
                          json_data['lastName'],
                          json_data['targetLow'], json_data['targetHigh'])

    def get_graph(self, patient_id) -> dict:
        response = requests.get(self.api_host + "/connections/" + patient_id + "/graph", headers=self.get_headers())
        if response.status_code != 200:
            logging.error(response.content)
            exit(1)
        response_data = json.loads(response.content)
        return response_data['data']['graphData']
