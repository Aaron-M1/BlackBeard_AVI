# file = open("example.txt", "w")
# file.write("Hello, this is my first file created using Python!")
# file.close()
# print("File created successfully!")

import os
import time
from datetime import datetime
now = datetime.now()
timestamp = now.strftime('%Y-%m-%d %H-%M-%S')

filepath = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop', 'BlackBeard_Logs', f'{timestamp}.txt')
dir_path = os.path.dirname(filepath)

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open(filepath, "a") as f:
    f.write("This is a new log entry.\n")
    f.write("This is not real information \n")
    f.write("Lorem Epsum.\n")
    pass