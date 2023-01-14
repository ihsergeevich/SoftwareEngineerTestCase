import unittest

import orjson
from websocket import create_connection

from config import Config


class TestWebsocket(unittest.TestCase):
    GOOD_DATA = [[{'timestamp': '2021-12-01T00:00:00.004000', 'price': 47466000, 'volume': 394000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47471000, 'volume': 5279000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47469000, 'volume': 5865000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47469000, 'volume': 2078000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47467000, 'volume': 5052000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47467000, 'volume': 30527000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47467000, 'volume': 113000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47471000, 'volume': 4812000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47466000, 'volume': 5217000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47465000, 'volume': 28696000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47465000, 'volume': 6000000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47463000, 'volume': 3000000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47463000, 'volume': 2078000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47461000, 'volume': 164000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47460000, 'volume': 423000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47460000, 'volume': 2078000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47466000, 'volume': 2078000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                  {'timestamp': '2021-12-01T00:00:00.004000', 'price': 47471000, 'volume': 212000000000,
                   'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:00.046000', 'price': 47463000, 'volume': 7579000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:00.072000', 'price': 47470000, 'volume': 1524000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:00.073000', 'price': 47470000, 'volume': 9208000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.073000', 'price': 47470000, 'volume': 713000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.073000', 'price': 47470000, 'volume': 7314000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.073000', 'price': 47470000, 'volume': 7102000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:00.074000', 'price': 47471000, 'volume': 8227000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:00.115000', 'price': 47474000, 'volume': 9000000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.115000', 'price': 47474000, 'volume': 948000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.115000', 'price': 47475000, 'volume': 2078000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.115000', 'price': 47477000, 'volume': 5852000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:00.115000', 'price': 47477000, 'volume': 12213000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:03.724000', 'price': 47476000, 'volume': 345000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.051000', 'price': 47477000, 'volume': 33395000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.060000', 'price': 47477000, 'volume': 12204000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.068000', 'price': 47477000, 'volume': 31445000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.068000', 'price': 47476000, 'volume': 28389000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.068000', 'price': 47474000, 'volume': 345000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.081000', 'price': 47477000, 'volume': 5874000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47484000, 'volume': 4000000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47485000, 'volume': 5212000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47483000, 'volume': 32402000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47484000, 'volume': 271000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47485000, 'volume': 150000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47484000, 'volume': 2078000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47487000, 'volume': 2078000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47487000, 'volume': 23387000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47487000, 'volume': 52875000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47483000, 'volume': 20875000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47486000, 'volume': 632000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47482000, 'volume': 784000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47481000, 'volume': 2078000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47478000, 'volume': 900000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47477000, 'volume': 4869000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47478000, 'volume': 131000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47478000, 'volume': 2078000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47479000, 'volume': 632000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47478000, 'volume': 250000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47480000, 'volume': 912000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47482000, 'volume': 3187000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47480000, 'volume': 8000000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47480000, 'volume': 121000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.093000', 'price': 47480000, 'volume': 2090000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.101000', 'price': 47474000, 'volume': 421000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.138000', 'price': 47475000, 'volume': 15542000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.138000', 'price': 47475000, 'volume': 482000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.138000', 'price': 47476000, 'volume': 26141000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.148000', 'price': 47483000, 'volume': 38281000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.148000', 'price': 47487000, 'volume': 36419000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.158000', 'price': 47476000, 'volume': 882000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.158000', 'price': 47487000, 'volume': 20214000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.190000', 'price': 47474000, 'volume': 2391000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.202000', 'price': 47474000, 'volume': 3895000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}], [
                     {'timestamp': '2021-12-01T00:00:04.220000', 'price': 47474000, 'volume': 57590000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'},
                     {'timestamp': '2021-12-01T00:00:04.220000', 'price': 47474000, 'volume': 1566000000000,
                      'ticker': '1000SHIB-USDT-SWAP@BINANCE'}]]

    DATA_FROM_SERVER = []
    WS_CLIENT = None

    def setUp(self) -> None:
        self.WS_CLIENT = create_connection(f"ws://websocket:{Config.WEBSOCKET_PORT}")
        self.prepare_data_from_server()

    def tearDown(self) -> None:
        self.WS_CLIENT.close()

    def prepare_data_from_server(self):
        while True:
            if not self.DATA_FROM_SERVER:
                self.DATA_FROM_SERVER = [orjson.loads(self.WS_CLIENT.recv())]
            else:
                self.DATA_FROM_SERVER.append(orjson.loads(self.WS_CLIENT.recv()))

            if len(self.GOOD_DATA) == len(self.DATA_FROM_SERVER):
                break

    def test_correct_order_data(self):
        for i in range(len(self.GOOD_DATA)):
            assert self.DATA_FROM_SERVER[i] == self.GOOD_DATA[i], (self.DATA_FROM_SERVER[i], self.GOOD_DATA[i])

            for a in range(1, len(self.DATA_FROM_SERVER[i])):
                assert self.DATA_FROM_SERVER[i][a - 1]['timestamp'] >= self.DATA_FROM_SERVER[i][a]['timestamp'], \
                    (self.DATA_FROM_SERVER[i][a - 1]['timestamp'], self.DATA_FROM_SERVER[i][a]['timestamp'])
