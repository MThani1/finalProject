
import cv2
import os
from datetime import datetime
import time
from ultralytics import YOLO
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

# ----------- CONFIG -----------
IMAGE_DIR = "imager"
os.makedirs(IMAGE_DIR, exist_ok=True)
LATEST_SAVE_DIR = "latest"
os.makedirs(LATEST_SAVE_DIR, exist_ok=True)


camera_url = "rtsp://admin:HVUYJVH7575FV7YY@192.168.0.158:554/stream1"
LATEST_IMAGE_PATH = os.path.join(IMAGE_DIR, "latest.jpg")
model = YOLO("sdpai.pt")
TOTAL_SPACES = 300
latest_count = 0
DELAY_SECONDS = 10

# ----------- CAMERA -----------
def capture_latest_image():
    cap = cv2.VideoCapture(camera_url)

    if not cap.isOpened():
        print("❌ Error: Could not open video stream")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("⚠️ Failed to read frame.")
        return None

    cv2.imwrite(LATEST_IMAGE_PATH, frame)
    print(f"✅ Saved: {LATEST_IMAGE_PATH}")
    return LATEST_IMAGE_PATH

def capture_latest_image():
    cap = cv2.VideoCapture(camera_url)

    if not cap.isOpened():
        print("❌ Error: Could not open video stream")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("⚠️ Failed to read frame.")
        return None

    # Save to latest.jpg (for detection)
    cv2.imwrite(LATEST_IMAGE_PATH, frame)

    # Save to 'latest/' folder for fine-tuning
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(LATEST_SAVE_DIR, f"frame_{timestamp}.jpg")
    cv2.imwrite(backup_path, frame)

    print(f"✅ Saved for detection: {LATEST_IMAGE_PATH}")
    print(f"📦 Saved for fine-tuning: {backup_path}")
    return LATEST_IMAGE_PATH


# ----------- DETECTION -----------
def count_cars(image_path):
    print("🚗 Running YOLO detection...")
    results = model(image_path)
    total_cars = sum(len(result.boxes) for result in results)
    print(f"🚙 Cars detected: {total_cars}")
    return total_cars

# ----------- API SETUP -----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CarCount(BaseModel):
    count: int

@app.post("/update_count")
def update_count(data: CarCount):
    global latest_count
    latest_count = data.count
    available_spaces = TOTAL_SPACES - latest_count
    return {"available_spaces": max(available_spaces, 0)}

@app.get("/available_spaces")
def get_available_spaces():
    available = TOTAL_SPACES - latest_count
    return {"available_spaces": max(available, 0)}

# ----------- BACKGROUND DETECTION LOOP -----------
def send_to_backend_loop():
    while True:
        print("\n📸 New detection cycle started...")
        image_path = capture_latest_image()

        if image_path:
            car_count = count_cars(image_path)
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/update_count",
                    json={"count": car_count}
                )
                print("✅ Sent to backend:", response.json())
            except requests.exceptions.RequestException as e:
                print("❌ Failed to contact backend:", e)
        else:
            print("⚠️ Image not captured. Skipping...")

        time.sleep(DELAY_SECONDS)

# ----------- ENTRY POINT -----------
if __name__ == "__main__":
    from threading import Thread
    import uvicorn

    # Run detection loop in background
    t = Thread(target=send_to_backend_loop, daemon=True)
    t.start()

    # Start FastAPI app
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
