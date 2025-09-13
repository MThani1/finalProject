# import requests
# import time
# from main import count_cars
# from main import capture_image

# DELAY_SECONDS = 10  # Wait time between each detection

# def send_to_backend():
#     while True:
#         print("\n📸 Starting new detection cycle...")
#         imager_path = capture_image()

#         if imager_path is None:
#             print("⚠️ Skipping detection due to camera issue.")
#         else:
#             car_count = count_cars(imager_path)
#             print(f"🚗 Detected {car_count} cars.")

#             try:
#                 response = requests.post(
#                     "http://127.0.0.1:8000/update_count",
#                     json={"count": car_count}
#                 )
#                 print("✅ Backend response:", response.json())
#             except requests.exceptions.ConnectionError:
#                 print("❌ Error: Could not connect to FastAPI backend.")

#         print(f"⏳ Waiting {DELAY_SECONDS} seconds for next cycle...\n")
#         time.sleep(DELAY_SECONDS)

# if __name__ == "__main__":
#     send_to_backend()
