import socket
import threading
import math

def handle_client(client_socket):
    """Handles client requests."""
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break
        
        # Perform CPU-intensive task (e.g., factorial)
        num = int(request)
        result = math.factorial(num)  # Replace with other CPU-intensive work if needed
        client_socket.send(f"Factorial of {num} is {result}".encode())

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
    start_server()
