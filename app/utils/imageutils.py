import numpy as np
import cv2
from urllib.request import urlopen
import http.client
import json
import sys

def convertHSVRange(h, s, v):
    return (180 * h / 360, 255 * s / 100, 255 * v / 100)

def image_point_to_world_frame_point(point) :    
    scalingfactor = 1
    planeZ = 0
    uvzPoint = np.asarray(point)
    uv_1=uvzPoint.T
    suv_1=scalingfactor*uv_1
    xyz_c=np.linalg.inv(caMaInt).dot(suv_1)
    XYZ=np.linalg.inv(caMaExtR).dot(xyz_c)
    XYZ = XYZ + [CENTER[0],CENTER[1],planeZ]

    return XYZ

# Color for text and form overlays
GRID_COLOR = (245, 66, 224)

# Values for the in range function
GREEN_MIN = convertHSVRange(h=70, s=27, v=15)
GREEN_MAX = convertHSVRange(h=170, s=100, v=100)
# The real image center given from camera matrix
CENTER = (826,575)

# Offset from Camera to groud plane in mm
CAMERA_OFFSET = 27

caMaExtR = np.eye(3, dtype=np.float64)
caMaExtT = np.array([[0], [0], [0]], dtype=np.float64)
caMaInt = np.genfromtxt('K.csv', delimiter=',')


def measure(image, drivePosition) :
    image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    image_width = image.shape[1]
    image_height = image.shape[0]
    
    mask = cv2.inRange(image_hsv, GREEN_MIN, GREEN_MAX)

    cv2.circle(image, (image_width - 50,CENTER[1]), radius=10, color=GRID_COLOR, thickness=2)
    cv2.putText(image, str(drivePosition+CAMERA_OFFSET) + ' mm', (image_width - 200,CENTER[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color=GRID_COLOR, thickness=2)
    cv2.line(image, (image_width - 50, image_height), (image_width - 50, 0), GRID_COLOR, thickness=2)
    cv2.line(image, (image_width - 20,CENTER[1]), (image_width - 80,CENTER[1]), GRID_COLOR, thickness=2)    
    for i in range(10):
        cv2.line(image, (image_width - 20,CENTER[1] + 50*i), (image_width - 80,CENTER[1] + 50*i), GRID_COLOR, thickness=1)
        cv2.line(image, (image_width - 20,CENTER[1] - 50*i), (image_width - 80,CENTER[1] - 50*i), GRID_COLOR, thickness=1)

    indices = np.where(mask == 255)
    _, idx = np.unique(indices[0], return_index=True)
    rows = indices[0][np.sort(idx)]
    rows_grouped = np.split(rows, np.where(np.diff(rows) != 1)[0]+1)
    
    deltaYinMM = 0
    deltaYinPX = 0

    for row in rows_grouped:
        if row.size > 100 :
            cv2.line(image, (0,row[0]), (image_width - 50,row[0]), GRID_COLOR, thickness=1)
            cv2.putText(image, str(CENTER[1]-row[0]) + ' px', (image_width - 300,row[0]+30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color=GRID_COLOR, thickness=2)
            uvWorldPoint = image_point_to_world_frame_point((CENTER[0],CENTER[1],1))
            detectedPoint = image_point_to_world_frame_point((0,row[0],1))
            deltaYinMM = uvWorldPoint[1] - detectedPoint[1]
            deltaYinPX = CENTER[1]-row[0]
            cv2.putText(image, str(round(deltaYinMM*100)) + ' mm', (image_width - 300,row[0]+60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color=GRID_COLOR, thickness=2)
            break

    return image, deltaYinMM*100, deltaYinPX, drivePosition+CAMERA_OFFSET
