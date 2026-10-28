import socket
import threading

HOST, PORT = "192.168.1.100", 5000

# Connection setup
sock = socket.create_connection((HOST, PORT))
send_lock = threading.Lock()
running = True

def receiver():
    """Continuously reads line-delimited key,value messages from the socket."""
    # Context manager ensures file wrapper releases properly
    with sock.makefile("r", encoding="utf-8") as file_stream:
        while running:
            line = file_stream.readline()
            if not line:  # Connection closed by remote host
                print("[network] Disconnected by peer.")
                break
            
            # Parse line
            parsed = parse_message(line)
            if parsed:
                name, val = parsed
                print(f"[from teensy] {name} = {val}")

def parse_message(line: str):
    """Parses incoming comma-separated string line into key-value tuple."""
    cleaned = line.strip()
    if not cleaned:
        return None
    
    name, sep, value_str = cleaned.partition(",")
    if not sep:
        print(f"[warning] Malformed line (no comma): {cleaned!r}")
        return None
        
    try:
        return name.strip(), float(value_str.strip())
    except ValueError:
        print(f"[warning] Invalid numeric payload: {value_str!r}")
        return None

def send(name: str, value: float) -> str:
    """Formats and transmits a command string over TCP, returning the raw string sent."""
    payload = f"{name},{value}\n"
    encoded = payload.encode("utf-8")
    
    with send_lock:
        sock.sendall(encoded)
        
    return payload  # Return the formatted string for logging or tracking

# Start background receiver
rx_thread = threading.Thread(target=receiver, daemon=True)
rx_thread.start()

# Example sends
sent_cmd1 = send("setpoint", 42.5)
sent_cmd2 = send("fire", 1.0)

input("Press Enter to quit...\n")

# Graceful cleanup
running = False
try:
    sock.shutdown(socket.SHUT_RDWR)
except OSError:
    pass
sock.close()