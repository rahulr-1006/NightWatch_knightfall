import cv2

cap = cv2.VideoCapture(0)  # Try 0, 1, or 2 if needed

if not cap.isOpened():
    print("❌ Camera not detected! Try changing the index (0, 1, 2).")
else:
    print("✅ Camera is working!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Could not read frame. Check if the camera is in use.")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
