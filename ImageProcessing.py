# -*- coding: utf-8 -*-

import cv2
import numpy as np
import InputOutput
import kmean
import locationDetection

#fx = 517 * 0.5 # focal length is calculated for 320x240
fx = 843
obj_width = 0.305 #meters
BLACK = 0
WHITE = 255

"""
*checkes to see if the ball is in the image
*returns fase if the ball is not in the image
"""
def inImage(image, x, y, r):
    dimator = 2*r
    height, width = image.shape 
    if ((dimator  > height) or  (dimator > width)):
        return False
    elif (((x-r) < 0) or ((y-r) <0) or ((y+r) > height) or ((x +r) >width)):
      return False
    else:
        return True

#Attempts to remove reflections o the balls off the water
#returns the image with any felections found removed
def reflectionDetection(image):
    #first find any ball candidates.
    sensitivity = 2.7
    initial_ball_locs = getBalls(image,sensitivity)
    
    circles = [] #the list of found circles
    if not initial_ball_locs == None:
        for candidate_loc in initial_ball_locs:
            clean_image = image.copy()
            top=goToTop(candidate_loc[0],candidate_loc[1],image)
            
            #Setup x and y trackers for left and right
            x_left = top[0]
            y_left = top[1]
            x_right = top[0]
            y_right = top[1]
            
            #Setup tracking positions for reflection detection
            left_farthest = (x_left,y_left)
            right_farthest = (x_right,y_right)
            
            left_close_pos = (x_left,y_left)
            right_close_pos = (x_right,y_right)
            #constants
            max_step_size = 25
            min_percent_decline = .1
            
            while(True):
                #the middle x is tracked to allow the left and right trackers to travel farther
                #If a sharp drop off is tracked towards the center the left or right will keep
                #searching until the middle point
                middle_x = (right_farthest[0] + left_farthest[0])/2
                
                #Move one step downward along the edge of the object. 
                leftPos = stepDown(image,x_left,y_left,-1,middle_x,max_step_size)
                rightPos = stepDown(image,x_right,y_right,1,middle_x,max_step_size)
                
                if(leftPos != None and rightPos != None):
                    #Check if both left and right are below their max position this we are on the downslope 
                    # of the circle no reason to continue
                    left_declining = (leftPos[0] - left_farthest[0]>(middle_x-left_farthest[0])*(min_percent_decline))
                    right_declining = (right_farthest[0]-leftPos[0]>(middle_x-right_farthest[0])*(min_percent_decline))
                    
                    if(left_declining and right_declining):
                        break
                    
                    left_farthest,right_farthest,left_close_pos,right_close_pos = \
                        updateMinMax(leftPos,rightPos,left_farthest,right_farthest,left_close_pos,right_close_pos)
                    x_left = leftPos[0]
                    y_left = leftPos[1]
                    x_right = rightPos[0]
                    y_right = rightPos[1]
                    cv2.rectangle(clean_image, (x_left - 2, y_left - 2), (x_left + 2, y_left + 2), 190, -1)
                    cv2.rectangle(clean_image, (x_right - 2, y_right - 2), (x_right + 2, y_right + 2), 190, -1)
                else:
                    break
            #Display image
            cv2.rectangle(clean_image, (x_left - 2, y_left - 2), (x_left + 2, y_left + 2), 85, -1)
            cv2.rectangle(clean_image, (x_right - 2, y_right - 2), (x_right + 2, y_right + 2), 85, -1)
            InputOutput.display_image(clean_image,"Show Bottom")
            
            circleX = (right_farthest[0] + left_farthest[0])/2
            circleY = (right_farthest[1] + left_farthest[1])/2
            circle_radius = (right_farthest[0] - left_farthest[0])/2
            circles.append((circleX,circleY,circle_radius))
    
    print "Output Circles: " + str(circles)
    print "Initial Ball Locations: " + str(initial_ball_locs)
    return circles

#updates the min and max positions as required
def updateMinMax(leftPos,rightPos,left_farthest,right_farthest,left_close_pos,right_close_pos):
    if(leftPos[0]<left_farthest[0]):
        left_farthest = leftPos
    elif(leftPos[0]>left_close_pos[0]):
        left_close_pos = leftPos
    
    if(rightPos[0]>right_farthest[0]):
        right_farthest = rightPos
    elif(rightPos[0]<right_close_pos[0]):
        right_close_pos = rightPos
        
    return (left_farthest,right_farthest,left_close_pos,right_close_pos)
        

