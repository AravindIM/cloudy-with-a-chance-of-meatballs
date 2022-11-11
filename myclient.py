#!/usr/bin/env python3

"""Run the client."""

import socket
import sys
from threading import Thread


class Client:
    """Create the client and functions to connect with server."""

    def __init__(self, host, port, buffer_size=2048):
        """Initialize the client object with host, port and buffer_size."""
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect to the lient object with host, and port."""
        self._socket.connect((self.host, self.port))

    def request(self, message):
        """Send request message to the server."""
        self._socket.send(f"{message}".encode())

    def response(self):
        """Recieve response from the server."""
        return self._socket.recv(self.buffer_size).decode()


def handle_connected(thread_num, busy_time):
    """Send request and recieve response from server."""
    while True:
        try:
            client = Client("192.168.122.2", 8008)
            client.connect()
            print(f"[Thread{thread_num}]: Connecting to server [OK]")
            client.request(busy_time)
            print(f"[Thread{thread_num}]: Sending message to server [OK]")
            response = client.response()
            print(f"[Thread{thread_num}]: Recieved response from server [OK]")
            print(f"[Thread{thread_num}]: Response: {response}")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    """Run the code."""
    try:
        thread_count = int(sys.argv[1])
        busy_time = int(sys.argv[2])
        for i in range(thread_count):
            clientThread = Thread(target=handle_connected, args=(i+1, busy_time))
            clientThread.start()
    except Exception as error:
        print(f"Error parsing command line arguments : {error}")


if __name__ == "__main__":
    main()
