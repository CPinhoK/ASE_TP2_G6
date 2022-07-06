import cv2
import sys

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
video_capture.set(3,640)
video_capture.set(4,480)
video_capture.set(cv2.CAP_PROP_FPS, 30)


import time

frame_rate = 30
prev = 0
total = 0
totaltimes=0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

	
    time_elapsed = time.time() - prev
    #print("te",1/time_elapsed)
    if total > 1:
        print("fps:",totaltimes)
        total=0
        totaltimes=0
    else:
        total+=time_elapsed
        totaltimes+=1



    prev = time.time()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags=cv2.CASCADE_SCALE_IMAGE
    )


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

