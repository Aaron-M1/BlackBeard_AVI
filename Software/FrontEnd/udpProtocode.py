import socket
import threading
import time

host, port = "127.0.0.1", 5000

def set_host(ip, port): # aaron asked me to make this function. i d k if it's useful or not.
    host = ip
    port = port

def connect(host,port,retry_delay=1, connect_timeout=3, max_connection_attempts=5):
    connection_attempts = 0
    while True: # there might be a way to make this more concise with a for loop. i dont feel like doing that rn tho :3c it works
        try:
            print(f"Connecting to {host}:{port}")
            sock = socket.create_connection((host, port), timeout=connect_timeout)
            sock.settimeout(None)
            return sock
        except (ConnectionRefusedError, socket.timeout, OSError) as e:
            connection_attempts += 1
            print(f"Server not ready ({e}), retrying in {retry_delay}s...")
            time.sleep(retry_delay)
            if connection_attempts == max_connection_attempts:
                print("Max connection attempts reached. Exiting.")
                raise

sock = connect(host, port)
# >>>>>>> fc43f9638533b1abfe82ee72598b171a244ba143

def setHost(ip):
    HOST = ip

def receiver():
    for line in sock.makefile("r"):
        name, _, value = line.strip().partition(",")
        print(f"[from teensy] {name} = {float(value)}")

threading.Thread(target=receiver, daemon=True).start()

def send(name: str, value: float):
    sock.sendall(f"{name},{value}\n".encode())


send("setpoint", 42.5)
send("water", 1.0)

input("Press Enter to quit...\n")   # keep main thread alive while receiving

sock.close()