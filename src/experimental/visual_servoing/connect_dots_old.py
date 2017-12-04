import rospy
import roslib

#import cv;
import cv2;
import cv_bridge

import numpy
import math
import os
import sys
import string
import time
import random
import tf
from sensor_msgs.msg import Image
import baxter_interface
from moveit_commander import conversions
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Header
import std_srvs.srv
from baxter_core_msgs.srv import SolvePositionIK, SolvePositionIKRequest


''' GLOBALS '''
cv_image = None #cv2.createImage((self.width, self.height), 8, 3)
circle_image = None
key = 0
img_state = 0
key_state = 0
hough_accumulator = 100
hough_min_radius  = 0
hough_max_radius  = 0
contrast_lo  = 185
contrast_hi  = 255

''' REGION FUNCTIONS '''

# reset all cameras (incase cameras fail to be recognised on boot)
def reset_cameras():
    reset_srv = rospy.ServiceProxy('cameras/reset', std_srvs.srv.Empty)
    rospy.wait_for_service('cameras/reset', timeout=10)
    reset_srv()

# open a camera and set camera parameters
def open_camera(camera, x_res, y_res):
    if camera == "left":
        cam = baxter_interface.camera.CameraController("left_hand_camera")
    elif camera == "right":
        cam = baxter_interface.camera.CameraController("right_hand_camera")
    elif camera == "head":
        cam = baxter_interface.camera.CameraController("head_camera")
    else:
        sys.exit("ERROR - open_camera - Invalid camera")

    # close camera
    # cam.close()

    # set camera parameters
    cam.resolution          = (int(x_res), int(y_res))
    cam.exposure            = -1             # range, 0-100 auto = -1
    cam.gain                = -1             # range, 0-79 auto = -1
    cam.white_balance_blue  = -1             # range 0-4095, auto = -1
    cam.white_balance_green = -1             # range 0-4095, auto = -1
    cam.white_balance_red   = -1             # range 0-4095, auto = -1

    # open camera
    cam.open()

# close a camera
def close_camera(camera):
    if camera == "left":
        cam = baxter_interface.camera.CameraController("left_hand_camera")
    elif camera == "right":
        cam = baxter_interface.camera.CameraController("right_hand_camera")
    elif camera == "head":
        cam = baxter_interface.camera.CameraController("head_camera")
    else:
        sys.exit("ERROR - close_camera - Invalid camera")

    # set camera parameters to automatic
    cam.exposure            = -1             # range, 0-100 auto = -1
    cam.gain                = -1             # range, 0-79 auto = -1
    cam.white_balance_blue  = -1             # range 0-4095, auto = -1
    cam.white_balance_green = -1             # range 0-4095, auto = -1
    cam.white_balance_red   = -1             # range 0-4095, auto = -1

    # close camera
    cam.close()

# camera call back function
def camera_callback(data, camera_name):
    global cv_image
    global img_state
    global contrast_hi
    global contrast_lo
    # Convert image from a ROS image message to a CV image
    try:
        cv_image = cv_bridge.CvBridge().imgmsg_to_cv2(data, "bgr8")

        if img_state == 1:
            gray_image = gray_it(cv_image)
            cv2.imshow('Baxter', gray_image)
        if img_state == 2:
            gray_image = gray_it(cv_image)
            _,thresh_image = cv2.threshold(gray_image,contrast_lo,contrast_hi,0)
            cv2.imshow('Baxter', thresh_image)
        elif img_state == 9:
    	    circle_image = hough_it(cv_image)
            cv2.imshow('Baxter', circle_image)
        elif img_state == 0 :
            cv2.imshow('Baxter', cv_image)



    except cv_bridge.CvBridgeError, e:
        print e

    # 3ms wait
    global key
    key = cv2.waitKey(3)

# left camera call back function
def left_camera_callback(data):
    camera_callback(data, "Left Hand Camera")

# right camera call back function
def right_camera_callback(data):
    camera_callback(data, "Right Hand Camera")

# head camera call back function
def head_camera_callback(data):
    camera_callback(data, "Head Camera")

# create subscriber to the required camera
def subscribe_to_camera(camera):
    if camera == "left":
        callback = left_camera_callback
        camera_str = "/cameras/left_hand_camera/image"
    elif camera == "right":
        callback = right_camera_callback
        camera_str = "/cameras/right_hand_camera/image"
    elif camera == "head":
        callback = head_camera_callback
        camera_str = "/cameras/head_camera/image"
    else:
        sys.exit("ERROR - subscribe_to_camera - Invalid camera")

    camera_sub = rospy.Subscriber(camera_str, Image, callback)



def create_blank(width, height, depth):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = numpy.zeros((height, width, depth), numpy.uint8)
    return image

def cv2array(im):
        depth2dtype = {cv2.CV_8U: 'uint8', # need to define this map properly, don't know constants
                       cv2.CV_8S: 'int8',
                       cv2.CV_16U: 'uint16',
                       cv2.CV_16S: 'int16',
                       cv2.CV_32S: 'int32',
                       cv2.CV_32F: 'float32',
                       cv2.CV_64F: 'float64'}
  
       # arrdtype=im.depth

        a = numpy.fromstring(im.tostring(), dtype = depth2dtype[0], count = 960 * 600 * 1) 		#im.width * im.height * im.nChannels)
        a.shape = (960, 600, 1)    #(im.height, im.width, im.nChannels)

        return a


