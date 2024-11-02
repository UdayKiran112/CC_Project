import socket
import threading
import time

# Server addresses (modify with your actual server IPs)
servers = ["192.168.122.132", "192.168.122.26"]
PORT = 9999

# Load modes
LOW_LOAD_REQUESTS = 5
HIGH_LOAD_REQUESTS = 20

def send_request(server_ip, number):
    """Sends a request to the server and receives the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server_ip, PORT))
            client.send(str(number).encode())
            response = client.recv(4096).decode()
            print(f"[CLIENT] Received from {server_ip}: {response}")
    except Exception as e:
        print(f"[CLIENT] Error connecting to {server_ip}: {e}")

def generate_load(mode="low"):
    """Generates load by sending requests to the server."""
    requests = LOW_LOAD_REQUESTS if mode == "low" else HIGH_LOAD_REQUESTS
    threads = []

    for _ in range(requests):
        for server_ip in servers:
            num = 50000  # Choose a large number for factorial calculation
            thread = threading.Thread(target=send_request, args=(server_ip, num))
            thread.start()
            threads.append(thread)
            time.sleep(0.1)  # Slight delay between requests

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    while True:
        generate_load("low")  # Start in low load mode
        time.sleep(10)
        generate_load("high")  # Switch to high load mode
        time.sleep(10)
