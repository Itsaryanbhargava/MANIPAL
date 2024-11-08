import cv2
import numpy as np

# Load pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set frame dimensions (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def count_fingers_and_get_coordinates(hand_segment, thresholded):
    # Convex hull and convexity defects detection
    hull = cv2.convexHull(hand_segment, returnPoints=False)
    defects = cv2.convexityDefects(hand_segment, hull)

    if defects is None:
        return 0, None  # No fingers detected, return None for coordinates

    finger_count = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(hand_segment[s][0])
        end = tuple(hand_segment[e][0])
        far = tuple(hand_segment[f][0])

        # Calculate the angles between fingers using the cosine rule
        a = np.linalg.norm(np.array(end) - np.array(far))
        b = np.linalg.norm(np.array(start) - np.array(far))
        c = np.linalg.norm(np.array(start) - np.array(end))

        # Cosine rule: find the angle between the fingers
        angle = np.arccos((b*2 + c*2 - a*2) / (2 * b * c)) * (180 / np.pi)

        # Ignore angles > 90 degrees and filter defects by distance
        if angle <= 90 and d > 9000:  # Adjusted the distance threshold for more reliability
            finger_count += 1
            cv2.circle(thresholded, far, 5, (0, 0, 255), -1)

    # Add 1 to include the thumb
    return finger_count + 1, cv2.boundingRect(hand_segment)  # Return finger count and bounding box

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror-like effect
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Apply Gaussian blur for hand detection
    gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)

    # Apply thresholding (Otsu's Binarization for dynamic thresholding)
    _, thresholded = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Apply morphological operations to remove small noise
    kernel = np.ones((5, 5), np.uint8)
    thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    # Draw rectangles around detected faces to avoid these areas during hand detection
    for (x, y, w, h) in faces:
        cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Mask out the face area from the thresholded image
        thresholded[y:y+h, x:x+w] = 0

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Find the largest contour, assuming it's the hand
        hand_segment = max(contours, key=cv2.contourArea)

        # Filter out small contours that could be noise
        if cv2.contourArea(hand_segment) > 8000:  # Adjusted minimum contour area for better accuracy
            # Draw the hand contour on the frame
            cv2.drawContours(frame_copy, [hand_segment], -1, (0, 255, 0), 2)

            # Count fingers and get bounding box coordinates
            fingers, hand_coordinates = count_fingers_and_get_coordinates(hand_segment, thresholded)

            # Determine the gesture: Only "Fist" or "Open Hand"
            if fingers >= 4:
                gesture = "Open Hand"
            else:
                gesture = "Fist"

            # Display the gesture and bounding box coordinates
            cv2.putText(frame_copy, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            if hand_coordinates:
                x, y, w, h = hand_coordinates
                cv2.putText(frame_copy, f'Coordinates: x={x}, y={y}, w={w}, h={h}', (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

        else:
            gesture = "No Hand Detected"
            cv2.putText(frame_copy, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)

    else:
        gesture = "No Hand Detected"
        cv2.putText(frame_copy, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Hand Gesture Detection", frame_copy)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