def gray_it(cv_image) :

    if cv_image is None:
        return None
    gray_image = create_blank(960, 600, 1)
    #cv2.cvtColor(cv_image, gray_image, cv2.COLOR_BGR2GRAY)
    cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY, gray_image)
    # create gray scale array of balls
    
    return gray_image

#def thresh_it(cv_image) :

#    for i in cv_image :
 #       for j in cv_image[i] :
  #          if()
   #             cv_image[i][j]


# Use Hough circles to find ball centres (Only works with round objects)
def hough_it(cv_image):
    # create gray scale image of balls
    #gray_image = cv2.create_image((960, 600), 8, 1)
    #global cv_image
    if cv_image is None:
        return None
    #gray_image = create_blank(960, 600, 1)
        #cv2.cvtColor(cv_image, gray_image, cv2.COLOR_BGR2GRAY)
    #cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY, gray_image)


    # create gray scale array of balls
    #gray_array = cv2array(gray_image)

    # find Hough circles

    gray_image = gray_it(cv_image)
    blur_image = cv2.medianBlur(gray_image,5)
    #blur_array = cv2array(gray_image)

    global hough_accumulator
    global hough_min_radius
    global hough_max_radius
    circles = cv2.HoughCircles(blur_image, cv2.HOUGH_GRADIENT, 1, 20, param1=50,  \
              param2=hough_accumulator, minRadius=hough_min_radius,       \
              maxRadius=hough_max_radius)

    # Check for at least one ball found
    if circles is None:
        # display no balls found message on head display
        # splash_screen("no balls", "found")
        # no point in continuing so exit with error message
        #sys.exit("ERROR - hough_it - No golf balls found")
	    return cv_image

    circles = numpy.uint16(numpy.around(circles))

    ball_data = {}
    n_balls   = 0

    circle_array = numpy.asarray(cv_image)

    # check if golf ball is in ball tray
    for i in circles[0,:]:
        cv2.circle(circle_array, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle in green
        cv2.circle(circle_array, (i[0], i[1]), 2, (0, 255, 0), 3)

        ball_data[n_balls]  = (i[0], i[1], i[2])
        n_balls            += 1

    #global circle_image 
    circle_image = circle_array #cv2.fromArray(circle_array)

    #print "here"
    #cv2.imshow("Hough Circle", circle_image)

    #return None
    # 3ms wait
    #cv2.waitKey(3)

    # Check for at least one ball found
    #if n_balls == 0:                    # no balls found
        # less than 12 balls found, no point in continuing, exit with error message
    #    sys.exit("ERROR - hough_it - No golf balls found")

    return circle_image

''' END REGION '''



limb = 'right'
width = 960
height = 600

# initialise ros node
rospy.init_node("connect_dots", anonymous = True)

# Enable the actuators
baxter_interface.RobotEnable().enable()

# directory used to save analysis images
image_directory = os.getenv("HOME") + "/Dots/"

# reset cameras
reset_cameras()

# close all cameras
#close_camera("left")
#close_camera("right")
#close_camera("head")

# open required camera
open_camera(limb, width, height)

# subscribe to required camera
subscribe_to_camera(limb)

while True:
    #time.sleep(0.1)
    #if cv_image is not None:
    #    cv2.imshow('Baxter', cv_image)
    #key = cv2.waitKey(3)

    if key == 27:
        break


    
    if key == ord('j'):
        hough_min_radius -= 5
        print "Min rad: ", hough_min_radius
    if key == ord('k'):
        hough_min_radius += 5
        print "Min rad: ", hough_min_radius
    if key == ord('u'):
        hough_max_radius -= 5
        print "Max rad: " , hough_max_radius
    if key == ord('i'):
        hough_max_radius += 5
        print "Max rad: ", hough_max_radius
    if key == ord('n'):
        hough_accumulator -= 10;
        if hough_accumulator < 0:
            hough_accumulator = 0
        print "HA : ", hough_accumulator
    if key == ord('m'):
        hough_accumulator += 10
        if hough_accumulator > 255:
            hough_accumulator = 255
        print "HA : ", hough_accumulator
            


    if key == 48:
        img_state = 0
        print img_state
    elif key == 49:
        img_state = 1
        print img_state
    elif key == 50:
        img_state = 2
        print img_state
    elif key == 51:
        img_state = 3
        print img_state
    elif key == 52:
        img_state = 4
        print img_state
    elif key == 53:
        img_state = 5
        print img_state
    elif key == 54:
        img_state = 6
        print img_state
    elif key == 55:
        img_state = 7
        print img_state
    elif key == 56:
        img_state = 8
        print img_state
    elif key == 57:
        img_state = 9
        print img_state

    key = -1

    #if cv_image is not None:
     #   print cv_image
        

