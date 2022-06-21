import time
import cv2
import numpy as np
import zipfile
import shutil
import redis
import json
from Data import plot
r = redis.Redis(host='localhost', port=6379, db=0)
# Specifying upper and lower ranges of color to detect in hsv format
lower = np.array([0, 50, 50])
upper = np.array([10, 255, 255]) # (These ranges will detect red)

cord = []  # list storing all the centre coordinate values of each video in a nested
total_sum = []  # list storing the sum of each x and y cordinate in a nested list for each different vid
mean = []  # list storing mean value of each video
mean_dict = {}  # dictionary storing the mean value of each video as a key and item pair

with zipfile.ZipFile('python.zip', 'r') as zip_ref:
    zip_ref.extractall('')

for k in range(1, 101):
    cord_vid = []
    total_sum_vid = []
    webcam_video = cv2.VideoCapture("videos/dot{}.mp4".format(int(k)))
    print("Detecting video {}".format(int(k)))
    for i in range(1, 601):
        success, video = webcam_video.read() # Reading webcam footage

        img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format

        mask = cv2.inRange(img, lower, upper) # Masking the image to find our color

        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

        # Finding position of all contours
        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                if cv2.contourArea(mask_contour):
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 0), 1)  #drawing rectangle

        cv2.imshow("mask image", mask) # Displaying mask image

        cv2.imshow("window", video) # Displaying webcam image

        cv2.waitKey(1)
        cent_x, cent_y = float(x+(w/2)), float(y+(h/2))  # taking centre point of the dot
        cord_vid.append(tuple((cent_x, cent_y)))
        total_sum_vid.append(cent_x+cent_y)
    total_sum.append(total_sum_vid)
    mean.append(round(float((sum(total_sum[int(k-1)]))/600),2))
    cord.append(cord_vid)
    mean_dict[k] = mean[int(k-1)]
r.set('coordinates', json.dumps(cord))
sorted_mean_dict = sorted(mean_dict.items(), key=lambda x: x[1], reverse=False) #sorting the mean dictionary in ascending order
closest_vid = ([item[0] for item in sorted_mean_dict])[:5]
furthest_vid = ([item[0] for item in sorted_mean_dict])[-5:]
closest_vid_mean = ([item[1] for item in sorted_mean_dict])[:5]
furthest_vid_mean = ([item[1] for item in sorted_mean_dict])[-5:]
print("The videos with dot coming closest to starting point on average are {} with mean {}" .format(closest_vid, closest_vid_mean))
print("The videos with dot coming Furthest to starting point on average are {} with mean {}" .format(furthest_vid, furthest_vid_mean))
r.set('closest_vid_num', json.dumps(closest_vid))
r.set('furthest_vid_num', json.dumps(furthest_vid))
cv2.destroyAllWindows()
shutil.rmtree('videos')
#time.sleep(2)
clos_vid_values = json.loads(r.get('closest_vid_num'))
furth_vid_values = json.loads(r.get('furthest_vid_num'))
plot(clos_vid_values, furth_vid_values)