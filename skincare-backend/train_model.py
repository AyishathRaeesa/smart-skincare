import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# =========================
# Dataset Path (IMPORTANT)
# =========================
DATA_DIR = r"D:/smartskincare/smart-skincare/skincare-backend/data/train"
MODEL_PATH = "./model/skin_model_efficientnet.pth"
CLASS_NAMES_PATH = "class_names.txt"

if __name__ == "__main__":
    # =========================
    # Check Dataset Path
    # =========================
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(
            f"❌ Dataset folder not found: {DATA_DIR}\n"
            f"Check that the path and drive letter are correct."
        )
    else:
        print(f"✅ Found dataset folder: {DATA_DIR}")

    # =========================
    # Device (use GPU if available)
    # =========================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # =========================
    # Image Transformations
    # =========================
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # EfficientNetB0 expects 224x224
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    # =========================
    # Load Dataset
    # =========================
    dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
    loader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=0)  # 👈 num_workers=0 is safest on Windows

    class_names = dataset.classes
    print(f"✅ Found {len(class_names)} classes: {class_names}")
    print(f"✅ Total images: {len(dataset)}")

    # =========================
    # Load Pretrained EfficientNetB0
    # =========================
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)

    # Freeze all layers for transfer learning
    for param in model.parameters():
        param.requires_grad = False

    # Replace classifier head with correct number of outputs
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(class_names))
    model = model.to(device)

    # =========================
    # Loss & Optimizer
    # =========================
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier[1].parameters(), lr=0.001)

    # =========================
    # Training Loop
    # =========================
    n_epochs = 10  # Increase for better accuracy
    print("\n🚀 Starting training...\n")

    for epoch in range(n_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for i, (images, labels) in enumerate(loader):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            print(f"Epoch[{epoch+1}/{n_epochs}] "
                  f"Batch[{i+1}/{len(loader)}] "
                  f"Loss: {loss.item():.4f}")

        epoch_loss = running_loss / len(loader)
        epoch_acc = 100.0 * correct / total
        print(f"\n>>> Epoch {epoch+1}/{n_epochs} completed "
              f"— Avg Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.2f}%\n")

    # =========================
    # Save Model & Class Names
    # =========================
    os.makedirs("model", exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)

    with open(CLASS_NAMES_PATH, "w") as f:
        for name in class_names:
            f.write(name + "\n")

    print(f"✅ Model saved to {MODEL_PATH}")
    print(f"✅ Class names saved to {CLASS_NAMES_PATH}")
