import cv2
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76
from tqdm import tqdm

# Load the video file
cap = cv2.VideoCapture('ep.mp4')

# Set the threshold for detecting flashing
threshold = 0.8

# Set the minimum number of flashes required in one second
min_flashes_per_second = 3

# Initialize variables for counting flashes
flash_count = 0
frames_since_flash = 0
fps = cap.get(cv2.CAP_PROP_FPS)
total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
pbar = tqdm(total=total_frame_count)

# Loop through the frames in the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    pbar.update(1)
    # Convert the frame to the CIELAB color space
    image = cv2.resize(frame, (100, 100))
    # Convert color space to LAB format and extract L channel
    L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
    # Normalize L channel by dividing all pixel values with maximum pixel value
    L = L/np.max(L)
    # Return True if mean is greater than thresh else False
    std_dev = np.mean(L)
    

    # Compute the ΔE between adjacent frames
    if 'prev_std_dev' not in locals():
        prev_std_dev = std_dev
    
    # Compute the standard deviation of the ΔE values
    diff = abs(std_dev - prev_std_dev) / prev_std_dev
    print(diff)
    # Check if the standard deviation is above the threshold
    if diff > threshold:
        flash_count += 1
        frames_since_flash = 0
    else:
        frames_since_flash += 1
        if frames_since_flash > fps:
            flash_count = 0

    # Check if there are at least three flashes in one second
    if flash_count >= min_flashes_per_second:
        print('At least {} flashes detected in one second at frame {}'.format(min_flashes_per_second, cap.get(cv2.CAP_PROP_POS_FRAMES)))

    # Store the current frame as the previous frame for the next iteration
    prev_std_dev = std_dev
pbar.close()
cap.release()
