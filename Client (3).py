import socket

# Server address and port
HOST = '127.0.0.1'
PORT = 65432

def start_client():
    """Create a client that connects to the server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the server
            client_socket.connect((HOST, PORT))

            # Receive welcome message from server
            welcome_message = client_socket.recv(1024)
            print(f"Received from server: {welcome_message.decode()}")

            # Send some data to the server
            while True:
                message = input("Enter a message to send (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                client_socket.sendall(message.encode())

                # Receive and print the response from the server
                response = client_socket.recv(1024)
                print(f"Received from server: {response.decode()}")
    # handling problems in the connection of the client
    except ConnectionRefusedError: # refused connection error
        print("Error: Could not connect to the server. Is the server running?")
    except ConnectionResetError: # connection unexpectedly closed error
        print("Error: Connection was unexpectedly closed by the server.")
    except Exception as e: # other errors that may occur + adding the error number\ massage
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    start_client()

