from PIL import  ImageFilter
import numpy as np
import cv2
import os
import dill
from ultralytics import YOLO
import matplotlib.pyplot as plt


class yolov8:
    @staticmethod
    def is_helmet_detected(prediction_result):

        if prediction_result.boxes:  # Ensure there are detected boxes
            for box in prediction_result.boxes:
                class_id = int(box.cls[0])  # Class ID
                class_name = prediction_result.names[class_id]  # Class name
                if class_name.lower() == "helmet":
                    return True
        return False
    @staticmethod
    # Helmet  motorbike   Head  SideMirror   License Plate
    def is_side_mirrors_detected(prediction_result):

        if prediction_result.boxes:  # Ensure there are detected boxes
            for box in prediction_result.boxes:
                class_id = int(box.cls[0])  # Class ID
                class_name = prediction_result.names[class_id]  # Class name
                if class_name.lower() == "sidemirror":
                    return True
        return False
    @staticmethod
    def get_detected_classes(prediction_result):

        detected_classes = []
        if prediction_result.boxes:  # Ensure there are detected boxes
            for box in prediction_result.boxes:
                class_id = int(box.cls[0])  # Class ID
                class_name = prediction_result.names[class_id]  # Class name
                detected_classes.append(class_name)
        return detected_classes
    @staticmethod
    def count_object(prediction_result, object_name):

        count = 0
        if prediction_result.boxes:  # Ensure there are detected boxes
            for box in prediction_result.boxes:
                class_id = int(box.cls[0])  # Class ID
                class_name = prediction_result.names[class_id]  # Class name
                if class_name.lower() == object_name.lower():
                    count += 1
        return count
    @staticmethod
    def crop_license_plate(prediction_result):

        cropped_images = []

        # Iterate over the detected bounding boxes
        if prediction_result.boxes:
            for box in prediction_result.boxes:
                class_id = int(box.cls[0])  # Class ID
                class_name = prediction_result.names[class_id]  # Class name

                # Check if the detected object is a license plate
                if class_name.lower() == "license plate":
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert coordinates to integers
                    # Crop the license plate region from the original image
                    cropped_image = prediction_result.orig_img[y1:y2, x1:x2]
                    cropped_images.append(cropped_image)

        return cropped_images

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
    def detect_violations_from_Image(source, model_path, save_dir=r"./Predictions"):
        os.makedirs(save_dir, exist_ok=True)  # Ensure save directory exists
        model = YOLO(model_path)

        results = model.predict(source=source, show=False)

        violations_and_plates = []  # List to store violations and cropped plates

        for i, result in enumerate(results):
            image = result.orig_img
            helmet_detected = yolov8.is_helmet_detected(result)
            side_mirrors_detected = yolov8.is_side_mirrors_detected(result)
            count_head = yolov8.count_object(result, 'head')
            cropped_plates = yolov8.crop_license_plate(result)

            violations = []
            if not helmet_detected:
                violations.append("Helmet")
            if not side_mirrors_detected:
                violations.append("Side Mirrors")
            if count_head >= 2:
                violations.append(f"Persons: {count_head}")
            if not cropped_plates:  # Check if no plates were detected
                violations.append("License Plate : Not Found")

            # Save and display cropped license plate if detected
            if cropped_plates:
                save_path = os.path.join(save_dir, f"LicensePlate_{i}.jpg")
                cv2.imwrite(save_path, cropped_plates[0])
                print(f"Saved cropped license plate to {save_path}")

            if violations:
                print(f"Violations Detected: {', '.join(violations)}")

            # Draw bounding boxes and labels
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = box.conf[0]
                label = f"{result.names[class_id]}: {confidence:.2f}"
                print(label)

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(image, label, (x1-10, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Save the final image with boxes
            save_path = os.path.join(save_dir, f"violation_{i}.jpg")
            cv2.imwrite(save_path, image)
            print(f"Saved detection result to {save_path}")

            # Resize dimensions (width, height)
            new_width = 800
            new_height = 800
            dsize = (new_width, new_height)
            resized_image = cv2.resize(image, dsize)

            # Display the final image
            cv2.imshow(f"Detection Result {i}", resized_image)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Append violations and cropped license plate (if detected)
            violations_and_plates.append({
                'violations': violations,
                'cropped_license_plate': cropped_plates[0] if cropped_plates else None
            })

        return violations_and_plates

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

        # Assuming `result` is the model prediction result




        #///////////////////////////////////////////////////////////////
        #  Callling of functions
        # if is_helmet_detected(result):
        #     print("Helmet detected!")
        #
        # if is_side_mirrors_detected(result):
        #     print("Side mirrors detected!")
        #
        # print("Detected classes:", get_detected_classes(result))
        #
        # helmet_count = count_object(result, "Helmet")
        # print(f"Number of helmets detected: {helmet_count}")

        # Assuming `result` is the YOLO model prediction result

        # cropped_plates = crop_license_plate(result)
        #
        # if cropped_plates:
        #     for i, plate in enumerate(cropped_plates):
        #         # Save or display the cropped license plate images
        #         save_path = f"cropped_plate_{i}.jpg"
        #         cv2.imwrite(save_path, plate)
        #         print(f"License plate saved to {save_path}")
        #
        #         # Optionally display the image
        #         cv2.imshow(f"License Plate {i}", plate)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        # else:
        #     print("No license plates detected.")






