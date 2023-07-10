import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from connection import Connection

load_dotenv()


class Api(ABC):
    api_host = os.getenv("LINKUP_API_HOST")
    _headers = {
        "Content-Type": "application/json",
        "Product": os.getenv("LINKUP_PRODUCT"),
        "User-Agent": os.getenv("LINKUP_USER_AGENT")
    }

    def __init__(self):
        self.token = ''

    def store_ticket(self, ticket: dict):
        ...

    def load_ticket(self):
        ...

    def get_headers(self, auth: bool = True) -> dict:
        headers = self._headers
        if self.token and auth:
            headers["Authorization"] = "Bearer " + self.token
        if "Version" not in self._headers:
            self._headers["Version"] = self.get_min_version()
        return headers

    @abstractmethod
    def get_min_version(self) -> str:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def get_connections(self) -> Connection:
        pass

    @abstractmethod
    def get_graph(self, connection_id: str) -> dict:
        pass
