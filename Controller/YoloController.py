from PIL import  ImageFilter
import numpy as np
import cv2
import os
import dill
from ultralytics import YOLO
import matplotlib.pyplot as plt



class yolov8:
    @staticmethod
    def preprocess_image(image, target_size=(640, 640), grayscale=False, normalize=True, blur=False,
                         edge_detection=False,
                         add_batch_dim=True):
        """
        Preprocess an image by resizing, converting to grayscale, normalizing, blurring, edge detection,
        and optionally adding a batch dimension.

        Parameters:
        - image: A PIL Image object.
        - target_size: A tuple (width, height) to resize the image.
        - grayscale: Convert the image to grayscale if True.
        - normalize: Normalize pixel values to range [0, 1] if True.
        - blur: Apply a slight blur to the image if True.
        - edge_detection: Apply edge detection to the image if True.
        - add_batch_dim: Adds an extra dimension for batch size if True.

        Returns:
        - A preprocessed image as a numpy array.
        """
        # Resize the image
        image = image.resize(target_size)

        # Convert to grayscale if specified
        if grayscale:
            image = image.convert('L')  # 'L' mode for grayscale

        # Apply blur if specified
        if blur:
            image = image.filter(ImageFilter.BLUR)

        # Apply edge detection if specified
        if edge_detection:
            image = image.filter(ImageFilter.FIND_EDGES)

        # Convert image to numpy array
        image_array = np.array(image)

        # Convert to float32 and normalize if specified
        if normalize:
            image_array = image_array.astype('float32') / 255.0  # Scale to [0, 1]

        # Add batch dimension if specified
        if add_batch_dim:
            image_array = np.expand_dims(image_array, axis=0)  # Shape becomes (1, height, width, channels)

        return image_array

    @staticmethod
    # Step 1: Train the model
    def train_model(data_path, saved_model_path):
        # Load the model
        model = YOLO('yolov8s.pt')  # Using the small version for a balance of speed and accuracy
        print("Training the model...")
        model.train(data=data_path, epochs=100, imgsz=640)
        print("Training completed.")
        model.save(saved_model_path)  # Save the trained model

    @staticmethod
    def detect_violations_from_Image(source, model_path,save_path=r"C:/Users/92306/PycharmProjects/TrafficGuardian/Prediction"):
        # Load the YOLO model
        model = YOLO(model_path)

        # Run prediction
        results = model.predict(source=source, show=False)  # Set `show=False` to handle display manually

        for result in results:
            image = result.orig_img  # Get the original image from the result
            if result.boxes:  # Check if any boxes were detected
                for box in result.boxes:
                    # Extract bounding box coordinates and class information
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                    class_id = int(box.cls[0])  # Class ID
                    confidence = box.conf[0]  # Confidence score
                    label = f"{result.names[class_id]}: {confidence:.2f}"

                    # Draw bounding box on the image
                    cv2.rectangle(image, (x1, y1), (x2, y2), (250, 255, 0), 5)  # Green box color and 2 is thickness
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)  # Label above the box

                    print(f"Detected: {result.names[class_id]} with confidence: {confidence:.2f}")
                # Save the image with detected violations to a file
                cv2.imwrite(save_path, image)
                print(f"Output saved to {save_path}")
                # Display the image inline in Jupyter Notebook
                # if __name__ == "__main__":
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.axis("off")
                plt.show()
            else:
                print("No violations detected.")

    @staticmethod
    def fine_tune_and_save(data_path, model_path, save_path, batch_size=16):
        print("Fine-tuning the model...")
        model = YOLO(model_path)  # Load the pre-trained model
        # Fine-tune the model with specified batch size
        model.train(data=data_path, epochs=30, imgsz=640, batch=batch_size , device=0 )
        model.save(save_path)  # Save the fine-tuned model
        print(f"Model saved to {save_path}")

    @staticmethod
    # Detect from video
    def detect_from_video(video_path, model_path):
        # Load the YOLOv8 model
        model = YOLO(model_path)

        # Open the video file or capture from webcam
        cap = cv2.VideoCapture(video_path)  # Use 0 for webcam, or replace with a video file path

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Optional: Create a video writer to save the output
        output_file = 'output_video.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Perform detection
            results = model.predict(source=frame, show=False)  # Don't show the frame during prediction

            # Process results
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        class_id = int(box.cls[0])  # Get the class ID of the detected object
                        confidence = box.conf[0]  # Get the confidence score

                        # Get the bounding box coordinates
                        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Unpack the coordinates

                        # Draw the bounding box and label
                        label = f"{result.names[class_id]}: {confidence:.2f}"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                    2)  # Draw label

            # Write the frame to the output video
            out.write(frame)

            # Display the frame
            cv2.imshow('Object Detection', frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        out.release()  # Save the output video
        cv2.destroyAllWindows()

    # Main function to run the detection
    if __name__ == "__main__":
        # Set the path to your dataset and model
        data_path = r'C:\Users\92306\PycharmProjects\TrafficGuardian\traffic guardian.v2i.yolov8\data.yaml'  # Update this path
        model_path = r'C:\Users\92306\PycharmProjects\TrafficGuardian\runs\detect\train26\weights\best.pt'  # Pre-trained model
        model_save_path = r'C:\Users\92306\PycharmProjects\TrafficGuardian\Model-yolo\yolov8s.pt'  # Path to save the fine-tuned model


        # # Load an image
        # image_path = "path_to_your_image.jpg"
        # image = cv2.imread(image_path)
        #
        # # Call the preprocess_image function with your desired parameters
        # preprocessed_image = preprocess_image(
        #     image,
        #     target_size=(640, 640),  # Resize to 640x640 (or adjust as needed)
        #     grayscale=False,  # Set to True if you want grayscale
        #     normalize=True,  # Set to True to normalize pixel values
        #     blur=True,  # Set to True to apply a slight blur
        #     edge_detection=False,  # Set to True to apply edge detection
        #     add_batch_dim=True  # Add batch dimension for model input
        # )
        #
        # Check the shape of the preprocessed image
        # print("Preprocessed image shape:", preprocessed_image.shape)

        # # Fine-tune and save the model
        # fine_tune_and_save(data_path, model_path, model_save_path)
        #
        # # Perform detection on a test image or video
        # test_image_path = 'path/to/test/image.jpg'  # Change to your test image path
        # detect_violations_from_Image(test_image_path, save_path)  # Use the fine-tuned model for detection

        # # Perform detection from a video
        # video_path = 'path/to/your/video.mp4'  # Update this path
        # detect_from_video(video_path, save_path)