#Finds the top of an object given a location in that image
def goToTop(x,y,image):
    width = image.shape[1]
    
    #store original value for display
    x1=x
    y1=y
    
    #Check x and y are within bounds
    if(x>=width or y>= image.shape[0]):
        cv2.rectangle(image, (x - 2, y - 2), (x + 2, y + 2), 175, -1)
        InputOutput.display_image(image,"GoToTop")
        InputOutput.printWarning("goToTop given invalid x,y: " + str((x,y)) + " - Dimensions: " + str(image.shape))
        return (x,y)
    else:
        print "GoToTop given valid x,y: " + str((x1,y1))
    
    
    #move up until black is found
    maxSearchRadius = 3
    searchRadius = 0
    
    #if given a black pixel this is a failure
    if(image[y,x]==BLACK):
        InputOutput.printWarning("goToTop given a black pixel)")
        InputOutput.display_image(image,"GoToTop")
        return (x,y)
        
    while(searchRadius<maxSearchRadius and y>0 and x+searchRadius<width and x-searchRadius>0):
        if image[y-1,x+searchRadius] != BLACK:
            x=x+searchRadius
            y=y-1
            searchRadius=0
        elif image[y-1,x-searchRadius] != BLACK:
            x=x-searchRadius
            y=y-1
            searchRadius=0
        else:
            searchRadius+=1 
            
    #display the starting location and ending location
    cv2.rectangle(image, (x1 - 2, y1 - 5), (x1 + 2, y1 + 2), 75, -1)
    cv2.rectangle(image, (x - 2, y - 2), (x + 2, y + 2), 175, -1)
    InputOutput.display_image(image,"GoToTop")
    return (x,y)
    
#Take one step down the sides of the image. 
#maxStepSize is the maximum x direction movement or a step
#direction is an integer which is 1 for right and -1 or left
#returns an (x,y) position if found. 
#returns None otherwise
def stepDown(image,x,y,direction,middle_x,max_step_size):
    #Check bounds. This formula is overly agressive
    if(image.shape[1] > y+1 and image.shape[0] <= x+max_step_size and 0 > x-max_step_size):
        return None
    x_new = x + direction * max_step_size
    while image[y+1,x_new] == BLACK and (abs(x_new - x) <= max_step_size or (direction * middle_x < x_new*direction)):
        x_new-=direction
    if abs(x_new - x) > max_step_size and (direction * middle_x >= x_new*direction):
        return None
    else: 
        return (x_new,y+1)
    
