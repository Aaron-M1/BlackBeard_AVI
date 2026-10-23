import socket
import threading

#This is all vibecoded lmao we will need to make this actually good next week

HOST, PORT = "192.168.1.100", 5000

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

