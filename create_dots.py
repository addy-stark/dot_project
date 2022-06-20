import time
import os
import zipfile
import cv2
import numpy as np
import shutil
import glob
from random import randint
frameSize = (100, 100)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
#out = cv2.VideoWriter('test_video.mp4', fourcc, 1, frameSize)


# Radius of circle
radius = 3

# Red color in BGR
color = (0, 0, 255)

# Line thickness of -1 px
thickness = -1
os.mkdir('videos')
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
for k in range(1, 101): #creating 100 videos

    out = cv2.VideoWriter('videos/dot{}.mp4'.format(int(k)), fourcc, 1, frameSize)
    for i in range(1, 601): #creating video of 10 minute
        x = randint(0, 100)
        y = randint(0, 100)
        center_coordinates = (x, y)
        img = np.ones((100, 100, 3), dtype=np.uint8)*255
        image = cv2.circle(img, center_coordinates, radius, color, thickness)
        out.write(image)
    out.release()
    cv2.destroyAllWindows()
    print("video {} created" .format(int(k)))
    #time.sleep(1)

with zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir('videos/', zipf)
shutil.rmtree('videos')

