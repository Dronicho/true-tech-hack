import cv2
import numpy as np
import json
from tqdm import tqdm
import motor.motor_asyncio
import asyncio
from nudenet import NudeDetector


MONGO_DETAILS = "mongodb://root:example@127.0.0.1:27017/"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.videos

student_collection = database.get_collection("videos")
# Load the video file
cap = cv2.VideoCapture('long.mp4')

# Set the threshold for detecting flashes
brightness_threshold = 0.25

# Initialize variables for counting flashes and frames
flash_count = 0
frames_since_flash = 0
fps = cap.get(cv2.CAP_PROP_FPS)
flash_start_time = None
flash_count = 0
prev_flash_end_time = None
total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


pbar = tqdm(total=total_frame_count)
# Loop through the frames in the video
data = []

while False:
    ret, frame = cap.read()
    if not ret:
        break
    pbar.update(1)

    # Convert the frame to grayscale
    image = cv2.resize(frame, (100, 100))
    
    
    # Convert color space to LAB format and extract L channel
    L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
    # Normalize L channel by dividing all pixel values with maximum pixel value
    L = L/np.max(L)
    # Return True if mean is greater than thresh else False
    std_dev = np.mean(L)

    # Compute the mean brightness of the current frame and the previous frame
    if 'prev_std_dev' not in locals():
      prev_std_dev = std_dev
    diff = abs(std_dev - prev_std_dev) / max(prev_std_dev, std_dev)

    # Check if the brightness difference is above the flash threshold
    if diff > brightness_threshold:
        if flash_start_time is None:
            flash_start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        flash_count += 1
        frames_since_flash = 0
    else:
        frames_since_flash += 1
    #     if frames_since_flash > fps:
    #         if flash_start_time is not None and flash_count > 3:
    #             flash_end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    #             flash_range = (flash_start_time, flash_end_time)
    #             # if prev_flash_end_time is not None and flash_range[0] - prev_flash_end_time >= 2:
    #             #     print('{} - {}'.format(prev_flash_start_time, prev_flash_end_time))
    #             prev_flash_start_time = flash_start_time
    #             prev_flash_end_time = flash_end_time
    #             flash_start_time = None
    #             flash_count = 0

    # Check if there are at least three flashes in one second
    if frames_since_flash > fps:
      if flash_count >= 3:
          # f.write('{ "startTime": {}, endTime: {}, actions: ["blur"] }'.format(flash_start_time, cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
          data.append({
            "startTime": int(flash_start_time),
            "endTime": int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000),
            "actions": ["lowerContrast"]
          })
          flash_start_time = None
          flash_count = 0

    # Store the current frame as the previous frame for the next iteration
    prev_std_dev = std_dev

cap.release()
pbar.close()
# loop = asyncio.get_event_loop()
detector = NudeDetector()
print(detector.detect_video('long.mp4', show_progress=True, batch_size=5))
# loop.run_until_complete(student_collection.insert_one({
#   "name": "long",
#   "data": data
# }))
# loop.close()