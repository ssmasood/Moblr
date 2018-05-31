
# coding: utf-8

# In[4]:

#from matplotlib import pyplot as plt
import numpy as np 
import cv2
import imgHelper
import csv


def main():
    name = input("Enter the name of your video file (include .mp4, .avi, etc): ")
    distances, ymax = readVideo(name)
    #imgHelper.graph(distances, ymax)
    
def readVideo(name):
    vidcap = cv2.VideoCapture(name)
    totalFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    calibrated = False
    rows = []
    with open("output %s.csv" % name[0:-4], 'w') as f:
        writer = csv.writer(f)
        for frame in range(0,totalFrames):
            success,img = vidcap.read(0)
            if not success:
                writer.writerow([frame, -1])
                continue
            elif not calibrated:
                img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
                img = cv2.GaussianBlur(img,(5,5), 0)
                Rwidth, Lwidth, Uheight, Dheight, threshold = imgHelper.calibrateImage(img)
                if threshold == 0:
                    writer.writerow([frame, -1])
                    continue
                else:
                    calibrated = True
            else:
                img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
                img = cv2.GaussianBlur(img,(5,5), 0)
            ret, img = cv2.threshold(img, threshold, 255, 0)
            img = img[Dheight:Uheight, Lwidth:Rwidth]
            row = []
            for i in range(Uheight-Dheight):
                if 255 in img[i,:]:
                    row.append(i)
            if len(row) > 5:
                rows.append((Uheight-Dheight)-row[len(row)//2])
            else:
                if rows:
                    rows.append(rows[-1])
            writer.writerow([frame, rows[-1]])
    return rows, Uheight-Dheight

if __name__ == "__main__":
    main()

