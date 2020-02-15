import cv2
import numpy as np
from collections import Counter
import time

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    start = time.time()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Shape of image is 480x640

    # red color detecting with treshold
    # open hsv app and see the value of the low red color
    # HSV = Hue, Saturation, Brightness Value / Hue values is in range(0 - 60) for red
    low_red = np.array([0, 180, 200])
    high_red = np.array([10, 360, 360])

    # ıt applied the low ang high points and we find what we want in determinant range of red scala.
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    matrix = np.asarray(red_mask)
    # cv2.imshow("Frame_Of_Red_Points", red_mask)

    result = np.where(matrix == 255)

    if (matrix.sum() / 255 > 800):  # We must detect number of pixel
        left_row = result[1].min()
        left_column = result[0].min()
        right_row = result[1].max()
        right_column = result[0].max()

        circle_center_point1 = (int)((right_row - left_row) / 2) + left_row
        circle_center_point2 = (int)((right_column - left_column) / 2) + left_column

        # cv2.rectangle(frame, pt1=(left_row - 10, left_column - 10), pt2=(right_row + 10, right_column + 10), color=(0, 255, 0), thickness= -1)
        cv2.circle(img=frame, center=(circle_center_point1, circle_center_point2), radius=9, color=(0, 255, 0),
                   thickness=-1)
        cv2.line(frame, pt1=(320, 0), pt2=(320, 480), color=(0, 255, 255), thickness=3)
        cv2.line(frame, pt1=(0, 240), pt2=(640, 240), color=(0, 255, 255), thickness=3)
        # cv2.putText(frame, text="FPS : ".format(fps), org=(450, 0), fontFace=None, fontScale=4, color=(0, 0, 0),
        #             thickness=2) It shows fps value in screen.But Dont forget apply fps in down part
        material_center_point_x = []
        material_center_point_y = []

        material_center_point_x.append(circle_center_point1)
        material_center_point_y.append(circle_center_point2)

        center_point_x = Counter(material_center_point_x)
        center_point_y = Counter(material_center_point_y)

        if len(material_center_point_x) >= 100:
            material_center_point_x.clear()
            material_center_point_x.append(center_point_x)

        if len(material_center_point_y) >= 100:
            material_center_point_y.clear()
            material_center_point_y.append(center_point_y)

        print("Our center point is ({}, {})".format(center_point_x.most_common()[0][0],
                                                    center_point_y.most_common()[0][0]))

    # Detect number of pixel the object in 1/ 2 / 5 /10/ 12/ 15/ 18/ 20/ 22/ 25/ 30 meters
    # Apply y = mx + c formula when y = meters, x = number of pixel and m = slope, c = constant
    # According to this variables(m,c) we can predict distance of material(y), don't forget(we already know x value)
    # print(matrix.sum( ) / 255)
    distance = (matrix.sum() / 255) * -0.004 + 46.6
    print("Distance : {}".format(distance))

    # print(matrix.sum())
    cv2.imshow("Normal Frame", frame)

    key = cv2.waitKey(1)
    end = time.time()
    seconds = end - start
    fps = 1 / seconds
    # print("FPS : {}".format(fps))

    if key == 27:  # when you press "ESC" key Frame will shut down

        break
cv2.destroyAllWindows()
