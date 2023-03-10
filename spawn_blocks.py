#!/usr/bin/env python

import rospy
import rospkg
import os
import numpy as np
import random

from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import DeleteModel
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion

def GetReferenceBlockPositions():
    # positions for four reference white blocks: 4x2 array
    ref_block_xy_pos = np.array([[0.0, 0.9], [0.5, 0.9], [0.5, -0.5], [0.0, -0.5]])
    return ref_block_xy_pos

def GetBlockPositions():

    # Fixed initial positions
    block_xy_pos = np.array([[0.2, 0.05], [0.3, 0.05], [0.4, 0.05]])

    
    i=0	
    while(i==0):
    	block_xy_pos =np.random.rand(3,2)*(0.35-0.1)+0.1
    	if (abs(block_xy_pos[0,0]-block_xy_pos[1,0])<=0.062 or abs(block_xy_pos[1,0]-block_xy_pos[2,0])<=0.062 or abs(block_xy_pos[0,0]-block_xy_pos[2,0])<=0.062):
    		i=0
	else:	
		i=1
  


    print(abs(block_xy_pos[0,0]-block_xy_pos[1,0]))
    print(abs(block_xy_pos[0,0]-block_xy_pos[2,0]))
    print(abs(block_xy_pos[2,0]-block_xy_pos[1,0]))	
	

    return block_xy_pos	


if __name__ == '__main__':

    # Initialize ROS node
    rospy.init_node('lab5_spawn_blocks_node', anonymous=True)
    # Initialize ROS pack
    rospack = rospkg.RosPack()
    # Get path to block
    ur_path = rospack.get_path('lab5')

    block_ref_path = os.path.join(ur_path, 'urdf', 'block_white.urdf')
    block1_path = os.path.join(ur_path, 'urdf', 'block_red.urdf')
    block2_path = os.path.join(ur_path, 'urdf', 'block_yellow.urdf')
    block3_path = os.path.join(ur_path, 'urdf', 'block_green.urdf')
    block_paths = [block1_path, block2_path, block3_path]

    rospy.wait_for_service('gazebo/spawn_urdf_model')
    spawn = rospy.ServiceProxy('gazebo/spawn_urdf_model', SpawnModel)
    delete = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)

    # Spawn four white blocks for position calculation
    ref_block_xy_pos = GetReferenceBlockPositions()
    for i_block_ref in range(4):
        block_name = 'block_ref_' + str(i_block_ref + 1)
        pose = Pose(Point(ref_block_xy_pos[i_block_ref, 0], ref_block_xy_pos[i_block_ref, 1], 0), Quaternion(0, 0, 0, 0))
        spawn(block_name, open(block_ref_path, 'r').read(), 'block', pose, 'world')
      
    # Spawn three blocks
    block_xy_pos = GetBlockPositions()
    for i_block in range(3):
        block_name = 'block_' + str(i_block + 1)
        pose = Pose(Point(block_xy_pos[i_block, 0], block_xy_pos[i_block, 1], 0), Quaternion(0, 0, 0, 0))
        spawn(block_name, open(block_paths[i_block], 'r').read(), 'block', pose, 'world')
    
    print("\n")
    print("********** Initial Block Positions **********")
    print(block_xy_pos)
    print("*********************************************")
    print("\n")
