import serial

# Open the serial port (adjust port and baud rate as needed)
ser = serial.Serial('/dev/ttyACM0', 115200)

# Read data
data = ser.readline()
print(data.decode())   


# DO NOT USE
# sincerely - peve in the house