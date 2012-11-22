#!/usr/bin/env python

import cv
from time import sleep

TIMEOUT = 60
OUT_DIR = "results/"

WINDOW_NAME = "Preview"

class Target:
    def __init__(self, camera_id = 0):
        self.capture = cv.CaptureFromCAM(camera_id)
        cv.NamedWindow(WINDOW_NAME, 1)

    def run(self):
        while True:
            img = cv.QueryFrame(self.capture)
            cv.ShowImage(WINDOW_NAME, img)

            # Listen for ESC key
            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break

if __name__=="__main__":
    t = Target(1)
    t.run()

