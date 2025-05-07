# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# from pytesseract import pytesseract
# import re
#
# pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# # Load the image
# image_path = r'C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\Predictions\saved_images1\1_bike_2.jpg'
#
# image = cv2.imread(image_path)
#
# if image is None:
#     print("Error: Image not found or path is incorrect.")
#     exit()
# # image = cv2.resize(image, (800, 800))
# # Convert to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # Thresholding
# _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
#
# # Find contours for character segmentation
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
# bounding_boxes = sorted(bounding_boxes, key=lambda b: b[0])  # Sort left to right
#
# char_images = []
# extracted_text = ""
#
# print("🔠 Segmenting characters and applying OCR...\n")
#
# for i, (x, y, w, h) in enumerate(bounding_boxes):
#     if w > 10 and h > 20:
#         char = thresh[y:y+h, x:x+w]
#         char_images.append(char)
#
#         # Show character
#         cv2.imshow(f"Character {i+1}", char)
#         cv2.waitKey(0)  # Delay for visual display
#
#         # OCR on each character
#         char_pil = Image.fromarray(cv2.bitwise_not(char))  # Invert to white text on black
#         char_text = pytesseract.image_to_string(char_pil, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789').strip()
#         print(f"Character {i+1}: '{char_text}'")
#
#         extracted_text += char_text
#
# cv2.destroyAllWindows()
#
# # Show final result
# print("\n🆗 Final Extracted Plate Text:", extracted_text)

import cv2
import easyocr
import matplotlib.pyplot as plt
import re
import numpy as np
class OCR:

    @staticmethod
    def NumberExtractor(img):
        # Initialize EasyOCR Reader
        reader = easyocr.Reader(['en'])

        image = img
        if image is None or not isinstance(image, np.ndarray):
            print("❌ Error: Invalid image.")
            return "UNKNOWN"

        # Run OCR
        results = reader.readtext(image)

        extracted_text = []
        print("🔠 Detected Characters from Image:\n")

        for (bbox, text, prob) in results:
            print(f"📦 Text: '{text}' | Confidence: {prob:.2f}")
            if prob > 0:
                extracted_text.append(text)

                # Optional: Draw bounding box (if needed for later processing)
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Extract and clean plate number
        extracted_number = ""
        for text in extracted_text:
            cleaned_text = re.sub(r'[^A-Za-z0-9]+', '-', text)
            print("🔧 Cleaned Text:", cleaned_text)

            pattern = r'\b([A-Za-z]{1,5}[-\s]?\d{1,5})\b'
            match = re.search(pattern, cleaned_text)
            if match:
                plate_number = match.group(1)
                print("✅ Cleaned Plate Number:", plate_number)
                extracted_number = plate_number
                break
            else:
                print("❌ No valid plate number found in:", text)
        print(f"return number plate from ocr {extracted_number}")
        return extracted_number.strip() if extracted_number else ""