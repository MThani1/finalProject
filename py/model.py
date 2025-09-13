# from ultralytics import YOLO

# model = YOLO("best1.pt")  # Load your trained model

# def count_cars(image_path):
#     results = model(image_path)
#     total_cars = sum(len(result.boxes) for result in results)  # Count boxes

#     if total_cars == 0:
#         print("🚫 No cars detected.")
#     else:
#         print(f"🚗 Cars detected: {total_cars}")
    
#     return total_cars
