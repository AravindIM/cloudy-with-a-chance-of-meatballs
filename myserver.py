"""Run the server."""

import socket
import time
from threading import Thread


def fib(n):
    """Calculate fibonacci of n."""
    a = 0
    b = 1
    if n < 1:
        return a
    elif n == 1:
        return b
    for i in range(1, n):
        c = a + b
        a = b
        b = c
    return b


def server_operation(connection=None, buffer_size=2048):
    """Run operations on accepting connection till the time specified."""
    time_interval = float(connection.recv(buffer_size).decode())
    current_time = time.time()
    end_time = current_time + time_interval
    while current_time < end_time:
        fib(5)
        current_time = time.time()
    connection.send("DONE".encode())


class Server:
    """Creates the server and provides functions to run it."""

    def __init__(self, address, port, buffer_size, max_listen=5):
        """Init the server properties."""
        self.address = address
        self.port = port
        self.buffer_size = buffer_size
        self.max_listen = max_listen
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, handle_connected):
        """Bind to the port and start listening."""
        self._socket.bind(self.address, self.port)
        self._socket.listen(self.max_listen)
        while True:
            conn, cl_addr = self._socket.accept()
            currConnThread = Thread(target=self.handle_connected,
                                    args=(conn, cl_addr, self.buffer_size))
            currConnThread.start()


def main():
    """Run the code."""
    server = Server("0.0.0.0", 8008, 2048)
    server.start(server_operation)


if __name__ == "__main__":
    main()
