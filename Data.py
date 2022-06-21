import redis
import json
import matplotlib.pyplot as plt

r = redis.Redis(host='localhost', port=6379, db=0)
all_coordinates = json.loads(r.get('coordinates'))

def plot(close_vid, furth_vid):
    for k in range(1, 6):
        closest_num = int(close_vid[int(k-1)] - 1)
        furthest_num = int(furth_vid[int(k-1)] - 1)
        closest_vid_cord = all_coordinates[closest_num]
        furthest_vid_cord = all_coordinates[furthest_num]
        fig, ax = plt.subplots(2, figsize=(10, 6))
        for i in range(600):
            ax[0].scatter(int(closest_vid_cord[int(i)][0]), int(closest_vid_cord[int(i)][1]))
            ax[1].scatter(int(furthest_vid_cord[int(i)][0]), int(furthest_vid_cord[int(i)][1]))
            ax[0].set_title("Close Coordinates Plot for video {}" .format(int(closest_num)+1))
            ax[0].set_xlabel('x')
            ax[0].set_ylabel('y')

            ax[1].set_title("Furthest Coordinates Plot for video {}".format(int(furthest_num)+1))
            ax[1].set_xlabel('x')
            ax[1].set_ylabel('y')
        plt.show()
        plt.close('all')
if __name__ == "__main__":
    clos_vid_values = json.loads(r.get('closest_vid_num'))
    furth_vid_values = json.loads(r.get('furthest_vid_num'))
    plot(clos_vid_values, furth_vid_values)

