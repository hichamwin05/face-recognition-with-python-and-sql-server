import cv2
import pyodbc
import numpy as np
import face_recognition
import pyttsx3
import serial
video_capture = cv2.VideoCapture(1)
connection_string = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-TQ1SBD9\MSSQLSERVER99;'
                      'Database=face_recognition;'
                      'Trusted_Connection=yes;')

mycursor = connection_string.cursor()

mycursor.execute("select * from stor_image")
rows = mycursor.fetchall()

known_face_names=[]
known_face_encodings =[]
for r in rows:
    db_enc = np.frombuffer(r[2])
    known_face_encodings.append(db_enc)
    known_face_names.append(r[1])
while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
        name = "unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]


        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 16, bottom - 16), font, 1.0, (255, 255, 255), 1)

        #if (name != "unknown"):
            #pyobj = pyttsx3.init()
            #pyobj.say("Welcoum" + name)
            #pyobj.runAndWait()

    cv2.imshow('Video', frame)
    k = cv2.waitKey(1) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

video_capture.release()
cv2.destroyAllWindows()
