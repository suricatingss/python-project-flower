import cv2
import numpy as np
import face_recognition
import face_recognition_models
import os
from datetime import datetime

def takeUserPic(camID = 0):
    cap = cv2.VideoCapture(camID)  # Open default camera

    while True:
        try:
            ret, frame = cap.read()
            if not ret: break

            # Convert frame to RGB for face recognition
            rgb_frame = frame[:, :, ::-1]

            # Find face locations
            face_locations = face_recognition.face_locations(rgb_frame)

            # If a face is detected, draw a green square and take a screenshot
            if face_locations:
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Take a screenshot
                screenshot = frame.copy()

                # Save the screenshot to a file
                cv2.waitKey(2000)
                cv2.imwrite('detected_face.png', screenshot)

                # Break out of the loop
                break

            # Display the frame
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        except: continue

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__": takeUserPic(1)
