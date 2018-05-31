
# coding: utf-8

# In[31]:


#from matplotlib import pyplot as plt
import numpy as np 
import cv2

def showFrame(name, number):
    vidcap = cv2.VideoCapture(name)
    vidcap.set(1, number)
    success, img = vidcap.read()
    print(success)
    img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
    calibrateImage(img)
    #tempimg = cv2.GaussianBlur(img,(5,5),0)
    #ret,th = cv2.threshold(tempimg,230,255,0)
    cv2.imshow("Image", th)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def writeImage(name, img):
    cv2.imwrite(name, img)

#def graph(distance, ymax):
#    plt.figure(figsize=(20,10))
#    plt.axis([0,len(distance),0,ymax])
#    plt.plot(range(0,len(distance)),distance)
#    plt.ylabel('Distance')
#    plt.xlabel('Frame')
#    plt.show()
    
def calibrateImage(img):
    # this function is needed for the createTrackbar step downstream
    def nothing(x):
        pass
    # create trackbar for canny edge detection threshold changes
    cv2.namedWindow('threshold', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('threshold', 600,400)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1280,720)
    # add ON/OFF switch to "canny"
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'threshold', 0, 1, nothing)


    # add lower and upper threshold slidebars to "canny"
    cv2.createTrackbar('Threshold', 'threshold', 0, 255, nothing)
    cv2.createTrackbar('UpperHeight', 'threshold', 0, img.shape[0]//2, nothing)
    cv2.createTrackbar('LowerHeight', 'threshold', 0, img.shape[0]//2, nothing)
    cv2.createTrackbar('LeftWidth', 'threshold', 0, img.shape[1]//2, nothing)
    cv2.createTrackbar('RightWidth', 'threshold', 0,img.shape[1]//2, nothing)


    # Infinite loop until we hit the escape key on keyboard
    while(1):

        # get current positions of four trackbars
        threshold = cv2.getTrackbarPos('Threshold', 'threshold')
        Rwidth = cv2.getTrackbarPos('RightWidth', 'threshold')
        Uheight = cv2.getTrackbarPos('LowerHeight', 'threshold')
        Lwidth = cv2.getTrackbarPos('LeftWidth', 'threshold')
        Dheight = cv2.getTrackbarPos('UpperHeight', 'threshold')
        Uheight = Uheight + img.shape[0]//2
        Rwidth = Rwidth + img.shape[1]//2
        s = cv2.getTrackbarPos(switch, 'threshold')

        if s == 0:
            edges = img
        else:
            edges = cv2.GaussianBlur(img,(5,5),0)
            ret,edges = cv2.threshold(edges,threshold,255,0)
            edges = edges[Dheight:Uheight, Lwidth:Rwidth]


        # display images
        cv2.imshow('original', img)
        cv2.imshow('image', edges)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:   # hit escape to quit
            break

    cv2.destroyAllWindows()
    return Rwidth, Lwidth, Uheight, Dheight, threshold

