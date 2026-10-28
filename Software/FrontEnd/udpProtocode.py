import socket
import threading
#vibecoded here too
HOST, PORT = "127.0.0.1", 5000
print(f"Connecting to {HOST}:{PORT}")
sock = socket.create_connection((HOST, PORT))

def receiver():
    # makefile() gives line-based reads, so framing is handled for us
    for line in sock.makefile("r"):
        name, _, value = line.strip().partition(",")
        print(f"[from teensy] {name} = {float(value)}")

threading.Thread(target=receiver, daemon=True).start()

def send(name: str, value: float):
    sock.sendall(f"{name},{value}\n".encode())

send("setpoint", 42.5)
send("fire", 1.0)

input("Press Enter to quit...\n")   # keep main thread alive while receiving
sock.close()