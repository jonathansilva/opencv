import cv2
import numpy as np
import pyscreenshot as ImageGrab

img = ImageGrab.grab(bbox = (100, 10, 400, 400))

while True:
    ret, orig_frame = cap.read()

    if not ret:
        img = ImageGrab.grab(bbox = (100, 10, 400, 400))
        continue

    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, up_yellow)

    '''element = cv2.getStructuringElement(cv2.MORPH_CROSS,(6,6))
    eroded = cv2.erode(img,element)
    dilate = cv2.dilate(eroded, element)
    skeleton = cv2.subtract(img, dilate)
    gray = cv2.cvtColor(skeleton,cv2.COLOR_BGR2GRAY)
    '''

    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi / 180, threshold = 10, minLineLength = 1, maxLineGap = 50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow("frame", frame)

    cv2.imshow("edges", edges)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
