#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2

x, y, theta = 0.0, 0.0, 0.0  # initialize Cartesian coordinate

# update odometry
def newOdom(msg):
    global x, y, theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    _, _, theta = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/robot_base_velocity_controller/odom", Odometry, newOdom)
pub = rospy.Publisher("/robot_base_velocity_controller/cmd_vel", Twist, queue_size=1)
r = rospy.Rate(4)

speed = Twist()
goal = Point()
goal.x = 7
goal.y = 8

while not rospy.is_shutdown():
    inc_x = goal.x - x
    inc_y = goal.y - y
    angle_to_goal = atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:  # use a small threshold for angle error
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    else:
        speed.linear.x = 0.5
        speed.angular.z = 0.0

    
    pub.publish(speed)
    r.sleep()


# import rospy
# from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Twist, Point
# from tf.transformations import euler_from_quaternion
# from math import atan2, sqrt

# # Callback function to update the robot's position
# def odom_callback(msg):
#     global x, y, theta
#     x = msg.pose.pose.position.x
#     y = msg.pose.pose.position.y
#     rot_q = msg.pose.pose.orientation
#     (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

# # Initialize the ROS node
# rospy.init_node('move_to_point')

# # Subscribe to the robot's odometry topic
# rospy.Subscriber('/robot_base_velocity_controller/odom', Odometry, odom_callback)

# # Set the publisher to the robot's velocity control topic
# velocity_publisher = rospy.Publisher('/robot_base_velocity_controller/cmd_vel', Twist, queue_size=10)

# # Set the rate of the ROS loop to update the velocity commands
# rate = rospy.Rate(10)

# # Define the goal point
# goal = Point()
# goal.x = 0
# goal.y = 0

# # Define the desired distance threshold from the goal
# distance_threshold = 0.1

# # Main ROS loop to calculate and publish the velocity commands
# while not rospy.is_shutdown():
#     # Calculate the distance from the robot to the goal
#     distance_to_goal = sqrt((goal.x - x)**2 + (goal.y - y)**2)

#     # If the robot has not reached the goal yet
#     if distance_to_goal > distance_threshold:
#         # Calculate the angle between the robot and the goal
#         angle_to_goal = atan2(goal.y - y, goal.x - x)

#         # Calculate the difference between the robot's current orientation and the goal angle
#         angle_diff = angle_to_goal - theta

#         # Normalize the angle difference to between -pi and pi
#         if angle_diff > 3.141592653589793:
#             angle_diff -= 2 * 3.141592653589793
#         elif angle_diff < -3.141592653589793:
#             angle_diff += 2 * 3.141592653589793

#         # Calculate the linear velocity command
#         linear_velocity = min(distance_to_goal, 0.5)

#         # Calculate the angular velocity command
#         angular_velocity = 2.0 * angle_diff

#         # Publish the velocity commands to the robot's velocity control topic
#         velocity_command = Twist()
#         velocity_command.linear.x = linear_velocity
#         velocity_command.angular.z = angular_velocity
#         velocity_publisher.publish(velocity_command)

#     # If the robot has reached the goal
#     else:
#         # Stop the robot by publishing a zero velocity command
#         velocity_command = Twist()
#         velocity_publisher.publish(velocity_command)

#     # Sleep to maintain the ROS rate
#     rate.sleep()