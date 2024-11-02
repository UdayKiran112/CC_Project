import socket
import threading
import math


def handle_client(client_socket):
    """Handles client requests."""
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break

        try:
            # Perform CPU-intensive task (e.g., factorial)
            num = int(request)
            result = math.factorial(
                num
            )  # Replace with other CPU-intensive work if needed
            response = f"Factorial of {num} is {result}"
        except ValueError:
            response = "Invalid input, please send a valid integer."

        client_socket.send(response.encode())

    client_socket.close()


def start_server(host="0.0.0.0", port=9999):
    """Starts the server and listens for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[SERVER] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[SERVER] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server(host="192.168.122.132")  # For server1
    # Uncomment the following line for server2 if needed
    # start_server(host="192.168.122.26")  # For server2
