import cv2
import numpy as np
import asyncio
import websockets

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width, _ = frame.shape

x1, y1 = 100, 100
x2, y2 = 220, 220
color = (255, 0, 0)

median_hsv_value = None

async def send_direction(direction):
    uri = "ws://192.168.202.158:6789"
    async with websockets.connect(uri) as websocket:
        await websocket.send(direction)

while True:
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    if not ret:
        break

    thickness = 2
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

    roi = frame[y1:y2, x1:x2]
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    median_hsv_value = np.median(roi_hsv, axis=(0, 1))
    print(f"Median HSV pixel value in rectangle: {median_hsv_value}")

    cv2.imshow("Random Rectangle on Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Final Median HSV Value:", median_hsv_value)

if median_hsv_value is not None:
    cv2.namedWindow("Trackbars")
    median_hue = int(median_hsv_value[0])
    median_saturation = int(median_hsv_value[1])
    median_value = int(median_hsv_value[2])

    cv2.createTrackbar("LH", "Trackbars", max(0, median_hue - 10), 179, nothing)
    cv2.createTrackbar("LS", "Trackbars", max(0, median_saturation - 20), 255, nothing)
    cv2.createTrackbar("LV", "Trackbars", max(0, median_value - 20), 255, nothing)
    cv2.createTrackbar("UH", "Trackbars", min(179, median_hue + 10), 179, nothing)
    cv2.createTrackbar("US", "Trackbars", min(255, median_saturation + 20), 255, nothing)
    cv2.createTrackbar("UV", "Trackbars", min(255, median_value + 20), 255, nothing)

    center_tolerance = 40

    while True:
        ret, frame = cap.read()
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lh = cv2.getTrackbarPos("LH", "Trackbars")
        ls = cv2.getTrackbarPos("LS", "Trackbars")
        lv = cv2.getTrackbarPos("LV", "Trackbars")
        uh = cv2.getTrackbarPos("UH", "Trackbars")
        us = cv2.getTrackbarPos("US", "Trackbars")
        uv = cv2.getTrackbarPos("UV", "Trackbars")

        lower_skin = np.array([lh, ls, lv], dtype=np.uint8)
        upper_skin = np.array([uh, us, uv], dtype=np.uint8)

        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.medianBlur(mask, 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        left_hand_center = None
        right_hand_center = None
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                hull = cv2.convexHull(contour)
                M = cv2.moments(hull)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    palm_center = (cx, cy)
                    frame_width = frame.shape[1]
                    if palm_center[0] < frame_width / 2:
                        left_hand_center = palm_center
                        cv2.circle(frame, left_hand_center, 10, (255, 0, 0), -1)
                    else:
                        right_hand_center = palm_center
                        cv2.circle(frame, right_hand_center, 10, (0, 255, 0), -1)

        direction = "Center"
        if left_hand_center and right_hand_center:
            height_difference = abs(left_hand_center[1] - right_hand_center[1])

            if height_difference <= center_tolerance:
                direction = "Center"
            elif right_hand_center[1] < left_hand_center[1]:
                direction = "Turn Right"

            else:
                direction = "Turn Left"

        
        asyncio.run(send_direction(direction))

        cv2.putText(frame, f"Steering Direction: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
