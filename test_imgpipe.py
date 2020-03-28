from ImagePipeline import process_image
import matplotlib.pyplot as plt
import cv2


# select an image to work with
# image = cv2.imread('test_images/solidWhiteRight.jpg')
# image = cv2.imread('test_images/solidWhiteCurve.jpg')
# image = cv2.imread('test_images/solidYellowCurve.jpg')
# image = cv2.imread('test_images/solidYellowCurve2.jpg')
# image = cv2.imread('test_images/solidYellowLeft.jpg')
image = cv2.imread('test_images/whiteCarLaneSwitch.jpg')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
out_img = process_image(image)
plt.imshow(out_img)
