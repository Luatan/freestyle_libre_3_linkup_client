import os

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

import glucose
from api.linkup import Linkup
from api.mock_linkup import MockLinkup
from connection import Connection

load_dotenv()


def create_dirs():
    if not os.path.exists("./dataStore"):
        os.mkdir("./dataStore")


def plot(data, low, high):
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df.Timestamp)
    print(df)
    df.plot(x='Timestamp', y='Value', color="black")
    # plt.axhline(glucose.to_mmol(high), color='r', ls='--', label='High')
    # plt.axhline(21, color='black', ls='-', )
    # plt.axhline(0, color='black', ls='-', )
    plt.axhspan(low, high, facecolor='green', alpha=0.3)
    plt.legend()
    plt.grid()
    plt.ylim([0, 21])
    plt.show()


def main():
    api = Linkup() if not os.getenv("LINKUP_MOCK_DATA").lower() == "true" else MockLinkup()
    api.login(os.getenv("LINKUP_USERNAME"), os.getenv("LINKUP_PASSWORD"))
    connection = api.get_connections()
    graph_data = api.get_graph(connection.patient_id)

    plot(graph_data, low=glucose.to_mmol(connection.target_low), high=glucose.to_mmol(connection.target_high))


if __name__ == '__main__':
    create_dirs()
    main()

