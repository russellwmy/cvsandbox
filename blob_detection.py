#!/usr/bin/env python

import cv
import numpy
from scipy.cluster.vq import *

class Target:

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        cv.NamedWindow("Target", 1)

    def run(self):
        # Capture first frame to get size
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        color_image = cv.CreateImage(cv.GetSize(frame), 8, 3)
        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)

        first = True
        detected = []
        
        while True:
            closest_to_left = cv.GetSize(frame)[0]
            closest_to_right = cv.GetSize(frame)[1]

            color_image = cv.QueryFrame(self.capture)

            # Smooth to get rid of false positives
            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 5, 0)

            if first:
                difference = cv.CloneImage(color_image)
                temp = cv.CloneImage(color_image)
                cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
                first = False
            else:
                cv.RunningAvg(color_image, moving_average, 0.020, None)

            # Convert the scale of the moving average.
            cv.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.AbsDiff(color_image, temp, difference)

            # Convert the image to grayscale.
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)

            # Convert the image to black and white.
            cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

            # Dilate and erode to get people blobs
            cv.Dilate(grey_image, grey_image, None, 18)
            cv.Erode(grey_image, grey_image, None, 10)

            storage = cv.CreateMemStorage(0)
            contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            points = []
            while contour:
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()

                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                # cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

                
            if len(points):
                try:
                    res, idx = kmeans2(numpy.asarray(points),2)
                    detected = []
                    detected.append([res[0][0], res[0][1]])
                    for i, item1 in enumerate(res):
                        for item2 in  res[i:]:
                            dist = numpy.sqrt(numpy.sum((item1-item2)**2))
                            if dist > 100 and [item2[0], item2[1]] not in detected :
                                detected.append([item2[0], item2[1]])
                except:
                    pass
                for item in detected:
                    x = int(item[0])
                    y = int(item[1])
                    cv.Circle(color_image, (x,y), 50, cv.CV_RGB(255, 100, 0), 1)
                print len(detected)
                

            cv.ShowImage("Target", grey_image)

            # Listen for ESC key
            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break

if __name__=="__main__":
    t = Target()
    t.run()
    
