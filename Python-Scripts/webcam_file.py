#!/usr/bin/env python

import cv
import os
import time

fps = 24.0
width = 960
height = 720

var = raw_input("Enter output filename for video: ")
var = os.getcwd()+ '\\' + var + '.avi'
fourcc = cv.CV_FOURCC('D', 'I', 'V', 'X')
#MPEG-1 only supports framerates of 23.976, 24, 25, 29.97, 30, 50, 59.94, and 60. Anything else is out of spec.
#CV_FOURCC('P','I','M','1')    = MPEG-1 codec
#CV_FOURCC('M','J','P','G')    = motion-jpeg codec (does not work well)
#CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2 codec
#CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3 codec
#CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4 codec
#CV_FOURCC('U', '2', '6', '3') = H263 codec
#CV_FOURCC('I', '2', '6', '3') = H263I codec
#CV_FOURCC('F', 'L', 'V', '1') = FLV1 codec
#writer = cv.CreateVideoWriter('Z:\DCC-003-TD\pdwater\project\webcam\python\\video\\baby.avi', fourcc, fps, (width, height), 1)

capture=cv.CaptureFromCAM(0)
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)    
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 960)
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 720)    
frame = cv.QueryFrame(capture)
frame_size = cv.GetSize(frame)
writer = cv.CreateVideoWriter(var, fourcc, fps, (width, height), 1)
time_start = time.time()

while(1):
    color_image = cv.QueryFrame(capture)
    cv.ShowImage("Color tracking",color_image)
    cv.WriteFrame(writer, color_image)
    
    sec = time.time() - time_start
    if sec > 0:
      print 1.0/sec
    time_start = time.time()

    if cv.WaitKey(2) == 27: 
      cv.DestroyWindow("Color tracking")
      break            
