"""Run the client."""

import socket


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


def main():
    """Run the code."""
    try:
        busy_time = input("Num of seconds:")
        client = Client("192.168.122.2", 8008)
        client.connect()
        print("Connecting to server [OK]")
        client.request(busy_time)
        print("Sending message to server [OK]")
        response = client.response()
        print("Recieved response from server [OK]")
        print(f"Response: {response}")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
