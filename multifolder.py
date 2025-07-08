import os
from PIL import Image

# def create_dummy_image(path, size=(200, 200), color=(255, 0, 0)):
#     """Create a simple dummy image at the given path."""
#     image = Image.new("RGB", size, color)
#     image.save(path)
#
# def auto_populate_violations_folder(num_violations=5):
#     main_folder = "violations"
#     os.makedirs(main_folder, exist_ok=True)
#
#     for i in range(1, num_violations + 1):
#         sub_folder = os.path.join(main_folder, f"violation{i}")
#         os.makedirs(sub_folder, exist_ok=True)
#
#         front_path = os.path.join(sub_folder, "front.jpeg")
#         side_path = os.path.join(sub_folder, "side.jpeg")
#
#         create_dummy_image(front_path, color=(0, 255, 0))  # Green
#         create_dummy_image(side_path, color=(0, 0, 255))   # Blue
#
#         print(f"Created: {front_path}, {side_path}")
#

# Run the function to create folders and images
# auto_populate_violations_folder(num_violations=5)


#
# import os
# from PIL import Image
#
#
# def get_front_and_side_images(base_path="violations"):
#     # Sort folders like violation1, violation2, ...
#     violation_folders = sorted([
#         folder for folder in os.listdir(base_path)
#         if os.path.isdir(os.path.join(base_path, folder))
#     ])
#
#     for folder in violation_folders:
#         folder_path = os.path.join(base_path, folder)
#         front_path = os.path.join(folder_path, "front.jpeg")
#         side_path = os.path.join(folder_path, "side.jpeg")
#
#         if os.path.exists(front_path) and os.path.exists(side_path):
#             # Load the images (optional)
#             front_image = Image.open(front_path)
#             side_image = Image.open(side_path)
#
#             print(f"📂 {folder} -> Front: {front_path}, Side: {side_path}")
#
#             # Example: show image (optional)
#             # front_image.show()
#             # side_image.show()
#
#             # You can return, yield or process images here...
#         else:
#             print(f"⚠️ Skipping {folder}: front or side image missing.")
#
#
# # Run the function
# get_front_and_side_images()
#
import os
import threading
from PIL import Image
from Model.Configure import app  # This should be your Flask app
from Controller import ChallanController


# --- STEP 1: Load all violations into a dict
def load_camera_images_from_folders(camera_id=1,base_folder="violations"):
    camera_images = {}

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            front_path = os.path.join(folder_path, "front.jpeg")
            side_path = os.path.join(folder_path, "side.jpeg")

            if os.path.exists(front_path) and os.path.exists(side_path):
                try:
                    front_image = Image.open(front_path).convert("RGB")
                    side_image = Image.open(side_path).convert("RGB")

                    # ✅ Use folder name (e.g., "violation1") as camera_id key
                    camera_images[folder_name] = [front_image, side_image]
                except Exception as e:
                    print(f"❌ Error reading images in folder {folder_name}: {str(e)}")
            else:
                print(f"⚠️ Missing front or side image in folder: {folder_name}")
    return camera_images


# --- STEP 2: Thread target function with app context
def process_violation(camera_id, image_pair):
    with app.app_context():
        try:
            camera_images = {camera_id: image_pair}
            response, code = ChallanController.SimulationParallel_autoviolationdetection_fromFolder(camera_images)

            print(f"✅ [CAMERA {camera_id}] → CODE: {code}, RESPONSE: {response.json if hasattr(response, 'json') else response}")
        except Exception as e:
            print(f"❌ Error in thread for camera {camera_id}: {str(e)}")


# --- STEP 3: Main function to spawn threads
def process_all_violations_in_threads():
    camera_images_dict = load_camera_images_from_folders()

    threads = []

    for cam_id, image_pair in camera_images_dict.items():
        t = threading.Thread(target=process_violation, args=(1, image_pair))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("✅ All violation threads finished.")


# --- RUN
if __name__ == "__main__":
    process_all_violations_in_threads()
