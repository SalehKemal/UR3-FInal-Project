#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm

def Get_MS():
	# Initialize return values of M and S
	M = np.eye(4)
	S = np.zeros((6,6))

	##### Your Code Starts Here #####
	# Fill in scripts from lab3 here
	Start = np.matrix([[1, 0, 0, -.15], [0, 1, 0, .15], [0, 0, 1, .162], [0, 0 ,0, 1]])
	M = np.matmul(M, Start)
	M = np.matmul(M, DHtoA(0, 0, -PI/2, 0))
	M = np.matmul(M, DHtoA(0, 0, 0, .244))
	M = np.matmul(M, DHtoA(0, 0, 0, .213))
	M = np.matmul(M, DHtoA(-PI/2, .083, -PI/2, 0))
	M = np.matmul(M, DHtoA(0, .083, PI/2, 0))
	M = np.matmul(M, DHtoA(0, .141, 0, .0535))

	
	##### Your Code Ends Here #####

	return M, S


def DHtoA(theta, d, alpha, a):
	# =================== Your code starts here ====================#
	# Write a script for returning the transformation matrix for the link from the DH parameters
	
	A = np.matrix([[np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
		       [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
		       [0, np.sin(alpha), np.cos(alpha), d],
		       [0, 0, 0, 1]])
	
	# ==============================================================#	
	return A


def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):
	# Initialize the return_value 
	return_value = [None, None, None, None, None, None]

	print("Foward kinematics calculated:\n")

	##### Your Code Starts Here #####
	# Fill in scripts from lab3 here
	PI = np.pi
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	T = np.eye(4)

	T = np.matmul(T, DHtoA(3/4*PI, 0, 0, 0.15*np.sqrt(2)))
	T = np.matmul(T, DHtoA(theta[0]-3/4*PI, 0.162, -PI/2, 0))
	T = np.matmul(T, DHtoA(theta[1], 0.027, 0, .244))
	T = np.matmul(T, DHtoA(theta[2], 0, 0, .213))
	T = np.matmul(T, DHtoA(theta[3]-PI/2, .083, -PI/2, 0))
	T = np.matmul(T, DHtoA(theta[4], .083, PI/2, 0))
	T = np.matmul(T, DHtoA(theta[5], .141, 0, .0535))

	##### Your Code Ends Here #####
	print(str(T) + "\n")

	return_value[0] = theta1 + np.pi
	return_value[1] = theta2
	return_value[2] = theta3
	return_value[3] = theta4 - (0.5*np.pi)
	return_value[4] = theta5
	return_value[5] = theta6

	if T[2, 3] < 0:
		print("Calculated Z coordinate is less than 0. The robot joint angles will be set as 0.")
		return_value = np.array([0, 0, 0, 0, 0, 0])

	return return_value


def inverse_kinematics(xWgrip, yWgrip, zWgrip, yaw_WgripDegree):
	return_value = np.array([0, 0, 0, 0, 0, 0])

	##### Your Code Starts Here #####
	L = [0, 0.152, 0.120, 0.244, 0.093, 0.213, 0.083, 0.083, 0.082, 0.0535, 0.052]

	# Step 1: find gripper position relative to the base of UR3,
	# and set theta_5 equal to -pi/2
	xgrip = xWgrip + 0.15
	ygrip = yWgrip - 0.15
	zgrip = zWgrip - 0.01
	theta_5 = -1*np.pi/2

	# Step 2: find x_cen, y_cen, z_cen
	x_cen = xgrip - L[9]*np.cos(np.deg2rad(yaw_WgripDegree))
	y_cen = ygrip - L[9]*np.sin(np.deg2rad(yaw_WgripDegree))
	z_cen = zgrip


	# Step 3: find theta_1
	d = 0.027 + L[6]
	theta_1 = np.arctan2(y_cen, x_cen) - np.arcsin(d/np.sqrt(x_cen**2 + y_cen**2))

	# Step 4: find theta_6 
	theta_6 = np.deg2rad((90 - yaw_WgripDegree + np.rad2deg(theta_1)))

	# Step 5: find x3_end, y3_end, z3_end
	x3_end = x_cen - L[7]*np.cos(theta_1) + d*np.sin(theta_1)
	y3_end = y_cen - L[7]*np.sin(theta_1) -d*np.cos(theta_1)
	z3_end = z_cen + L[8] + L[10]

	# Step 6: find theta_2, theta_3, theta_4
	r = np.sqrt((x3_end**2) + (y3_end**2))
	h = z3_end - L[1]

	theta_3 = np.arccos((r**2 + h**2 - L[3]**2 - L[5]**2)/(2*L[3]*L[5]))
	theta_2 = (np.arctan(h/r) + np.arccos((L[5]**2 - L[3]**2 - r**2 - h**2)/(-2*L[3]*np.sqrt(r**2 + h**2))))*-1
	theta_4 = -theta_3 - theta_2

	##### Your Code Ends Here #####

	# print theta values (in degree) calculated from inverse kinematics
	
	print("Joint angles: ")
	print(str(theta_1*180/np.pi) + " " + str(theta_2*180/np.pi) + " " + \
			str(theta_3*180/np.pi) + " " + str(theta_4*180/np.pi) + " " + \
			str(theta_5*180/np.pi) + " " + str(theta_6*180/np.pi))

	# obtain return_value from forward kinematics function
	return_value = lab_fk(theta_1, theta_2, theta_3, theta_4, theta_5, theta_6)

	return return_value
