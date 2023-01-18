#!/usr/bin/env python

import cv2
import numpy as np

def FindBlockByColor(image, color):
    # Convert the image into the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # lower = (hmin, smin, vmin)
    # upper = (hmax, smax, vmax)
    lower = (0,0,0)
    upper = (179,255,255)

    ##### Your Code Starts Here #####
    
    # ToDo: find and define lower and upper bounds of the target color
    # You can use either string or integer type for the 'color' input

#Checks the color and assigns the respective hmin, smin, and vmin values for it
    if (color == "WHITE"):
        lower = (0,0,220)
        upper = (0,0,255)
    elif (color == "RED"):
        lower=(0,100,50)
        upper=(27,255,255)
    elif (color == "YELLOW"):
        lower=(25,150,50)
        upper=(35,255,255)
    elif (color == "GREEN"):
        lower=(35,100,45)
        upper=(100,255,255)
	
	##### Your Code Ends Here #####
    
    # Find mask image
    mask_image = cv2.inRange(hsv_image, lower, upper)
    
    # Remove comment signs to show the masked image result
    '''
    cv2.namedWindow("Masked Image")
    cv2.imshow("Masked Image", mask_image)
    cv2.waitKey(0)
    '''

    # Output: a masked image for showing the position of the certain color block

    return mask_image

def FindBlockCenter(mask_image):
    _image = cv2.bitwise_not(mask_image)
    params = cv2.SimpleBlobDetector_Params()
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs
    keypoints = detector.detect(_image)
    _image = cv2.bitwise_not(_image)

    block_centers = []

    ##### Your Code Starts Here #####
    
    # ToDo: find blob centers in the image coordinates 
    #  
    # Output: store the results in 'block_centers'
    # 
    # Hint: only 'keypoints' results are needed
    # 
    # 'block_centers' array has a size of (n x 2), where n is the number of blobs found

    for x in keypoints:
	    block_centers.append([x.pt[0], x.pt[1]])
    num_blobs = len(keypoints)

    #print(block_centers)
    #print(num_blobs)
	##### Your Code Ends Here #####


    # Remove comment signs to show the image with 'block_centers' result added
    
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(_image, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    for i in range(num_blobs):   
        cv2.circle(im_with_keypoints, (int(keypoints[i].pt[0]), int(keypoints[i].pt[1])), 2, (0, 0, 255), -1)

    # Show keypoints
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.waitKey(0)
    

    return block_centers


def PixelToWorld(target_block_center_pixel, image):
    # ToDo: function that converts the detected center pixel position in image coord 
    #       to (x, y) coord in world frame
    # 
    # Output: 'block_xy': x, y coordinates in world frame of a block, as a list
    #
    # Use the four white blocks as reference points to calculate coordinates

    block_xw = 0.0
    block_yw = 0.0
    block_xy = [block_xw, block_yw]

    ##### Your Code Starts Here #####

#Define the ranges for the world as well as the x and y coordinates for the target block
    x_range_world = 0.5
    y_range_world = 1.4
    x_img = target_block_center_pixel[0]
    y_img = target_block_center_pixel[1]

#Find and assign the locations of the governing white blocks in the corner
    white_center = FindBlockCenter(FindBlockByColor(image, "WHITE"))
    WBlock_bottom_left = white_center[1]
    WBlock_top_left = white_center[3]
    WBlock_bottom_right = white_center[0]
    
  
#Find the range of the white blocks
    x_range_img = WBlock_bottom_right[0] - WBlock_bottom_left[0]
    y_range_img = WBlock_bottom_left[1] - WBlock_top_left[1] 

#Divide the World range by the Pixel range in order to find a conversion ratio. Note that the X of the world is the Y of the pixel and etc.
    xRatio = x_range_world/y_range_img
    yRatio = y_range_world/x_range_img

#Calculate the offset from the world frame to the pixel frame and apply it to our target block
    world_frame_offset_y = 0.9/yRatio + WBlock_bottom_left[0]
    world_frame_offset_x = 0.5/xRatio + WBlock_top_left[1]
    target_x_img = (world_frame_offset_x - y_img)
    target_y_img = (world_frame_offset_y - x_img)

#Convert the pixel frame into the world frame
    target_x_world = target_x_img*yRatio
    target_y_world = target_y_img*xRatio
    block_xy = [target_x_world, target_y_world]

	##### Your Code Ends Here #####

    return block_xy


def FindColorBlockWorldCoord(image, color):
    # (Optional):
    # You may define the following function integrating all functions above 
    # for easier usage in 'lab5_main.py' later

    block_xy = [0.0, 0.0]

    ##### Your Code Starts Here #####
    image_mask = FindBlockByColor(image, color)
    block_centers = FindBlockCenter(image_mask)
    block_xy = PixelToWorld(block_centers[0], image)
	
	##### Your Code Ends Here #####


    return block_xy
    

# The above functions can be tested in the '__main__' function below: 
# Steps:
# 1) Make this script executable
# 2) Run 'python find_block_pos.py' in terminal

if __name__ == '__main__':
    image = cv2.imread("../img_test_1.png")
    # Your test code below
    print("Green: " + str(FindColorBlockWorldCoord(image, "GREEN")))
    print("Yellow: " + str(FindColorBlockWorldCoord(image, "YELLOW")))
    print("Red: " + str(FindColorBlockWorldCoord(image, "RED")))
