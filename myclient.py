#!/usr/bin/env python3

"""Run the client."""

import socket
import sys
from threading import Thread
import random
import time


SERVER_IP = "192.168.122.2"
SERVER_PORT = 8008
BUFFER_SIZE = 2048

ips = [SERVER_IP]


class Client:
    """Create the client and functions to connect with server."""

    def __init__(self, host, port, buffer_size=2048):
        """Initialize the client object with host, port and buffer_size."""
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect to the client object with host, and port."""
        self._socket.connect((self.host, self.port))

    def request(self, message):
        """Send request message to the server."""
        self._socket.send(f"{message}".encode())

    def response(self):
        """Recieve response from the server."""
        return self._socket.recv(self.buffer_size).decode()


def handle_connected(thread_num, busy_time):
    """Send request and recieve response from server."""
    global ips
    while True:
        time.sleep(1)
        try:
            client = Client(random.choice(ips), SERVER_PORT, BUFFER_SIZE)
            client.connect()
            print(f"[Thread{thread_num}]: Connecting to server {client.host} ... [OK]")
            client.request(busy_time)
            print(f"[Thread{thread_num}]: Sending message to server {client.host} ... [OK]")
            response = client.response()
            print(f"[Thread{thread_num}]: Recieved response from server {client.host} ... [OK]")
            print(f"[Thread{thread_num}]: Response from {client.host}: {response}")
        except Exception as e:
            print(f"ERROR: {e}")


def handle_autoscaler_connection():
    """Recieve information from autoscaler."""
    global ips
    autoscaler_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    autoscaler_socket.bind(("127.0.0.1", 6009))
    autoscaler_socket.listen(10)
    conn, _ = autoscaler_socket.accept()
    new_ip = conn.recv(BUFFER_SIZE).decode()
    print(f"[AUTOSCALER]: Recieved new ip: {new_ip}")
    ips.append(new_ip)


def main():
    """Run the code."""
    try:
        thread_count = int(sys.argv[1])
        busy_time = int(sys.argv[2])
        autoscalerThread = Thread(target=handle_autoscaler_connection)
        autoscalerThread.start()
        for i in range(thread_count):
            clientThread = Thread(target=handle_connected, args=(i+1, busy_time))
            clientThread.start()
    except Exception as error:
        print(f"ERROR: Please type thread count and busy time as arguments. {error}")


if __name__ == "__main__":
    main()
