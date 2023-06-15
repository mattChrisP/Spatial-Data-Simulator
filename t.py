import csv

from rtree import index
from rtree.index import Rtree

rt = None
data_points = []

cnt = 0

f = open('locations_data.csv', 'r')

for line in f.readlines():
    if cnt > 100:
        break
    reader = line.rstrip("\r\n").split(",")
    data_points.append(reader)
    cnt += 1

# with open('locations_data.csv', 'r') as f:
print(data_points)

headers = data_points.pop(0)

# you can preprocess locations_data.csv datasets here
def preprocess():
    global rt, data_points
    print("Preprocessing...")

    p = index.Property()
    rt = index.Index(properties=p)

    # Populate R-tree index with bounds of polygons
    for i, point in enumerate(data_points):
        rt.insert(i, (float(point[1]), float(point[2]), float(point[1]), float(point[2])))

    print("Finish preprocessing")

def get_k_most_important_points_in_rect(k, x1, y1, x2, y2):
    global rt, data_points
    point_ids = list(rt.intersection((x1, y1, x2, y2)))
    points = [data_points[i] for i in point_ids]
    return sorted(points, key=lambda x: x[3], reverse=True)[:k]

def get_k_nearest_points_to_location(k, x, y):
    global rt, data_points
    point_ids = list(rt.nearest(coordinates=(x,y), num_results=k))
    return [data_points[i] for i in point_ids]

def get_data():
    global data_points
    return data_points


