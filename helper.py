import math
import numpy as np
import cv2
from scipy import stats


def preproc_yw(img):
    # return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Unlike the given "grayscale" helper function, convert the image to HLS space
    # to isolate only yellow and white colors for better processing
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    yellow_ulim = np.array([45, 255, 255], dtype="uint8")
    yellow_llim = np.array([15, 120, 150], dtype="uint8")
    white_ulim = np.array([180, 50, 255], dtype="uint8")
    white_llim = np.array([0, 0, 200], dtype="uint8")

    yellow_mask = cv2.inRange(img_hsv, yellow_llim, yellow_ulim)
    yellow_img = cv2.bitwise_and(img, img, mask=yellow_mask)

    white_mask = cv2.inRange(img_hsv, white_llim, white_ulim)
    white_img = cv2.bitwise_and(img, img, mask=white_mask)

    img_yw = cv2.cvtColor(yellow_img, cv2.COLOR_RGB2GRAY) + cv2.cvtColor(white_img, cv2.COLOR_RGB2GRAY)
    return img_yw

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


# def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
def draw_lines(img, lines):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    #         cv2.line(img, (x1, y1), (x2, y2), color, thickness)

    left_lane_endpoints = []
    right_lane_endpoints = []

    Left_Thd = -1
    Right_Thd = 1
    Slope_Tol = 0.8

    # Classify the lines and store the endpoints as left lane and right lane
    for line in lines:
        for x1,y1,x2,y2 in line:
            # determine if the line is left lane or right lane
            if (y2-y1)/(x2-x1) > Left_Thd-Slope_Tol and (y2-y1)/(x2-x1) < Left_Thd+Slope_Tol:
            # if (y2-y1)/(x2-x1) < 0: #left lane has negative slope
                left_lane_endpoints.append([x1,y1])
                left_lane_endpoints.append([x2,y2])
            elif (y2-y1)/(x2-x1) > Right_Thd-Slope_Tol and (y2-y1)/(x2-x1) < Right_Thd+Slope_Tol:
            # elif (y2-y1)/(x2-x1) > 0: #right lane has positive slope
                right_lane_endpoints.append([x1,y1])
                right_lane_endpoints.append([x2,y2])

    # Run linear regression to get the generalized left and right lane equation
    # left_lane_endpoints = np.asarray(left_lane_endpoints)
    # right_lane_endpoints = np.asarray(right_lane_endpoints)
    left_lane = stats.linregress(left_lane_endpoints)
    right_lane = stats.linregress(right_lane_endpoints)

    # Draw the line
    ysize = img.shape[0]

    left_y1 = np.float32(0.6*ysize)
    left_y2 = np.float32(ysize)
    left_x1 = np.float32((left_y1 - left_lane.intercept)/left_lane.slope)
    left_x2 = np.float32((left_y2 - left_lane.intercept)/left_lane.slope)

    right_y1 = np.float32(0.6*ysize)
    right_y2 = np.float32(ysize)
    right_x1 = np.float32((right_y1 - right_lane.intercept)/right_lane.slope)
    right_x2 = np.float32((right_y2 - right_lane.intercept)/right_lane.slope)

    cv2.line(img, (left_x1, left_y1), (left_x2, left_y2), [255,0,0], 5)
    cv2.line(img, (right_x1, right_y1), (right_x2, right_y2), [0,0,255], 5)



def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)
