import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# =========================
# Paths (Update if needed)
# =========================
DATA_DIR = r"D:/smartskincare/smart-skincare/skincare-backend/data/test"  # 👈 test dataset folder
MODEL_PATH = "./model/skin_model_efficientnet.pth"
CLASS_NAMES_PATH = "class_names.txt"

if __name__ == "__main__":
    # =========================
    # Check Dataset Path
    # =========================
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"❌ Test dataset not found at {DATA_DIR}")
    else:
        print(f"✅ Found test dataset: {DATA_DIR}")

    # =========================
    # Device (GPU if available)
    # =========================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # =========================
    # Image Transformations (same as training)
    # =========================
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    # =========================
    # Load Test Dataset
    # =========================
    test_dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False, num_workers=0)

    with open(CLASS_NAMES_PATH, "r") as f:
        class_names = [line.strip() for line in f.readlines()]

    # =========================
    # Load Trained Model
    # =========================
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(class_names))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model = model.to(device)
    model.eval()

    # =========================
    # Accuracy Calculation
    # =========================
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    accuracy = 100.0 * correct / total if total > 0 else 0.0
    print("\n==============================")
    print(f"✅ Total Test Images: {total}")
    print(f"✅ Overall Test Accuracy: {accuracy:.2f}%")
    print("==============================\n")
