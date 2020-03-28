# **Finding Lane Lines on the Road**

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/Step2.png "Grayscale"
[image2]: ./examples/Step3.png "Grayscale"
[image3]: ./examples/Step4.png "Grayscale"
[image4]: ./examples/Final.png

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

The lane detection image processing pipeline is consisted of 6 steps:

1. **Pre-Processing:** In this step, the image is converted to HLS color space. Unlike the provided helper function (which uses grayscale image), HLS color space provides better capability in separating different colors. The white and yellow sections of images are being extracted, all other colors are discarded, the masked image is then converted to grayscale for easier handling.

2. **Gaussian Blur:** In this step, the gaussian blur filter is applied to the image to smooth the edges.
![Image Output After Gaussian Blur][image1]

3. **Canny Edge Detection:** In this step, I use the canny edge detection algorithm to extract edges from the masked image.
![Image Output After Canny Edge Detection][image2]

4. **Mask Region-of-Interest:** In this step, a polygon area is defined with the image x and y sizes in mind (ROI is defined as a function of the image height and width). I always start with the left and right bottom corner of the image, then go up roughly 60% of the image height and roughly 48% away from left and right sides of image. After this, the masked image should contain only car lane edges.  
![Detected Edges in Region-of-Interest][image3]

5. **Hough Transform:** In this step, the masked edges are fed through a Hough transformation. The connected lines are recognized.

6. **Reconstruct Car Lane:** With the lines recognized from Hough transform, the next step will be to reconstruct and draw the car lanes on the original image. I would like to have an averaged/extrapolated line, so the sub-steps taken are:
  **(1) Categorize left and right lane lines:** I use the slope of lines to determine whether it belongs to left lane or right lane group. I then put the [x,y] coordinates of the lines to a bucket where I store all the endpoints for left/right lanes respectively.
  **(2) Run Linear Regression:** The best method to get an averaged car lane from endpoints would be running a linear regression, the least square method is used. This will give me the slope and intercept of the car lanes (left and right respectively).
  **(3) Draw Car Lanes:** After I have the slope and intercept of the left and right car lane, I can now draw the lanes on the original image with a given upper and lower bound for y axis.

The final result will look like below image:
![Final Output Image with Lane Lines Marked][image4]

### 2. Identify potential shortcomings with your current pipeline

The potential shortcomings of the current pipeline include:

1. **Failure to recognize lane lines at low contrast:** When running the challenge video with the current pipeline, the code was unable to recognize car lanes when the color contrast gets lower - when the road surface changes from asphalt (darker color) to concrete (yellow-white-ish color, 00:04-00:06 of challenge video).

2. **Non-ideal performance when lane lines are curvy:** Because the current pipeline uses linear regression to average all lane lines recognized, the represented car lanes looked less than ideal when the lanes are curvy.

### 3. Suggest possible improvements to your pipeline

A possible future update to this pipeline would be to improve the code robustness to combat with low contrast frames and sudden lost of lane-recognition. Possible solutions could include: pre-process the image to increase contrast before feeding into the pipeline; add "if-then" criteria to the code to handle cases when no lanes are recognized; use the result from last frame as a "low-fidelity" alternative when this scenario happens.

Another improvement would be to better deal with curvy roads, instead of always using linear regression, a second-order polynomial regression could be used to improve lane line quality at curvy roads.
