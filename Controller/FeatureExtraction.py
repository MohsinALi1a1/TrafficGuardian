import uuid
import json
import os
import cv2
import numpy as np
from ultralytics import YOLO
from scipy.optimize import linear_sum_assignment
from PIL import Image

# Load your YOLOv8 model
MODEL_PATH = r"C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\bike\runs\detect\bike_detector_m4\weights\best.pt"
TARGET_CLASS = "bike-and-person"
model = YOLO(MODEL_PATH)


class FeatureExtraction:

    @staticmethod
    def detect_and_crop(image, label=TARGET_CLASS):
        results = model(image, verbose=False)[0]
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

            crop = image[y1:y2, x1:x2]
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

    @staticmethod
    def load_and_resize(path, size=(640, 480)):
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"Image not found at path: {path}")
        return cv2.resize(img, size)

    @staticmethod
    def extract_features(img):
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(img, None)
        return keypoints, descriptors

    @staticmethod
    def compute_similarity_score(des1, des2, top_k=10):
        if des1 is None or des2 is None:
            return float('inf'), []
        bf = cv2.BFMatcher()
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        top_matches = matches[:top_k]
        score = sum(m.distance for m in top_matches) / len(top_matches) if top_matches else float('inf')
        return score, top_matches

    @staticmethod
    def preprocess_image_hd(image_bgr, upscale_factor=2, apply_clahe=False):
        """
        Preprocess an image:
        - Upscale (convert to HD)
        - Remove noise
        - Sharpen
        - Apply Histogram Equalization or CLAHE

        Args:
            image_bgr (np.ndarray): Input image in BGR format
            upscale_factor (int): Factor to upscale the image
            apply_clahe (bool): Whether to apply CLAHE (if False, use histogram equalization)

        Returns:
            np.ndarray: Preprocessed image (BGR)
        """

        # Step 1: Upscale the image
        h, w = image_bgr.shape[:2]
        hd_image = cv2.resize(image_bgr, (w * upscale_factor, h * upscale_factor), interpolation=cv2.INTER_CUBIC)

        # # Step 2: Denoise
        # denoised = cv2.fastNlMeansDenoisingColored(hd_image, None, h=10, hColor=10, templateWindowSize=7,
        #                                            searchWindowSize=21)

        denoised = cv2.bilateralFilter(hd_image, d=9, sigmaColor=75, sigmaSpace=75)

        # Step 3: Sharpening
        sharpen_kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
        sharpened = cv2.filter2D(denoised, -1, sharpen_kernel)

        # Step 4: Contrast enhancement
        if apply_clahe:
            # Use CLAHE
            lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            merged = cv2.merge((cl, a, b))
            final = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
        else:
            # Use histogram equalization on Y channel
            ycrcb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(ycrcb)
            y_eq = cv2.equalizeHist(y)
            ycrcb_eq = cv2.merge((y_eq, cr, cb))
            final = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)

        return final


    @staticmethod
    def start(camera_images):
        front_paths = []
        side_paths = []

        print("Camera_image type:", type(camera_images[0]))
        print("Camera_image item:", camera_images[0])
        if camera_images:
            image_list = []
            for item in camera_images:
                image = item['image']
                print("Camera_image type:", type(image))

                # Convert PIL to OpenCV BGR image
                image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                image_list.append(image_cv2)

        # === DETECT IN FRONT IMAGE ===
        front_crops, front_predictions = FeatureExtraction.detect_and_crop(image_list[0])

        # === DETECT IN SIDE IMAGE ===
        side_crops, side_predictions = FeatureExtraction.detect_and_crop(image_list[1])

        # === PRINT RESULTS IN JSON FORMAT ===
        print("\n🛵 Front Image Detection:")
        print(json.dumps({"predictions": front_predictions}, indent=2))

        print("\n🛵 Side Image Detection:")
        print(json.dumps({"predictions": side_predictions}, indent=2))
        output_dir = "Seperate_output"
        os.makedirs(output_dir, exist_ok=True)

        # === SAVE CROPPED IMAGES (Optional) ===
        for i, crop in enumerate(front_crops):
            filename = os.path.join(output_dir, f"front_crop_{i + 1}.jpg")
            cv2.imwrite(filename, crop)
            front_paths.append(filename)
        for i, crop in enumerate(side_crops):
            filename = os.path.join(output_dir, f"side_crop_{i + 1}.jpg")
            cv2.imwrite(filename, crop)
            side_paths.append(filename)

        print(f"\n✅ Crops saved: {len(front_crops)} from front, {len(side_crops)} from side.")

        front_imgs = [FeatureExtraction.load_and_resize(p) for p in front_paths]
        side_imgs = [FeatureExtraction.load_and_resize(p) for p in side_paths]

        front_features = [FeatureExtraction.extract_features(img) for img in front_imgs]
        side_features = [FeatureExtraction.extract_features(img) for img in side_imgs]

        n_front = len(front_imgs)
        n_side = len(side_imgs)
        cost_matrix = np.zeros((n_front, n_side))
        all_matches = {}

        for i, (f_kp, f_des) in enumerate(front_features):
            for j, (s_kp, s_des) in enumerate(side_features):
                score, matches = FeatureExtraction.compute_similarity_score(f_des, s_des)
                cost_matrix[i, j] = score
                all_matches[(i, j)] = matches

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        output_dir = "matched_output"
        os.makedirs(output_dir, exist_ok=True)

        print("\n🔍 Matched Bike Pairs with Visuals:")
        match = {}
        count = 0
        matched_pairs = []

        for i, j in zip(row_ind, col_ind):
            front_img = front_imgs[i]
            side_img = side_imgs[j]
            f_kp, _ = front_features[i]
            s_kp, _ = side_features[j]
            matches = all_matches[(i, j)]

            vis_img = cv2.drawMatches(front_img, f_kp, side_img, s_kp, matches, None,
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            match[f'bike{count}'] = [i + 1, j + 1]
            count += 1
            label = f"Match: Front {i + 1} ↔ Side {j + 1} | Score: {cost_matrix[i, j]:.2f}"
            cv2.putText(vis_img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 50), 2)

            filename = os.path.join(output_dir, f"match_F{i + 1}_S{j + 1}.jpg")
            cv2.imwrite(filename, vis_img)

            front_img_data = cv2.imread(front_paths[i])
            side_img_data = cv2.imread(side_paths[j])
            matched_pairs.append({
                "front": front_img_data,
                "side": side_img_data
            })

            print(f"✅ {label} → Saved: {filename}")

        for i in match.keys():
            print(match[i])

        print("\n📁 Matched Pairs (converted to PIL):")
        pil_matched_pairs = []

        for pair in matched_pairs:
            processed = FeatureExtraction.preprocess_image_hd(pair['front'], upscale_factor=1, apply_clahe=False)
            processedside = FeatureExtraction.preprocess_image_hd(pair['side'], upscale_factor=1, apply_clahe=False)
            front_pil = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            side_pil = Image.fromarray(cv2.cvtColor(processedside, cv2.COLOR_BGR2RGB))

            pil_matched_pairs.append({
                'front': front_pil,
                'side': side_pil
            })

            print(f"Front mode: {front_pil.mode}, size: {front_pil.size}")
            print(f"Side mode: {side_pil.mode}, size: {side_pil.size}")

        return pil_matched_pairs
