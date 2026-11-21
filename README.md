# Data Driven Beauty: AI Skin Condition Analyzer

A web app that analyzes a skin or face photo with a PyTorch image classifier and suggests skincare products for the predicted condition.

> **Disclaimer:** This is an educational project, not a medical tool. It is a small model and has no "healthy skin" class, so any photo is labelled as one of the conditions. Always see a dermatologist for diagnosis.

## Features
- Capture a photo from the webcam or upload an image
- Classifies 21 skin conditions (Acne, Eczema, Psoriasis, Rosacea, Vitiligo, Warts and more)
- Returns the prediction, a confidence score and recommended products
- Shows product photos for supported conditions
- Tells the user to see a doctor for serious conditions

## Tech stack
- **Backend:** Python, Flask, PyTorch, OpenCV
- **Frontend:** HTML, CSS, JavaScript

## Project structure
```
skincare-backend/    Flask API (app.py), trained model, class names, recommendation images
skincare-frontend/   Web page (index.html, script.js, style.css)
```

## Run it locally

**1. Backend**
```bash
cd skincare-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The API runs on http://127.0.0.1:5000.

**2. Frontend** (in a second terminal)
```bash
cd skincare-frontend
python -m http.server 8000
```
Open http://localhost:8000, choose or capture a photo, and click **Analyze**.

## API
`POST /analyze` with form-data field `image`. Returns the prediction, confidence, products and image URLs.

## Dataset
The skin-disease images used for training are not included because of their size. Download the dataset and place it in `skincare-backend/data/train` and `skincare-backend/data/test`, one folder per condition.

## Training
`python train_model.py` trains the model on `data/train` and saves it to `model/skin_model.pth`.
