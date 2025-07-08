import cv2
import uuid
import json
from ultralytics import YOLO

# === CONFIGURATION ===
FRONT_IMAGE_PATH = r"C:\Users\Syed Mohsin Ali\Downloads\1-removebg-preview (9).png"
SIDE_IMAGE_PATH = r"C:\Users\Syed Mohsin Ali\Downloads\1-removebg-preview (8).png"
MODEL_PATH = r"C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\bike\runs\detect\bike_detector_m4\weights\best.pt"
TARGET_CLASS = "bike-and-person"

# === LOAD YOLOv8 MODEL ===
model = YOLO(MODEL_PATH)

# === FUNCTION TO RUN DETECTION AND CROP ===
def detect_and_crop(image_path, label=TARGET_CLASS):
    img = cv2.imread(image_path)
    results = model(img, verbose=False)[0]  # Get first result
    crops = []
    predictions = []

    for box, conf, cls in zip(results.boxes.xywh, results.boxes.conf, results.boxes.cls):
        class_id = int(cls.item())
        class_name = model.names[class_id]

        if class_name != label:
            continue

        x, y, w, h = map(int, box)
        x1, y1, x2, y2 = x - w // 2, y - h // 2, x + w // 2, y + h // 2
        x1, y1 = max(x1, 0), max(y1, 0)

        crop = img[y1:y2, x1:x2]
        crops.append(crop)

        predictions.append({
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "confidence": round(conf.item(), 3),
            "class": class_name,
            "class_id": class_id,
            "detection_id": str(uuid.uuid4())
        })

    return crops, predictions

# === DETECT IN FRONT IMAGE ===
front_crops, front_predictions = detect_and_crop(FRONT_IMAGE_PATH)

# === DETECT IN SIDE IMAGE ===
side_crops, side_predictions = detect_and_crop(SIDE_IMAGE_PATH)

# === PRINT RESULTS IN JSON FORMAT ===
print("\n🛵 Front Image Detection:")
print(json.dumps({"predictions": front_predictions}, indent=2))

print("\n🛵 Side Image Detection:")
print(json.dumps({"predictions": side_predictions}, indent=2))

# === SAVE CROPPED IMAGES (Optional) ===
for i, crop in enumerate(front_crops):
    cv2.imwrite(f"front_crop_{i+1}.jpg", crop)

for i, crop in enumerate(side_crops):
    cv2.imwrite(f"side_crop_{i+1}.jpg", crop)

print(f"\n✅ Crops saved: {len(front_crops)} from front, {len(side_crops)} from side.")
