from fastapi import FastAPI, File, UploadFile
import requests
import shutil
import os
from fastapi.responses import FileResponse

app = FastAPI()

# Roboflow Model API details
ROBOFLOW_API_KEY = "your_roboflow_api_key"
MODEL_ENDPOINT = "https://detect.roboflow.com/ui-xeb6f/5?api_key=" + ROBOFLOW_API_KEY
UPLOAD_FOLDER = "uploads"
FEATURES_FOLDER = "features"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FEATURES_FOLDER, exist_ok=True)

@app.post("/detect/")
async def detect_ui_elements(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Send image to Roboflow API
    with open(file_path, "rb") as img:
        response = requests.post(MODEL_ENDPOINT, files={"file": img})
    
    if response.status_code != 200:
        return {"error": "Failed to process image"}
    
    detections = response.json().get("predictions", [])
    
    # Generate Gherkin feature file
    feature_content = generate_gherkin_feature(file.filename, detections)
    feature_path = os.path.join(FEATURES_FOLDER, f"{file.filename}.feature")
    
    with open(feature_path, "w") as f:
        f.write(feature_content)
    
    return FileResponse(feature_path, media_type="text/plain", filename=f"{file.filename}.feature")

def generate_gherkin_feature(image_name, detections):
    feature_text = f"Feature: UI Element Detection for {image_name}\n\n"
    feature_text += "  Scenario: Detect UI elements\n"
    for detection in detections:
        element = detection.get("class", "Unknown Element")
        x, y, width, height = detection.get("x", 0), detection.get("y", 0), detection.get("width", 0), detection.get("height", 0)
        feature_text += f"    Given a UI element '{element}' at ({x}, {y}) with size ({width}x{height})\n"
    return feature_text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
