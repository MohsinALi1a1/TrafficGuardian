
import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment
import os


front_paths = [
    r"C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\front_crop_1.jpg",

    r"C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\front_crop_2.jpg"
]

side_paths = [

    r"C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\side_crop_1.jpg",

    r"C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\side_crop_2.jpg",


]


# === Step 2: Load and Resize Images ===
def load_and_resize(path, size=(640, 480)):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {path}")
    return cv2.resize(img, size)

front_imgs = [load_and_resize(p) for p in front_paths]
side_imgs = [load_and_resize(p) for p in side_paths]

# === Step 3: Extract SIFT Features ===
def extract_features(img):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return keypoints, descriptors

front_features = [extract_features(img) for img in front_imgs]
side_features = [extract_features(img) for img in side_imgs]

# === Step 4: Compute Similarity ===
def compute_similarity_score(des1, des2, top_k=10):
    if des1 is None or des2 is None:
        return float('inf'), []
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    top_matches = matches[:top_k]
    score = sum(m.distance for m in top_matches) / len(top_matches) if top_matches else float('inf')
    return score, top_matches

# === Step 5: Build Cost Matrix & Save Matches ===
n_front = len(front_imgs)
n_side = len(side_imgs)
cost_matrix = np.zeros((n_front, n_side))
all_matches = {}

for i, (f_kp, f_des) in enumerate(front_features):
    for j, (s_kp, s_des) in enumerate(side_features):
        score, matches = compute_similarity_score(f_des, s_des)
        cost_matrix[i, j] = score
        all_matches[(i, j)] = matches

# === Step 6: Hungarian Algorithm ===
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# === Step 7: Draw Matches & Save ===
output_dir = "matched_output"
os.makedirs(output_dir, exist_ok=True)

print("\n🔍 Matched Bike Pairs with Visuals:")
match={}
count=0
for i, j in zip(row_ind, col_ind):
    front_img = front_imgs[i]
    side_img = side_imgs[j]
    f_kp, _ = front_features[i]
    s_kp, _ = side_features[j]
    matches = all_matches[(i, j)]

    vis_img = cv2.drawMatches(front_img, f_kp, side_img, s_kp, matches, None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Add text on top
    match[f'bike{count}']=[i+1 , j+1]
    count=count+1
    label = f"Match: Front {i+1} ↔ Side {j+1} | Score: {cost_matrix[i,j]:.2f}"
    cv2.putText(vis_img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 255, 50), 2)

    filename = os.path.join(output_dir, f"match_F{i+1}_S{j+1}.jpg")
    cv2.imwrite(filename, vis_img)
    print(f"✅ {label} → Saved: {filename}")


for i in match.keys():
    print(match[i])