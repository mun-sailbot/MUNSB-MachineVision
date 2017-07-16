# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 16:57:33 2016

@author: Jeffrey
"""
import math

def getDistance(detectedCircle):
    w=2*detectedCircle[2]    
    x=w**(-0.973)
    m=14339
    #b=1263.4
    dist = m*x
    print "radious is " + str(w)
    print "distance to the ball is: " + str(dist)
    return dist
    
def getDistance1(balldimator, detectedCircle):
    #TODO     
    return 0
def getDistance2balls(detectedCircle1, detectedCircle2):
    dist1 = getDistance(detectedCircle1)
    print "distance to ball 1 is: " + str(dist1)
    dist2= getDistance(detectedCircle2)
    print "distance to ball 2 is: " + str(dist2)
    
    return (dist1, dist2) 
    
#returns deg from center the ball is detected at.
# postive num is to the Right negtive is to the Left
def getDeg(detectedCircle):
    imageWith= 640
    Hyponouse = getDistance(detectedCircle)
    ballXpos =detectedCircle[0]
    print "ballXpos = " + str(ballXpos)
    offcenter = abs((imageWith/2)- ballXpos)
    deg=math.degrees(math.sin(offcenter/Hyponouse))
    if (ballXpos > (imageWith/2)):
        deg = abs(deg)
    else:
        deg = abs(deg)*(-1)
    print "deg from center = " + str(deg)
    return deg
    
#returns deg from center the ball is detected at.
# postive num is to the Right negtive is to the Lef    
def getDeg2Circs(detectedCircle1, detectedCircle2):
    imageWith= 640*2
    Hyponouse = getDistance(detectedCircle1)
    ballXpos =detectedCircle1[0]
    offcenter = abs(ballXpos - (imageWith/2) )
    deg1=math.degrees(math.sin(offcenter/Hyponouse))
    if (ballXpos > (imageWith/2)):
        deg2 = abs(deg1)
    else:
        deg2 = abs(deg1)*(-1)
    print "deg from center circle2 = " + str(deg1)
    
    Hyponouse = getDistance(detectedCircle2)
    ballXpos =detectedCircle2[0]
    offcenter = abs(ballXpos - (imageWith/2) )
    deg2=math.degrees(math.sin(offcenter/Hyponouse))
    if (ballXpos > (imageWith/2)):
        deg2 = abs(deg2)
    else:
        deg2 = abs(deg2)*(-1)
    print "deg from center  circle2= " + str(deg2)
    return (deg1, deg2 )
    
    """ w=2*detectedCircle[2]    
    x=math.log10(w)
    m=-551.68
    b=1263.4
    dist = m*x+b
    print "radious is " + str(w)
    print "distance to the ball is: " + str(dist)
    return dist"""
    
    """ w=2*detectedCircle[2]    
    y=(w/640)*100
    m=-0.0442
    b=22.533
    dist = (y - b)/m
    print "radious is " + str(w)
    print "distance to the ball is: " + str(dist)"""