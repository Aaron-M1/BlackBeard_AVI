#this ois old test stuff for a live camera feed that saves the recordings.
#DO NOT RUN because this was before i knew import os and i didn't create a pathway for the recordings
# any recordings run through this code will just save it to the folder the file is in
# so dont do that unless you want to put some random video in the depricated folder
import cv2
import time
from datetime import datetime
now = datetime.now()
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 20.0 

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
timestamp = now.strftime('%Y-%d-%m %H-%M-%S')
out = cv2.VideoWriter(f'{timestamp}.mp4', fourcc, fps, (frame_width, frame_height))

print("Recording started. Press 'r' to stop and save.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to grab frame.")
        break

    out.write(frame)
    cv2.imshow('Live Recording', frame)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Video successfully saved as '{timestamp}.mp4'")