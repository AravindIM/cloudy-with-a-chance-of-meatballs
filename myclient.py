"""Run the client."""

import socket
import sys
from threading import Thread

SERVER_IP = "192.168.122.2"
SERVER_PORT = 8008
BUFFER_SIZE = 2048


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
        self._socket.send(message.encode())

    def response(self):
        """Recieve response from the server."""
        return self._socket.recv(self.buffer_size).decode()

def handle_connected(client,busy_time):
    """ Send request and recieve reesponse from Server """
    try:
        print("Connecting to server [OK]")
        client.request(busy_time)
        print("Sending message to server [OK]")
        response = client.response()
        print("Recieved response from server [OK]")
        print(f"Response: {response}")
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    """Run the code."""
    try :
        busy_time = sys.argv[1]
    except Exception as error :
        print(f"Error parsing command line arguments : {error}")
    while True :
        client = Client(SERVER_IP, SERVER_PORT, BUFFER_SIZE)
        client.connect()
        Thread(target=handle_connected, args=(client,busy_time))



if __name__ == "__main__":
    main()
