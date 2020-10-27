
import cv
import time
import serial
import os

#hsv_min = cv.Scalar(20,100,100)
#hsv_max = cv.Scalar(30,255,255)
#HSV means Hue-Saturation-Value, where the Hue is the color.Saturation is the greyness,
#so that a Saturation value near 0 means it is dull or grey looking.
#And Value is the brightness of the pixel.
#cv.Scalar(welke kleur(berijk is anders),hoe ver naar de grijs tint,ZWART WAARDE(SCHADUW))
#BLAUW
os.chdir('Z:\DCC-003-TD\pdwater\project\webcam\python\\video')
hsv_min = cv.Scalar(85,50,100)
hsv_max = cv.Scalar(120,255,255)
detect_threshold = 10 #frames
HSV_threshold = 5

    #For example, in MS Paint, it is 0-239. But OpenCVs hue values range from 0-179.
    #So you need to scale any hue value you take from MS Paint (multiple the hue from MS Paint by 180/240).
def getthresholdedimg(im):

  #this function take RGB image.Then convert it into HSV for easy colour detection and threshold it with yellow and blue part as white and all other regions as black.Then return that image'''
  global imghsv
  imghsv=cv.CreateImage(cv.GetSize(im),8,3)
  cv.CvtColor(im,imghsv,cv.CV_BGR2HSV) # Convert image from RGB to HSV
  imgthreshold=cv.CreateImage(cv.GetSize(im),8,1)

  #Values 20,100,100 to 30,255,255 working perfect for yellow at around 6pm
  cv.InRangeS(imghsv, hsv_min, hsv_max, imgthreshold);
  return imgthreshold

x_co = 0
y_co = 0
def on_mouse(event,x,y,flag,param):
  global x_co
  global y_co
  global PickColor
  if(event==cv.CV_EVENT_LBUTTONDOWN):
    PickColor = True
  if(event==cv.CV_EVENT_MOUSEMOVE):
    x_co=x
    y_co=y


ser = serial.Serial()
ser.baudrate = 19200
ser.port = 0
ser.open()

capture=cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)    
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 960)
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 720)    
frame = cv.QueryFrame(capture)
frame_size = cv.GetSize(frame)
first = True
grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
scan_movement_from_y = 3
scan_movement_from_x = 160
detect_counter_left = 0
detect_counter_right = 0
detect_right = False
detect_left = False
PickColor = False
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)

var = raw_input("Enter output filename for video: ")
var = os.getcwd()+ '\\' + var + '.avi'
fps = 24.0
width = 960
height = 720
fourcc = cv.CV_FOURCC('P','I','M','1')
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
writer = cv.CreateVideoWriter(var, fourcc, fps, (width, height), 1)



while(1):
    time_start = time.time()
    color_image = cv.QueryFrame(capture)
    imdraw=cv.CreateImage(cv.GetSize(frame),8,3)
    cv.SetZero(imdraw)
    cv.Flip(color_image,color_image,1)
    cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
    
    #find movement
    
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
        if scan_movement_from_y < pt1[1]:
            cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)
            if scan_movement_from_x > pt1[0]:
                detect_left = True
            else:
                detect_right = True

    if detect_left:
        if detect_counter_left > detect_threshold:
            ser.write(chr(1))
            print "left"
        detect_counter_left = 0
        detect_left = False
    else:
        detect_counter_left += 1
        
    if detect_right:
        if detect_counter_right > detect_threshold:
            ser.write(chr(2));
            print "right"
        detect_counter_right = 0
        detect_right = False
    else:
        detect_counter_right += 1

    imgyellowthresh=getthresholdedimg(color_image)
    cv.Erode(imgyellowthresh,imgyellowthresh,None,3)
    cv.Dilate(imgyellowthresh,imgyellowthresh,None,10)
    img2=cv.CloneImage(imgyellowthresh)
    storage = cv.CreateMemStorage(0)

    #present HSV color
    cv.SetMouseCallback("Color tracking",on_mouse, 0);
    if  PickColor==True:
        PickColor = False
        hsv = cv.CreateImage(cv.GetSize(color_image), 8, 3)
        thr = cv.CreateImage(cv.GetSize(color_image), 8, 1)
        cv.CvtColor(color_image, hsv, cv.CV_BGR2HSV)
        s=cv.Get2D(hsv,y_co,x_co)
        print "H:",s[0],"      S:",s[1],"       V:",s[2]
        #cv.PutText(color_image,str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co),font, (55,25,255))
        #hsv_min = cv.Scalar(s[0]-HSV_threshold,s[1]-HSV_threshold,s[2]-HSV_threshold)
        #hsv_max = cv.Scalar(s[0]+HSV_threshold,s[1]+HSV_threshold,s[2]+HSV_threshold)
        hsv_min = cv.Scalar(s[0]-HSV_threshold,5,5)
        hsv_max = cv.Scalar(s[0]+HSV_threshold,255,255)


    #find color
    contour = cv.FindContours(imgyellowthresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []
    
    # This is the new part here. ie Use of cv.BoundingRect()
    while contour:
      # Draw bounding rectangles
      bound_rect = cv.BoundingRect(list(contour))
      contour = contour.h_next()
      # for more details about cv.BoundingRect,see documentation
      pt1 = (bound_rect[0], bound_rect[1])
      pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
      points.append(pt1)
      points.append(pt2)
      if pt1[1] > 1:
        scan_movement_from_y = pt1[1]
        scan_movement_from_x = pt1[0]
      cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(0,255,0), 1)

    cv.ShowImage("Color tracking",color_image)
    cv.WriteFrame(writer, color_image)
    cv.WriteFrame(writer, color_image)
    
    sec = time.time() - time_start
    #while sec < 0.048:
    #  sec = time.time() - time_start
    sec = time.time() - time_start
    if sec>0:
        print 1.0/sec
    
    if cv.WaitKey(1) == 27: 
      cv.DestroyWindow("Color tracking")
      ser.close()
      break