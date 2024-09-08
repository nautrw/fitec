import cv2
import numpy as np
import potrace


def get_edges(image, lower_threshold=50, upper_threshold=150):
    image_read = cv2.imread(image)
    edges = cv2.Canny(image_read, lower_threshold, upper_threshold)
    return edges


def get_traces(data):
    data[data > 1] = 1
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.POTRACE_TURNPOLICY_MINORITY, 1.0, 1, 0.5)
    return path


def get_bezier_curves(path):
    bezier_curves = []
    for curve in path:
        segments = curve.segments
        for segment in segments:
            if segment.is_corner:
                start_point = segment.c
                end_point = segment.end_point
                bezier_curves.append((start_point, end_point))
            else:
                start_point = segment.c
                control1 = segment.control1
                control2 = segment.control2
                end_point = segment.end_point
                bezier_curves.append((start_point, control1, control2, end_point))
    return bezier_curves


def get_latex(filename):
    latex = []
    path = get_traces(get_edges(filename))

    for curve in path.curves:
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0, y0 = start.x, start.y
            if segment.is_corner:
                x1, y1 = segment.c.x, segment.c.y
                x2, y2 = segment.end_point.x, segment.end_point.y
                latex.append(f"((1-t){x0}+t{x1},(1-t){y0}+t{y1})")
                latex.append(f"((1-t){x1}+t{x2},(1-t){y1}+t{y2})")
            else:
                x1, y1 = segment.c1
                x2, y2 = segment.c2
                x3, y3 = segment.end_point
                latex.append(
                    f"((1-t)((1-t)((1-t){x0}+t{x1})+t((1-t){x1}+t{x2}))+t((1-t)((1-t){x1}+t{x2})+t((1-t){x2}+t{x3})),(1-t)((1-t)((1-t){y0}+t{y1})+t((1-t){y1}+t{y2}))+t((1-t)((1-t){y1}+t{y2})+t((1-t){y2}+t{y3})))"
                )
            start = segment.end_point
    return latex


image_path = "amomo.jpg"
edges = get_edges(image_path)
traces = get_traces(edges)
print(traces)
bezier_curves = get_bezier_curves(traces)
print(bezier_curves)

for i in get_latex("amomo.jpg"):
    print(i)
