import numpy as np
import cv2

def detect(im):


    """
    Script using OpenCV's Hough transforms for reading images of 
    simple dials.
    """

    # load grayscale image
    gray_im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    # create version to draw on and blurred version
    draw_im = cv2.cvtColor(gray_im, cv2.COLOR_GRAY2BGR)
    blur = cv2.GaussianBlur(gray_im, (0,0), 5)

    m,n = gray_im.shape

    # Hough transform for circles
    # cv2.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]
    circles = cv2.HoughCircles(gray_im, cv2.cv.CV_HOUGH_GRADIENT, 2, 10, np.array([]), 20, 60, m/20)[0]

    # Hough transform for lines (regular and probabilistic)
    # edges = cv2.Canny(blur, 20, 60)
    # lines = cv2.HoughLines(edges, 2, np.pi/90, 40)[0]
    # plines = cv2.HoughLinesP(edges, 1, np.pi/180, 20, np.array([]), 10)[0]

    # draw 
    for c in circles[:3]:
        # green for circles (only draw the 3 strongest)
        cv2.circle(draw_im, (c[0],c[1]), c[2], (0,255,0), 2) 

    #for (rho, theta) in lines[:5]:
    #    # blue for infinite lines (only draw the 5 strongest)
    #    x0 = np.cos(theta)*rho 
    #    y0 = np.sin(theta)*rho
    #   pt1 = ( int(x0 + (m+n)*(-np.sin(theta))), int(y0 + (m+n)*np.cos(theta)) )
    #    pt2 = ( int(x0 - (m+n)*(-np.sin(theta))), int(y0 - (m+n)*np.cos(theta)) )
    #    cv2.line(draw_im, pt1, pt2, (255,0,0), 2) 

    # for l in plines:
        # red for line segments
    #     cv2.line(draw_im, (l[0],l[1]), (l[2],l[3]), (0,0,255), 2)
      
    cv2.imshow("circles",draw_im)

capture = cv2.VideoCapture(0)
while True:
    _,img = capture.read()
    detect(img)
    if cv2.waitKey(5) == 27:
         break
