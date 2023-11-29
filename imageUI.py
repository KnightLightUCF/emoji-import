import cv2 

global coordinates
coordinates = []


def calculateCoords(start, end):
    xdistance = end[0] - start[0]
    ydistance = end[1] - start[1]
    for i in range(xdistance):
        for j in range(ydistance):
            coordinates.append((i+start[0], j+start[1]))
    coordinates.append(end)
    print(coordinates)
    

   
def drag(event, x, y, flags, params):
    global dragging
    global startCoord
    global endCoord
    
    if event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        startCoord = (x, y)
        print(x, ' ', y)
        
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        endCoord = (x, y)
        calculateCoords(startCoord, endCoord)
        print(x, ' ', y)
    for item in coordinates:
         newimage = cv2.rectangle(img,startCoord,endCoord,(0,255,0),-1)
         cv2.imshow('new', newimage)
        
if __name__=="__main__": 
    # reading the image 
    img = cv2.imread('knightro1.jpg', 1) 

    # displaying the image 
    cv2.imshow('image', img) 

    # setting mouse handler for the image 
    # and calling the click_event() function 
    cv2.setMouseCallback('image', drag) 

    # wait for a key to be pressed to exit 
    cv2.waitKey(0) 

    # close the window 
    cv2.destroyAllWindows() 