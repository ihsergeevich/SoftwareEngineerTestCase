import asyncio
import json
import traceback

import websockets
from websockets import WebSocketServerProtocol
import pandas as pd

from config import Config


class WebSocketServer:
    """
    Web-socket server
    """
    __slots__ = 'clients', 'host', 'port', 'df'

    def __init__(self, port, host='0.0.0.0'):
        """
        Init and prepare data
        """
        self.clients = set()
        self.host = host
        self.port = port
        self.__prepare_df()

    async def run(self) -> None:
        """
        Create websocket server
        :return:
        """
        async with websockets.serve(self.__ws_handler, self.host, self.port):
            await asyncio.Future()

    async def __register(self, ws: WebSocketServerProtocol) -> None:
        """
        Register new ws connect
        :param ws:
        :return:
        """
        self.clients.add(ws)

    async def __unregister(self, ws: WebSocketServerProtocol) -> None:
        """
        Unregister ws connect
        :param ws:
        :return:
        """
        self.clients.remove(ws)

    async def __send_to_client(self) -> None:
        """
        Checks for the presence of the client
        and runs data getter
        :return:
        """
        if self.clients:
            await self.__data_getter()

    def __prepare_df(self) -> None:
        """
        Prepare parquet data for a client
        :return:
        """
        df = pd.read_parquet('trades_sample.parquet', engine='fastparquet')
        self.df = df.sort_values('timestamp', ascending=True)

    async def __data_getter(self) -> None:
        """
        Get data from parquet file, group
        by timestamp and sand it to client
        :return:
        """
        data_list = []
        old_timestamp = None

        for _, data in self.df.iterrows():
            if old_timestamp and old_timestamp == data['timestamp']:
                data_list.append({
                    'timestamp': data['timestamp'].strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    'price': data['price'],
                    'volume': data['volume'],
                    'ticker': data['ticker'],
                })
            else:
                if data_list:
                    await asyncio.gather(
                        *[asyncio.create_task(client.send(json.dumps(data_list))) for client in self.clients])

                old_timestamp = data['timestamp']
                data_list = [{
                    'timestamp': data['timestamp'].strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    'price': data['price'],
                    'volume': data['volume'],
                    'ticker': data['ticker'],
                }]

    async def __ws_handler(self, ws: WebSocketServerProtocol) -> None:
        """
        Entry point to connect with websocket
        Register new ws clients
        Start send data
        Unregister client if he was disconnected or some else exception
        :param ws:
        :return:
        """
        await self.__register(ws)

        try:
            await self.__send_to_client()
        except Exception:
            await self.__unregister(ws)


if __name__ == '__main__':
    server = WebSocketServer(port=Config.WEBSOCKET_PORT)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(server.run())
        loop.run_forever()
    finally:
        loop.close()

