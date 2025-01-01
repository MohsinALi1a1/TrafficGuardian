import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace 'yolov8n.pt' with your custom weights if applicable)
model = YOLO(r'C:\Users\92306\PycharmProjects\TrafficGuardian\yolov8mtrafficmodel.pt')  # Use 'yolov8n.pt', 'yolov8s.pt', etc., or your custom model

# Path to the input video
video_path = r"C:\Users\92306\PycharmProjects\TrafficGuardian\5927708-hd_1080_1920_30fps.mp4"

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

# Define the codec and create a VideoWriter object to save the output video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

# Process the video frame by frame
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no more frames are available

    # Perform inference using YOLOv8
    results = model.predict(source=frame, conf=0.1, verbose=False)  # Adjust `conf` as needed

    # Annotate the frame with results
    annotated_frame = results[0].plot()
    annotated_frame = cv2.resize(annotated_frame, (640, 640))
    # Display the annotated frame
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    # Write the annotated frame to the output video
    out.write(annotated_frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video objects
cap.release()
out.release()
cv2.destroyAllWindows()
