let selectedBlob = null;
let selectedName = 'image.jpg';

// Splash screen
window.onload = () => {
  setTimeout(() => {
    document.getElementById('splash-screen').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
    initCamera();
  }, 1500);
};

function initCamera() {
  const video = document.getElementById("video");
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    })
    .catch(err => {
      console.error("Camera error:", err);
      document.getElementById("result").innerText =
        "Camera not available. You can upload an image instead.";
    });
}

function showPreview(blob) {
  const img = document.getElementById("captured-image");
  img.src = URL.createObjectURL(blob);
  img.style.display = "block";
}

// Capture from camera
document.getElementById("capture").addEventListener("click", () => {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const resultElement = document.getElementById("result");

  if (!video.videoWidth) {
    resultElement.innerText = "Camera not available. Please upload an image instead.";
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(blob => {
    selectedBlob = blob;
    selectedName = "captured.jpg";
    showPreview(blob);
    resultElement.innerText = "Image captured. Click Analyze.";
  }, "image/jpeg", 0.95);
});

// Upload from file
document.getElementById("file-input").addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;

  selectedBlob = file;
  selectedName = file.name;
  showPreview(file);
  document.getElementById("result").innerText = "Image selected. Click Analyze.";
});

// Analyze
document.getElementById("analyze-button").addEventListener("click", async () => {
  const resultElement = document.getElementById("result");

  if (!selectedBlob) {
    resultElement.innerText = "Please capture or upload an image first.";
    return;
  }

  const formData = new FormData();
  formData.append("image", selectedBlob, selectedName);

  resultElement.innerText = "Analyzing...";

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    if (data.error) {
      resultElement.innerText = "Error: " + data.error;
    } else {
      resultElement.innerText =
        "Prediction: " + data.prediction +
        "\nRecommended Products:\n" + (data.products?.join(", ") || "None");
    }
  } catch (error) {
    console.error("Fetch error:", error);
    resultElement.innerText =
      "Failed to analyze image. Is the backend running on port 5000?";
  }
});