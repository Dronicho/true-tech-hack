import sys
import numpy as np
import cv2
from tqdm import tqdm
import queue

path = sys.argv[1]

WINDOW_SIZE = 10

with open(f'{path}.json', 'w+') as f:
  vidcap = cv2.VideoCapture(f'{path}.mp4')
  fps = int(vidcap.get(cv2.CAP_PROP_FPS))
  last_color_average = 0
  points = 0
  frame_count = 0
  second_counter = 0
  success, image = vidcap.read()
  total_frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
  pbar = tqdm(total=total_frame_count)

  window = []

  
  time = 0
  prev_time = None
  while success:
      frame_count += 1
      pbar.update(1)

      # Get the average color
      r, g, b = np.average(np.average(image, axis=0), axis=0)
      current_color_average = (r + g + b) / 3

      # If the difference between the two frames is greater or less than a certain threshold
      time = int(frame_count / fps)
      if time > 5 and time < 10:
        print(last_color_average, current_color_average)
      window.append(abs(last_color_average - current_color_average) > 50)
      last_color_average = current_color_average
      # if ():



      # Reset the last_color_average
      if (len(window) == fps):
        if (not any(window) and prev_time != None):
          f.write(f'{prev_time} - {time}\n')
          prev_time = None
        elif any(window):
          if (prev_time == None):
            prev_time = time
        window.clear()
          
      success, image = vidcap.read()
  if (prev_time != None):
    f.write(f'{prev_time} - {time}')
  pbar.close()
  
  # Return average number of flashes per second
  
