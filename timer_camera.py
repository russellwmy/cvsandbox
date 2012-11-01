#!/usr/bin/env python

import cv
from time import sleep

TIMEOUT = 60
OUT_DIR = "results/"

class Target:


    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)

    def run(self, fname_fs = "img_%s.jpg"):
        # Capture first frame to get size
        i = 0
        while True:
            color_image = cv.QueryFrame(self.capture)
            fname = OUT_DIR + fname_fs % (i)
            cv.SaveImage(fname, color_image)
            print fname + " saved"
            i += 1
            sleep(TIMEOUT)

if __name__=="__main__":
    t = Target()
    t.run()
