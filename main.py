import cv2
import numpy as np
import potrace


def get_edges(image, lower_threshold=50, upper_threshold=150):
    image_read = cv2.imread(image)
    edges = cv2.Canny(image_read, lower_threshold, upper_threshold)
    return edges


def get_traces(data):
    data[data > 1] = 1  # Simplified this line
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.POTRACE_TURNPOLICY_MINORITY, 1.0, 1, 0.5)
    return path


def get_bezier_curves(path):
    bezier_curves = []
    for curve in path:
        segments = curve.segments
        for segment in segments:
            if segment.is_corner:
                # For corner segments, we'll use a straight line (linear Bézier)
                start_point = segment.c
                end_point = segment.end_point
                bezier_curves.append((start_point, end_point))
            else:
                # For curve segments, we'll extract the cubic Bézier control points
                start_point = segment.c
                control1 = segment.control1
                control2 = segment.control2
                end_point = segment.end_point
                bezier_curves.append((start_point, control1, control2, end_point))
    return bezier_curves


image_path = "amomo.jpg"
edges = get_edges(image_path)
traces = get_traces(edges)
bezier_curves = get_bezier_curves(traces)

for i, curve in enumerate(bezier_curves):
    print(f"Curve {i + 1}:")
    if len(curve) == 2:
        print("  Linear Bézier (straight line)")
        print(f"    Start point: {curve[0]}")
        print(f"    End point: {curve[1]}")
    else:
        print("  Cubic Bézier curve:")
        print(f"    Start point: {curve[0]}")
        print(f"    Control point 1: {curve[1]}")
        print(f"    Control point 2: {curve[2]}")
        print(f"    End point: {curve[3]}")