def getBalls(image,sensitivity):
    #Apply the Hough Transform to find the circles
    circles = cv2.HoughCircles(image,cv2.cv.CV_HOUGH_GRADIENT,sensitivity , 5) #2.3 is tp be screwed 2.5 is good
    
    #/// Apply the Hough Transform to find the circles
    if (circles is None):
        print "Hough transform called but no circles found."
        output = image.copy()
        InputOutput.display_image(np.hstack([image, output]),"houghTransform")
        return circles
    else:
        circlexList = []
        circleyList = []
        circlerList = []
        circleList = []
        circles = np.round(circles[0, :]).astype("int")

        output = image.copy()
        # loop over the (x, y) coordinates and radius of the circles
       
        Sum_x=0
        Sum_y=0
        Sum_r=0

        count =0 
        for (x, y, r) in circles:
            #get average circle
			if inImage(output,x,y,r):
				count = count+1            
				Sum_x= Sum_x +x #((ax*count)+x)/(count+1)
				Sum_y= Sum_y +y #((ay*count)+y)/(count+1)
				Sum_r= Sum_r + r #((ar*count)+r)/(count+1)
				#avaragedCircle=
				
				circlexList.append(x)
				circleyList.append(y)
				circlerList.append(r)
				
				tempCirc = (x, y, r)
				circleList.append(tempCirc)
				# draw the circle in the output image, then draw a rectangle
				# corresponding to the center of the circle
				
				cv2.circle(output, (x, y), r, (120, 255, 0), 4)
				cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            
        
        centeredCircles = kmean.findAvarages(circleList)
        centerCirc1= centeredCircles[0]
        centerCirc2= centeredCircles[1]
        radSum =(centerCirc1[2])+(centerCirc2[2])
        distBetween= kmean.getDistBetween(centerCirc1, centerCirc2)
        
        print "centeredCircles: " + str(centeredCircles) 
        #print "total radius = " + str(radSum)
        #print "distance between = " + str(distBetween)
        if ( (distBetween - radSum) <0 ): # determins is if there is overlap of the 2 circles
            print "1 ball detected"
            ax = Sum_x/count
            ay = Sum_y/count
            ar = Sum_r/count
            circ = (ax, ay, ar)
            
            #print the average circle
            cv2.circle(output, (ax, ay), ar, (239, 239, 239), 4)
            cv2.rectangle(output, (ax -5, ay -5), (ax+ 5, ay+5), (239, 239, 239), -1)
            locationDetection.getDistance(circ)
            locationDetection.getDeg(circ)

            #return the single average circle            
            final_circles = ((ax,ay,ar),)
            
        else:
            print "2 balls detected"
            
            #print both circles
            cv2.circle(output, (centerCirc2[0], centerCirc2[1]), centerCirc2[2], (239, 239, 239), 4)
            cv2.rectangle(output, (centerCirc2[0] - 5, centerCirc2[1] - 5), (centerCirc2[0] + 5, centerCirc2[1] + 5), (239, 239, 239), -1)
            cv2.circle(output, (centerCirc1[0], centerCirc1[1]), centerCirc1[2], (239, 239, 239), 4)
            cv2.rectangle(output, (centerCirc1[0] - 5, centerCirc1[1] - 5), (centerCirc1[0] + 5, centerCirc1[1] + 5), (239, 239, 239), -1)   
            temp = locationDetection.getDistance2balls(centerCirc1, centerCirc2)
            locationDetection.getDeg2Circs(centerCirc1, centerCirc2)
            
            #return the two circles            
            final_circles = ((centerCirc1[0], centerCirc1[1],centerCirc1[2]),(centerCirc2[0], centerCirc2[1],centerCirc2[2]))
        
        # show the output image
        InputOutput.display_image(np.hstack([image, output]),"houghTransform")
        return final_circles

#Convert the image from a color image to a thresholded image
def thresholdRed(image):
    #minGBR = (25, 14, 50)#(0,26,100) # 0,50,120
    #maxGBR = (130, 110, 255)#(15,243,255) #15, 200, 255
   # minGBR = ( 42, 50, 14)
   # maxGBR = ( 255,190, 110)
    
   # minGBR = np.array([0, 50, 60])#(0,26,100) # 0,50,120
   # maxGBR = (15, 200, 255)
   # minGBR= (0, 0, 0)#(0,26,100) # 0,50,120
    #maxGBR= (176, 255, 255)
    #minGBR= (0, 0, 0)
    #maxGBR= (176, 255, 255)
    lowerRedHSV = (0, 80, 50)
    upperRedHSV= (15, 255, 255)
    mask2 =cv2.inRange(image, lowerRedHSV, upperRedHSV)
    
    lower_red = (170, 80, 90)
    upper_red = (180, 255, 255)
    mask1 = cv2.inRange(image, lower_red, upper_red)
    totalMask = mask1 + mask2
    """
    lowerRedHSV = (0, 80, 80)
    upperRedHSV= (20, 255, 255)
    mask1 =cv2.inRange(image, lowerRedHSV, upperRedHSV)
    
    lower_red = (170, 80, 80)
    upper_red = (180, 255, 255)
    mask2 = cv2.inRange(image, lower_red, upper_red)"""

    totalMask = mask1 + mask2
    return totalMask
    
#Removes any red noise picked up in image
def removeNoise(image):
    #kernel = np.ones((9,9),np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 3))
    
    dilations = 7
    # opening
    image = cv2.erode(image,kernel,iterations = dilations)
    image = cv2.dilate(image,kernel,iterations = dilations)

    # closing
    image = cv2.dilate(image,kernel,iterations = dilations)
    image = cv2.erode(image,kernel,iterations = dilations)
    """
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.dilate(image,kernel,iterations =15)
    image = cv2.erode(image,kernel,iterations = 2)
    image = cv2.dilate(image,kernel,iterations =15)
    image = cv2.erode(image,kernel,iterations = 2)
    image = cv2.dilate(image,kernel,iterations =15)
    image = cv2.erode(image,kernel,iterations = 2)"""
   
    return image