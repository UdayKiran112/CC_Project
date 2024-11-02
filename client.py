import socket
import threading
import time

def create_client(server_ip, server_port):
    """Creates a TCP client that connects to the specified server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        return client_socket
    except ConnectionRefusedError:
        print(f"[CLIENT] Error connecting to {server_ip}:{server_port}")
        return None

def send_requests(client_socket, number_to_calculate, request_count):
    """Sends requests to the server and handles responses."""
    for _ in range(request_count):
        client_socket.send(str(number_to_calculate).encode())
        response = client_socket.recv(1024).decode()
        print(f"[CLIENT] Received: {response}")

    client_socket.close()

def run_client(server_ip, server_port, thread_count, number_to_calculate, request_count):
    """Creates multiple threads to simulate multiple clients."""
    threads = []
    for _ in range(thread_count):
        client_socket = create_client(server_ip, server_port)
        if client_socket:
            thread = threading.Thread(target=send_requests, args=(client_socket, number_to_calculate, request_count))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

def gradually_increase_load(server_ip, server_port, initial_threads, increment, max_threads, requests_per_thread, ramp_up_time):
    """Gradually increases load on the server."""
    current_threads = initial_threads
    while current_threads <= max_threads:
        print(f"[CLIENT] Starting load test with {current_threads} threads...")
        run_client(server_ip, server_port, current_threads, 20, requests_per_thread)
        
        time.sleep(ramp_up_time)  # Wait before increasing the load
        current_threads += increment

if __name__ == "__main__":
    server1_ip = "192.168.122.132"  # IP of server1
    server2_ip = "192.168.122.26"    # IP of server2
    server_port = 9999                # Port for both servers

    initial_threads = 1                # Starting number of threads
    increment = 1                      # Number of threads to add each ramp-up
    max_threads = 50                   # Maximum number of threads
    requests_per_thread = 10           # Number of requests each thread will send
    ramp_up_time = 10                  # Time to wait between increases (in seconds)

    print(f"[CLIENT] Starting gradual load test on {server1_ip}...")
    gradually_increase_load(server1_ip, server_port, initial_threads, increment, max_threads, requests_per_thread, ramp_up_time)

    print(f"[CLIENT] Starting gradual load test on {server2_ip}...")
    gradually_increase_load(server2_ip, server_port, initial_threads, increment, max_threads, requests_per_thread, ramp_up_time)

    print("[CLIENT] Load test completed.")
