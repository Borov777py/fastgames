from logging import getLogger
from typing import Any
from socket import socket, AF_INET, SOCK_STREAM
from json import loads, dumps
from threading import Thread
from time import sleep

from .dispatcher import Dispatcher


logger = getLogger(name=__name__)


class _Client:
    def __init__(self, client_data: tuple[socket, Any]):
        self.__socket, self.__address = client_data

        logger.info(f"New connect: {self.__address}")

    def __call__(self, dispatcher: Dispatcher) -> None:
        """Клиентский цикл, который открыт в отдельном потоке"""
        while True:
            try:
                data = loads(self.__socket.recv(1024).decode('UTF-8'))
            except BlockingIOError:
                continue
            except Exception:
                logger.warning("Error when receiving data from the client")
                break

            try:
                result = dispatcher.handle_data(data=data)
            except Exception:
                logger.warning("Client data processing error")
                break

            try:
                self.__socket.sendall(bytes(dumps(result), 'UTF-8'))
            except Exception:
                logger.warning("Error when sending data to the client")
                break

        self.__socket.close()
        logger.info(f'Disconnect: {self.__address}')


class Server:
    def __init__(self, ip_address: tuple[str, int]):
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind(ip_address)
        self.__socket.listen(10)
        self.__socket.setblocking(False)

        logger.info(f"Create server: {ip_address}")

    def get_clients(self, dispatcher: Dispatcher) -> None:
        """Ожидает подключения к серверу и запускает отдельный поток для клиента"""
        try:
            while True:
                try:
                    Thread(
                        target=_Client(client_data=self.__socket.accept()),
                        args=(dispatcher,)
                    ).start()
                except BlockingIOError:
                    sleep(0.1)
        except KeyboardInterrupt:
            self.__socket.close()
            logger.info(f"Close server...")
