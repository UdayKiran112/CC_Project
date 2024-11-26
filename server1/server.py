import socket
import threading
import time


# Simulate a CPU-intensive task (to trigger high CPU utilization)
def cpu_intensive_task():
    start_time = time.time()
    while time.time() - start_time < 5:  # Simulate a 5-second computation
        x = 0
        for _ in range(1000000):
            x += 1
    return x


# Handle each client request
def handle_client(client_socket):
    request = client_socket.recv(1024).decode("utf-8")
    if request == "COMPUTE":
        # Simulate CPU intensive task
        cpu_intensive_task()
        client_socket.send("Computation Done".encode("utf-8"))
    client_socket.close()


# Server function to listen for incoming connections
def server_thread(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    print(f"Server listening on {ip}:{port}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


# Start the server
if __name__ == "__main__":
    ip = "0.0.0.0"  # Accept connections on any IP
    port = 9999  # Example port
    server_thread(ip, port)
