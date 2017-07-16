# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 21:04:06 2016

@author: Jeffrey
"""
def findAvarages(circleList):
    #circleList
    if (len(circleList)<1):
        return (0,0,0)
    else:
        #print "______kmean is runing________"
        iterations = 20
        ##TODO:  genreate a ranom number
        center1 = (100 ,100, 30)
        center2 =  (300, 300, 30)
        count1 = 0 
        count2 = 0
        circleNum=0
        #print "center1= " + str(center1[0])
        #print "center1= " + str(center1[1])
        for i in range(0, iterations):
            #print "count= " + str(i)
            if(count1+count2 == 0):  #first pass
                circleNum=0
                tempCircle=circleList[0]
                center1 = (tempCircle[0] ,tempCircle[1], tempCircle[2])
                center2= (tempCircle[0], tempCircle[1], tempCircle[2])
            else:
                circleNum= circleNum+1
            for i in range(0, len(circleList)):
                tempCircle=circleList[i]
                #print "circleList= " +str(circleList)
                #print "center1= " + str(center1[0])
                #print "center1= " + str(center1[1])
                tempTuple = (0 ,0, 0)
                #print "tempTuple= " + str(tempTuple)
                tempTuple = (tempCircle[0], tempCircle[1])
                #print "tempTuple= " + str(tempTuple)
                if(nearestPoint(tempTuple, center1, center2)== center1):
                    if count1 ==0:
                        center1 =  ((center1[0]*count1 + tempCircle[0])/(count1+1), (center1[1]*count1 + tempCircle[1])/(count1+1), (center1[2]*count1 + tempCircle[2])/(count1+1))
                    else:
                        center1 = (tempCircle[0], tempCircle[1], tempCircle[2])
                    #center1 =  (C1Center.Lon*count1 + GPSNode.GetGPSValLon())/(count1+1)
                    count1 = count1+1
                else:
                    if count2 ==0:
                        center2 =  ((center2[0]*count2 + tempCircle[0])/(count2+1), (center2[1]*count2 + tempCircle[1])/(count2+1), (center2[2]*count2 + tempCircle[2])/(count2+1))
                    else:
                        center2 = (tempCircle[0], tempCircle[1], tempCircle[2])
                    #C2Center.Lat =  (C2Center.Lat*count2 + GPSNode.GetGPSValLat())/(count2+1)
                    #C2Center.Lon =  (C2Center.Lon*count2 + GPSNode.GetGPSValLon())/(count2+1)
                    count2 =count2+1
        #print "center1: " + center1 + " & Center2: " + center2 
        kCenter = (center1, center2)
        return kCenter #(center1, center2)
     
def nearestPoint(point, point1, point2):
    #print "center= " + str(point[0]) + " , " +str(point[1])
    #print "center1= " + str(point1[0]) + " , " +str(point1[1])
    #print "center2= " + str(point2[0]) + " , " +str(point2[1])
    #print "nearestPoint running"
    LW=(abs(point[0]-point1[0]), abs(point[1]-point1[1]))
    #print "LW found"
    distToPoint1 = ((LW[0]**2)+(LW[1]**2))**(0.5)
    #print "distToPoint1 found"    
    LW=(abs(point[0]-point2[0]), abs(point[1]-point2[1]))
    distToPoint2 = ((LW[0]**2)+(LW[1]**2))**(0.5)
    #print "distToPoint1 found" +str(distToPoint2)
    if(distToPoint1 > distToPoint2):
        return point2
    else:
        return point1

def getDistBetween(point1, point2):
    
    LW=(abs(point1[0]-point2[0]), abs(point1[1]-point2[1]))
    dist = ((LW[0]**2)+(LW[1]**2))**(0.5)
    print "dist between kmean = " +str(dist)
    return dist
    
