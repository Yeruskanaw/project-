import socket
import threading
from contextlib import closing

# Define the server's address and port
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to bind the server to
MAX_CONNECTIONS = 5 # the max number of active connections at once
active_connections = 0 # the number of how much connections are now active
lock = threading.Lock() # sync access to active active_connections

def handle_client(client_socket, client_address):
    """Handle the communication with the connected client."""
    global active_connections
    print(f"New connection from {client_address}")
    with lock:
        active_connections+=1 # adding 1 to active connection when a new connection occurs
    print ( f"active connections: {active_connections}\n" )

    try:
        # Send a welcome message to the client
        client_socket.sendall(b"Welcome to the server!")

        while True:
            # Receive data from the client
            data = client_socket.recv(1024)

            if not data:
                # If no data is received, break the loop and close the connection
                print(f"Connection closed by {client_address}")
                break

            print(f"Received from {client_address}: {data.decode()}")
            response = f"Echoing: {data.decode()}"
            client_socket.sendall(response.encode())  # Send a response back to the client

# handling errors with clients connections
    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        # Close the client connection
        client_socket.close() # closing the interrupted connection with client
        with lock:
            active_connections-=1 # lowering the num of active connections
        # print the current connections num
        print(f"active connections: {active_connections}")


def start_server():
    """Start the TCP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the server socket to the address and port
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CONNECTIONS) # added the MAX_CONNECTIONS so the server could listen up to 5 clients at the same time

        print(f"Server started, listening on {HOST}:{PORT}...")

        while True:
            # Accept new client connections
            client_socket, client_address = server_socket.accept()

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_server()
