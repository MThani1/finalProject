# import cv2
# import os
# from datetime import datetime
# import time
# from ultralytics import YOLO
# from fastapi import FastAPI
# from pydantic import BaseModel
# # Assuming this function is defined in camera.py

# from fastapi.middleware.cors import CORSMiddleware

# # Folder to store images
# IMAGE_DIR = "imager"
# os.makedirs(IMAGE_DIR, exist_ok=True)

# # Your RTSP camera URL
# camera_url = "rtsp://admin:HVUYJVH7575FV7YY@192.168.0.158:554/stream1"

# def capture_image(interval_seconds=30):
#     print("📷 Starting camera image capture loop...")

#     cap = cv2.VideoCapture(camera_url)

#     if not cap.isOpened():
#         print("❌ Error: Could not open video stream")
#         return

#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 print("⚠️ Failed to retrieve frame. Exiting...")
#                 break

#             # Generate a timestamped filename
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = os.path.join(IMAGE_DIR, f"frame_{timestamp}.jpg")

#             # Save the image
#             cv2.imwrite(filename, frame)
#             print(f"✅ Saved image: {filename}")

#             # Wait before next capture
#             time.sleep(interval_seconds)

#     except KeyboardInterrupt:
#         print("🛑 Stopped by user.")

#     finally:
#         cap.release()
#         print("🔒 Camera released.")

# # Run the loop directly if this file is executed
# if __name__ == "__main__":
#     capture_image(interval_seconds=30)




# model = YOLO("best1.pt")  # Load your trained model

# def count_cars(capture_image):
#     print("🚗 Counting cars...")
#     results = model(capture_image)
#     total_cars = sum(len(result.boxes) for result in results)  # Count boxes

#     if total_cars == 0:
#         print("🚫 No cars detected.")
#     else:
#         print(f"🚗 Cars detected: {total_cars}")
    
#     return total_cars


# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change to ["http://localhost:3000"] for security
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     )


# TOTAL_SPACES = 100  # Total capacity of the parking lot
# latest_count = 0  # Store last received count

# class CarCount(BaseModel):
#     count: int

# @app.post("/update_count")
# def update_count(data: CarCount):
#     global latest_count
#     latest_count = data.count
#     available_spaces = TOTAL_SPACES - latest_count
#     return {"available_spaces": max(available_spaces, 0)}

# @app.get("/available_spaces")
# def get_available_spaces():
#     available = TOTAL_SPACES - latest_count
#     return {"available_spaces": max(available, 0)}
