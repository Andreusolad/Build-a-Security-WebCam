import cv2 #cv2 collaborates with numpy library
import time
from emailing import send_email
import glob

video = cv2.VideoCapture(0)  # 0 because I only have 1 (main) camera in my laptop
time.sleep(1)  # code waits 1 sec


first_frame = None
status_list = []
count = 1
while True:
    status = 0
    check, frame = video.read()

    # Algorithm to convert pixels to gray scale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gray frame is blurred a bit, last tuple is the amount of blurness
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    cv2.imshow("My video", gray_frame_gau)

    # We store the first frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # First frame minus gray_frame_gau to see "if there is movement"
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("My video", delta_frame)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] # Pixels equal or higher than 30 are categorized as 255, what's white.
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    # Detect the contours around those white areas, contours list of the countours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If the object is small we run the loop again, we continue
    for contour in contours:
        if cv2.contourArea(contour) < 3000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # Draw a rectangle around the frame, positions, its colour and width
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_object)

        cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
