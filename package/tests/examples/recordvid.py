import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_video = None

is_recording = False

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam Recording", frame)

    if is_recording:
        output_video.write(frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s") and not is_recording:
        print("Recording started")
        output_video = cv2.VideoWriter("webcam_recording.mp4", fourcc, 20.0, (640, 480))
        is_recording = True

    elif key == ord("q"):
        print("Recording stopped")
        break

cap.release()
if output_video:
    output_video.release()
cv2.destroyAllWindows()
