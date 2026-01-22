import socket
import threading

# Server address and port
HOST = '127.0.0.1'
PORT = 65432

def simulate_client():
    """Simulate a client connecting to the server."""
    try:
        with socket.socket ( socket.AF_INET, socket.SOCK_STREAM ) as client_socket:
            client_socket.connect ( (HOST, PORT) )

            # Receive welcome message from server
            welcome_message = client_socket.recv ( 1024 )
            print ( f"Received from server: {welcome_message.decode ()}" )
            # Send a test message
            client_socket.sendall ( b"Hello from client!" )
            response = client_socket.recv ( 1024 )
            print ( f"Received from server: {response.decode ()}" )

    # handling errors
    except ConnectionRefusedError:  # refused connection error
        print ( "Error: Could not connect to the server. Is the server running?" )
    except ConnectionResetError:  # connection unexpectedly closed error
        print ( "Error: Connection was unexpectedly closed by the server." )
    except Exception as e:  # other errors that may occur + adding the error number\ message
        print ( f"An unexpected error occurred: {e}" )

# adding more clients at once - up to  5
if __name__ == "__main__":
    threads = []
    for i in range ( 5 ):  # Simulate 5 clients
        t = threading.Thread ( target=simulate_client )
        t.start ()
        threads.append ( t )

    for t in threads:
        t.join ()
