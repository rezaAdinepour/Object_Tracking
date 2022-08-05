import cv2 as cv
from tracker import *

tracker = EuclideanDistTracker()


cap = cv.VideoCapture('highway.mp4')
objectDetector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=50)


while(cap.isOpened()):
    ret, frame = cap.read()
    #height, width, _ = frame.shape
    #print(height, width)

    #part of original frame
    pof = frame[400:700, 480:1100]

    #image optimization
    mask = objectDetector.apply(pof)
    blur = cv.GaussianBlur(mask, (15, 15), 0)
    _, thresh = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=8)

    #find object
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    detectPos = []
    for contour in contours:
        area = cv.contourArea(contour)
        if(area > 970):
            #cv.drawContours(roi, contour, -1, (0, 255, 0), 2)
            (x, y, w, h) = cv.boundingRect(contour)
            detectPos.append([x, y, w, h])

    # track object
    boxIDs = tracker.update(detectPos)
    for boxID in boxIDs:
        (x, y, w, h, ID) = boxID
        cv.putText(pof, str(ID), (x, y - 5), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
        cv.rectangle(pof, (x, y), (x + w, y + h), (0, 255, 0), 3)


    #print(boxIDs)
    #print(detectPos)

    cv.imshow('frame', frame)
    #cv.imshow('mask', mask)
    #cv.imshow('blur', thresh)
    #cv.imshow('roi', roi)
    #cv.imshow('thresh', thresh)
    #cv.imshow('dilate', dilated)


    key = cv.waitKey(30)
    if(key == 27):
        break

cap.release()
cv.destroyAllWindows()