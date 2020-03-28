#importing some useful packages
import numpy as np
import helper as h

def process_image(image):

    ysize = image.shape[0]
    xsize = image.shape[1]

    ## Parameter Tuning: change and optimize parameters here:
    ks = 5 # kernel_size for GaussianBlur
    lo_thd = 50 # low_threshold for canny edge detection
    hi_thd = 150 # high_threshold for canny edge detection
    ROI_vertices = np.array([[(0, ysize),(0.48*xsize, 0.6*ysize), (0.52*xsize, 0.6*ysize), \
    (xsize, ysize)]], dtype=np.int32) # boundaries for masking lane line region
    # below are hough transform parameters
    rho = 1 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 30     # minimum number of votes (intersections in Hough grid cell)
    min_line_len = 20 # minimum number of pixels making up a line
    max_line_gap = 15    # maximum gap in pixels between connectable line segments

    # Pre-process the image to include only yellow and white
    img_yw = h.preproc_yw(image)

    # Process the image - canny with masked region
    img_yw_blur = h.gaussian_blur(img_yw, ks)
    edges = h.canny(img_yw_blur, lo_thd, hi_thd)
    edges_masked = h.region_of_interest(edges, ROI_vertices)

    # Run Hough Xform and draw the lines
    img_line = h.hough_lines(edges_masked, rho, theta, threshold, min_line_len, max_line_gap)
    img_comb = h.weighted_img(img_line, image)

    return img_comb
