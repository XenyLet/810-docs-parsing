import math

import cv2
import matplotlib.pyplot as plt
import numpy as np

DESKEW_PAGE_TYPES = [
    "elements_list_page_1",
    "elements_list_other_pages",
    "specification"
]

DESKEW_PARAMS = {
    "elements_list_page_1": {
        "epsilon": 0.02,
        "corners": 4
    },
    "specification": {
        "epsilon": 0.02,
        "corners": 4
    },
    "elements_list_other_pages": {
        "filter_epsilon": 0.02,
        "epsilon": 0.0025,
        # "epsilon": 0.01,
        "corners": 6
    },
}

def draw_corners(corners, image):
    for index, c in enumerate(corners):
        character = chr(65 + index)
        cv2.putText(image, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

def _extract_corners(cnt, epsilon):
    _epsilon = epsilon * cv2.arcLength(cnt, True)
    approx_corners = cv2.approxPolyDP(cnt, _epsilon, True)
    # cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
    return sort_poins(np.concatenate(approx_corners).tolist())


def detect_corners_from_contour(cnt, page_type, test_img):
    """
    Detecting corner points form contours using cv2.approxPolyDP()
    Args:
        canvas: np.array()
        cnt: list
    Returns:
        approx_corners: list
    """
    params = DESKEW_PARAMS[page_type]

    approx_corners = _extract_corners(cnt, params["epsilon"])
    iters = 0
    max_it = 100
    max_eps = 0.02
    min_eps = 0
    cur_eps = max_eps
    tgt_corners = params["corners"]
    while iters < max_it:
        iters += 1
        approx_corners = _extract_corners(cnt, cur_eps)
        test_img_copy = test_img.copy()
        draw_corners(approx_corners, test_img_copy)
        l = len(approx_corners)
        if l > tgt_corners:
            min_eps = cur_eps
            cur_eps = (cur_eps + max_eps) / 2
        elif l < tgt_corners:
            max_eps = cur_eps
            cur_eps = (cur_eps - min_eps) / 2
        else:
            break

    if len(approx_corners) != params["corners"]:
        raise RuntimeError("Algrithm did not converge")
    # if "filter_epsilon" in params:
    #     epsilon = params["filter_epsilon"] * cv2.arcLength(cnt, True)
    #     filtered_contour = cv2.approxPolyDP(cnt, epsilon, True)
    # else:
    #     filtered_contour = cnt
    # filtered_contour = cnt
    #
    # if len(approx_corners) > params["corners"]:
    #
    # assert len(approx_corners) == params["corners"], "Incorrect corners number detected"

    # Rearranging the order of the corner points
    if page_type == "elements_list_page_1":
        pass
    elif page_type == "elements_list_other_pages":
        A, B, C, D, E, F = order_corners(approx_corners, w=test_img.shape[1], h=test_img.shape[0])
        test_img_copy = test_img.copy()
        draw_corners([A, B, C, D, E, F], test_img_copy)

        AD = np.array([A, D])
        EF = np.array([E, F])
        t, s = np.linalg.solve(np.array([AD[1] - AD[0], EF[0] - EF[1]]).T, EF[0] - AD[0])
        intersection = (1 - t) * AD[0] + t * AD[1]
        intersection = [round(c) for c in intersection]

        approx_corners = [A, B, F, intersection]

    return approx_corners


def get_max_contour(image):
    im = image.copy()
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(im, 70, 255, cv2.THRESH_BINARY)
    invert = cv2.bitwise_not(thresh)
    kernel = np.ones((3, 3), np.uint8)
    img_dilation = cv2.dilate(invert, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    return cnt


def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    min_x, min_y, max_x, max_y = min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)
    return [
        [min_x, min_y],
        [min_x, max_y],
        [max_x, max_y],
        [max_x, min_y],
    ]

def order_corners(corners, w, h):
    def _distance(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    # return in order left-to-right, up-to-down
    structured_corners = {
        i: c
        for i, c in enumerate(corners)
    }

    # get upper-left
    i, A = min(structured_corners.items(), key=lambda c_d: _distance([0,0], c_d[1]))
    structured_corners.pop(i)

    # get upper right
    i, B = min(structured_corners.items(), key=lambda c_d: _distance([w, 0], c_d[1]))
    structured_corners.pop(i)

    # get middle_left
    i, C = min(structured_corners.items(), key=lambda c_d: _distance([0, h/2], c_d[1]))
    structured_corners.pop(i)

    # get lower left
    i, E = min(structured_corners.items(), key=lambda c_d: _distance([0, h], c_d[1]))
    structured_corners.pop(i)

    # get lower right
    i, F = min(structured_corners.items(), key=lambda c_d: _distance([w, h], c_d[1]))
    structured_corners.pop(i)

    # only middle right must be left
    assert len(structured_corners) == 1
    D = list(structured_corners.values())[0]

    return A, B, C, D, E, F




def sort_poins(points: list):
    return sorted(points, key=lambda p: (p[1], p[0]))


def deskew_img(image: np.ndarray, page_type: str):
    if page_type not in DESKEW_PAGE_TYPES:
        raise ValueError("Incorrect Deskew page type")

    test_img = image.copy()

    max_contour = get_max_contour(image)
    cv2.drawContours(test_img, max_contour, -1, (255, 255, 0), 10)

    corners = detect_corners_from_contour(max_contour, page_type, test_img.copy())
    draw_corners(corners, test_img)

    bounding_rect = bounding_box(corners)

    corners = np.float32(sort_poins(corners))
    bounding_rect = np.float32(sort_poins(bounding_rect))

    matrix = cv2.getPerspectiveTransform(corners, bounding_rect)
    result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))

    return result
