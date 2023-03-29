import sys
import cv2
import numpy as np
import json
from tqdm import tqdm
import motor.motor_asyncio
import asyncio
from tensorflow import keras
import predict
from PIL import Image
import time



MONGO_DETAILS = "mongodb://root:example@127.0.0.1:27017/"
SECOND_FRACTION = 1

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.videos

student_collection = database.get_collection("videos")
# Load the video file
def process(filename):
  cap = cv2.VideoCapture(f'{filename}.mp4')

  # Set the threshold for detecting flashes
  brightness_threshold = 0.25

  # Initialize variables for counting flashes and frames
  flash_count = 0
  frames_since_flash = 0
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  flash_start_time = None
  flash_count = 0
  prev_flash_end_time = None
  total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

  nsfw_tolerance = 3
  time_from_nsfw = 0
  nfsw_start = None


  pbar = tqdm(total=total_frame_count)
  # Loop through the frames in the video
  data = []
  model = predict.load_model('./net/saved_model.h5')
  fraction = int(fps/SECOND_FRACTION)
  interval = [(fraction * i) for i in range(SECOND_FRACTION)]
  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      pbar.update(1)

      # Convert the frame to grayscale
      image = cv2.resize(frame, (224, 224))
      actions = []
      
      if cap.get(cv2.CAP_PROP_POS_FRAMES) % fps in interval:
          t = time.time_ns()
          cvt_image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          im_pil = Image.fromarray(cvt_image)
          
          img_array = keras.preprocessing.image.img_to_array(im_pil)
          img_array /= 255

          res = predict.classify_nd(model, np.asarray([img_array]))[0]
          if (res['porn'] > 0.5 or res['sexy'] > 0.5):
            time_from_nsfw = 0
            if (nfsw_start is None):
              nfsw_start = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
          else:
            time_from_nsfw += fraction/fps

      
      
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

      if frames_since_flash > fps:
        if flash_count >= 3:
            data.append({
              "startTime": int(flash_start_time),
              "endTime": int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000),
              "actions": ["lowerContrast"]
            })
            flash_start_time = None
            flash_count = 0
      if time_from_nsfw > nsfw_tolerance and nfsw_start is not None:
        data.append({
          "startTime": int(nfsw_start),
          "endTime": int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000),
          "actions": ["blur"]
        })
        nfsw_start = None
        time_from_nsfw = 0

      prev_std_dev = std_dev
  if nfsw_start is not None:
    data.append({
      "startTime": int(nfsw_start),
      "endTime": int(total_frame_count / fps),
      "actions": ["blur"]
    })
  cap.release()
  pbar.close()
  loop = asyncio.get_event_loop()
  loop.run_until_complete(student_collection.insert_one({
    "name": filename,
    "data": data
  }))
  loop.close()


if __name__ == '__main__':
  filename = sys.argv[1]
  process(filename)