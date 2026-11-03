# old qnethernet test. just leaving it here in case, did not code a matching c++ file.
import socket

TEENSY_IP = ""
TEENSY_PORT = 0

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TEENSY_IP, TEENSY_PORT))
        s.sendall(b"Hello from Python!\n")
        
        data = s.recv(1024)
        print(f"Received from Teensy: {data.decode('utf-8')}")
except Exception as e:
    print(f"Connection error: {e}")