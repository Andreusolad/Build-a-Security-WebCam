import cv2 #cv2 collaborates with numpy library
import time

video = cv2.VideoCapture(0)  # 0 because I only have 1 (main) camera in my laptop
time.sleep(1)  # code waits 1 sec

while True:
    check, frame = video.read()
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
