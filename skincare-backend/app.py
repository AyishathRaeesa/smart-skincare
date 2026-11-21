import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "skin_model.pth")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "class_names.txt")
REC_IMG_DIR = os.path.join(BASE_DIR, "static", "images", "recommendations")

with open(CLASS_NAMES_PATH, "r") as f:
    class_names = [line.strip() for line in f if line.strip()]


class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 32 * 16 * 16)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


model = SimpleCNN(num_classes=len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Text recommendations, keyed by the model's class names
RECOMMENDATIONS = {
    "Acne": ["Salicylic Acid Cleanser", "Oil-Free Moisturizer", "Acne Spot Treatment (Benzoyl Peroxide)"],
    "Actinic_Keratosis": ["See a dermatologist (these patches can become cancerous)", "SPF 50+ Sunscreen", "Annual skin check-up"],
    "Benign_tumors": ["Consult a dermatologist to confirm the diagnosis"],
    "Bullous": ["See a doctor promptly for evaluation", "Do not pop blisters"],
    "Candidiasis": ["Antifungal Cream (Clotrimazole)", "Keep the area clean and dry"],
    "DrugEruption": ["Contact your doctor or pharmacist about recent medicines", "Seek urgent care if you have fever, blisters or trouble breathing"],
    "Eczema": ["Ceramide Lotion", "Oatmeal Bath Treatment", "Hydrating Cream"],
    "Infestations_Bites": ["Calamine Lotion", "Antihistamine for itching", "See a doctor if the rash spreads"],
    "Lichen": ["Prescription Steroid Cream (from a doctor)", "Gentle Moisturizer"],
    "Lupus": ["See a doctor for diagnosis and treatment", "SPF 50+ Sunscreen"],
    "Moles": ["SPF 30+ Sunscreen", "Annual Dermatologist Exam"],
    "Psoriasis": ["Coal Tar Shampoo", "Thick Moisturizing Ointment", "Topical Steroid Cream"],
    "Rosacea": ["Anti-Redness Moisturizer", "Mineral Sunscreen", "Gentle Non-Foaming Cleanser"],
    "Seborrh_Keratoses": ["Usually harmless; see a dermatologist if it changes", "SPF 30+ Sunscreen"],
    "SkinCancer": ["See a dermatologist as soon as possible", "SPF 50+ Sunscreen"],
    "Sun_Sunlight_Damage": ["SPF 50+ Sunscreen", "Hydrating Moisturizer", "Annual skin check-up"],
    "Tinea": ["Antifungal Cream (Clotrimazole)", "Keep area dry and clean"],
    "Vascular_Tumors": ["Consult a dermatologist for evaluation"],
    "Vasculitis": ["See a doctor promptly for evaluation"],
    "Vitiligo": ["Gentle Sunscreen SPF 50+", "Moisturizer for Sensitive Skin", "Vitamin D Cream"],
    "Warts": ["Salicylic Acid Patch", "Cryotherapy at Dermatologist"],
}

# Model class -> product photo folder (only conditions where product photos make sense)
IMAGE_FOLDERS = {
    "Acne": "acne",
    "Actinic_Keratosis": "actinic_keratosis",
    "Eczema": "eczema",
    "Lichen": "lichen_planus",
    "Moles": "melanocytic_nevus_mole",
    "Psoriasis": "psoriasis",
    "Rosacea": "rosacea",
    "Tinea": "tinea_ringworm",
    "Vitiligo": "vitiligo",
    "Warts": "warts",
}


def get_images(predicted_class):
    folder = IMAGE_FOLDERS.get(predicted_class)
    if not folder:
        return []
    path = os.path.join(REC_IMG_DIR, folder)
    if not os.path.isdir(path):
        return []
    files = sorted(f for f in os.listdir(path)
                   if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    return [url_for("static", filename=f"images/recommendations/{folder}/{f}", _external=True)
            for f in files]


app = Flask(__name__)
CORS(app)


def is_face_present(pil_img):
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return len(faces) > 0


def is_skin_present(pil_img):
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([50, 255, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv_img, lower_skin, upper_skin)
    return np.sum(skin_mask > 0) / skin_mask.size > 0.10


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    try:
        img = Image.open(file.stream).convert("RGB")

        if not (is_face_present(img) or is_skin_present(img)):
            return jsonify({
                "error": "No face or skin detected. Please upload a clear, close-up photo of your face or skin area."
            }), 400

        image_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(image_tensor)
            probs = torch.softmax(output, 1)
            conf, predicted = torch.max(probs, 1)
            predicted_class = class_names[predicted.item()]

        products = RECOMMENDATIONS.get(predicted_class, ["Consult a dermatologist"])
        return jsonify({
            "prediction": predicted_class.replace("_", " "),
            "confidence": round(conf.item() * 100, 1),
            "products": products,
            "images": get_images(predicted_class),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)