#!/usr/bin/env python3

# drive_control_node.py
# Subscriber node - subscribes to /drive/cmd_vel and sends commands to RC motor
# Responsible for direct motor-control of the rover

import rospy

from RoverEngine import RoverEngine
from geometry_msgs.msg import Twist

# global engine control
engine = RoverEngine()

def cmd_vel_callback(twist):
    """ The callback for the topic /drive/cmd_vel """
    thrust = twist.linear.x
    yaw = twist.angular.z
    drive_motors(thrust, yaw)


def drive_motors(thrust, yaw):
    """Send motor commands to drive rover

    Args:
        thrust: A unit scalar [-1.0, 1.0] where 0.0 is zero thrust (stopped) and 1.0 is full-speed forward (not recommended)
        and -1.0 is full reverse thrust (not recommended)

        yaw: A unit scalar [-1.0, 1.0] where 0.0 is no yaw (straight steering), 1.0 is a full-right turn, and -1.0 is a full left turn.

    Note: Values will be clamped to the range [-1.0, 1.0] is out of bounds
    """
    thrust_clamped = max(min(thrust, 1.0), -1.0)
    yaw_clamped = max(min(yaw, 1.0), -1.0)
    engine.set_input(thrust_clamped, yaw_clamped)


def run_node():
    """ Node main function """

    # ros node setup
    rospy.init_node('drive_control_node', anonymous=False)
    rospy.Subscriber('/drive/cmd_vel', Twist, cmd_vel_callback)

    try:
        rospy.spin()
    except:
        engine.shut_down()


if __name__ == '__main__':
    run_node()
