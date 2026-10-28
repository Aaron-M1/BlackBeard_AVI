import socket
import threading
import time

# ---------- fake Teensy (runs in a background thread) ----------
def fake_teensy(srv):
    conn, addr = srv.accept()
    print("[teensy] client connected", flush=True)
    conn.sendall(b"temperature,23.5\n")
    for line in conn.makefile("r"):
        print(f"[teensy] got: {line.strip()}", flush=True)
        name, _, value = line.strip().partition(",")
        conn.sendall(f"{name}_ack,{value}\n".encode())

srv = socket.socket()
srv.bind(("127.0.0.1", 0))      # port 0 = let Windows pick a free port
srv.listen()
HOST, PORT = srv.getsockname()
threading.Thread(target=fake_teensy, args=(srv,), daemon=True).start()
print(f"[main] fake Teensy on {HOST}:{PORT}", flush=True)

# ---------- your client code ----------
sock = socket.create_connection((HOST, PORT))

def receiver():
    for line in sock.makefile("r"):
        name, _, value = line.strip().partition(",")
        print(f"[client] from teensy: {name} = {float(value)}", flush=True)

threading.Thread(target=receiver, daemon=True).start()

def send(name: str, value: float):
    sock.sendall(f"{name},{value}\n".encode())

send("setpoint", 42.5)
send("fire", 1.0)

time.sleep(1)    # give replies time to arrive
sock.close()
print("[main] done")