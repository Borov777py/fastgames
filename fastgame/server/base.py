from logging import getLogger
from typing import Any
from socket import socket, AF_INET, SOCK_STREAM
from json import loads, dumps
from threading import Thread

from .dispatcher import Dispatcher
from .models import RequestModel


logger = getLogger(name=__name__)


class Client:
    def __init__(self, client_data: tuple[socket, Any]):
        self.__socket, self.__address = client_data

        logger.info(f"New connection: {self.__address}")

    def __get_data(self) -> Any:
        """Получение данных от клиента"""
        return loads(self.__socket.recv(1024).decode('UTF-8'))

    def __send_data(self, response: Any) -> None:
        """Отправка данных клиенту"""
        return self.__socket.sendall(bytes(dumps(response), 'UTF-8'))

    def loop(self, dispatcher: Dispatcher):
        """Клиентский цикл, который открыт в отдельном потоке"""
        while True:
            try:
                requests: list[RequestModel] = [RequestModel(**data) for data in self.__get_data()]
            except Exception:
                self.__socket.close()
                logger.info(f'Disconnect: {self.__address}')
                break

            response: dict[str, Any] = dispatcher.handle_requests(requests=requests)

            self.__send_data(response=response)



class Server:
    def __init__(self, ip_address: tuple[str, int]):
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind(ip_address)
        self.__socket.listen(10)

        logger.info(f"Create server: {ip_address}")

    def get_clients(self, dispatcher: Dispatcher) -> None:
        """Ожидает подключения к серверу и запускает отдельный поток для клиента"""
        while True:
            client = Client(
                client_data=self.__socket.accept()
            )

            Thread(
                target=client.loop,
                args=(dispatcher, )
            ).start()
