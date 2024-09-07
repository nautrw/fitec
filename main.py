import cv2
import numpy as pd
import potrace


def get_edges(image, lower_threshold=50, upper_threshold=150):
    image_read = cv2.imread(image)
    edges = cv2.Canny(image_read, lower_threshold, upper_threshold)

    return edges


cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)
cv2.imshow("frame", get_edges("/home/leo/fitec/amomo.jpg"))
cv2.waitKey(0)
cv2.destroyAllWindows()
