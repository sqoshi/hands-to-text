import cv2

from hands_to_text.video import CNNModelService, RandomForestModelService
from hands_to_text.video.images import draw_classbox
from hands_to_text.video.processor import FramesProcessor


def run_realtime_inference(frames_processor):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        chbox = frames_processor.process_frame(frame)

        if chbox is not None:
            draw_classbox(frame, chbox)
        else:
            cv2.putText(
                frame,
                "No Hand Detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        cv2.imshow("Hand Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    service = CNNModelService(
        # path="/home/piotr/Workspaces/studies/htt-models/models/cnn.pth"
        path="/home/piotr/Workspaces/studies/htt-models/models/cnnasl.pth"
    )
    # service = RandomForestModelService(
    # path="/home/piotr/Workspaces/studies/htt-models/models/rf.pickle"
    # )
    frames_processor = FramesProcessor(model_service=service)
    run_realtime_inference(frames_processor)
