import socket
import threading


def fibonacci_recursive(n):
    """Returns the nth Fibonacci number using a naive recursive approach."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def handle_client(client_socket):
    """Handles client requests with a CPU-intensive Fibonacci calculation."""
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break

        try:
            # Interpret the client's input as a number to calculate Fibonacci
            num = int(request)
            # Perform a CPU-intensive calculation
            result = fibonacci_recursive(num)
            response = f"Fibonacci of {num} is {result}"
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
    # Use the IP address of your server
    # start_server(host="192.168.122.132")  # For server1
    start_server(host="192.168.122.26")  # Uncomment for server2 if needed
