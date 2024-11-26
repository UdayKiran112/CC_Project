import socket
import threading
import random
import time

# List of server addresses
server_addresses = [
    ("192.168.122.201", 9999),  # Example IPs of VM servers
]

# Number of requests to send based on load mode
low_load_requests = 5
high_load_requests = 50


def send_request(server_ip, server_port):
    """Send a request to the server and wait for a response."""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        client.send("COMPUTE".encode("utf-8"))
        response = client.recv(1024)
        print(f"Received: {response.decode('utf-8')}")
        client.close()
    except Exception as e:
        print(f"Error sending request to {server_ip}:{server_port} - {e}")


def client_load_mode(mode="low"):
    """Simulate client load by sending requests to servers."""
    requests_to_send = low_load_requests if mode == "low" else high_load_requests
    threads = []
    for _ in range(requests_to_send):
        # Randomly select a server to send a request to
        server_ip, server_port = random.choice(server_addresses)
        thread = threading.Thread(target=send_request, args=(server_ip, server_port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# Function to periodically switch between low and high load
def simulate_load():
    while True:
        # Start with low load
        print("[CLIENT] Starting low load mode...")
        client_load_mode(mode="low")
        time.sleep(10)  # Simulate low load for 10 seconds

        # Switch to high load
        print("[CLIENT] Switching to high load mode...")
        client_load_mode(mode="high")
        time.sleep(10)  # Simulate high load for 10 seconds


# Start the client simulation
if __name__ == "__main__":
    simulate_load()
