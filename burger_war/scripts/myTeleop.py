#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios


from geometry_msgs.msg import Twist

#from std_msgs.msg import String
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import cv2


msg = """

Control TurtleBot3 using keyboard
---------------------------
Moving around:
        k
   h         l
        j

CTRL-C to quit
Please input key
"""

class MyTeleop():
    def __init__(self, bot_name):
        # bot name 
        self.name = bot_name
        # velocity publisher
        self.vel_pub = rospy.Publisher('/red_bot/cmd_vel', Twist,queue_size=1)

    def getKey(self):
        if os.name == 'nt':
            return msvcrt.getch()

        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key


    def calcTwist(self):

        keyValue = ''
        while(1):
            if not keyValue:
                keyValue = self.getKey()
            else:
                break

        if keyValue == 'k':
            x = 0.1
            th = 0
        elif keyValue == 'j':
            x = -0.1
            th = 0
        elif keyValue == 'h':
            x = 0
            th = 0.5
        elif keyValue == 'l':
            x = 0
            th = -0.5
        else:
            x = 0
            th = 0
        twist = Twist()
        twist.linear.x = x; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
        return twist

        if os.name != 'nt':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def strategy(self):
        r = rospy.Rate(0.5) # change speed 1fps

        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0

        while not rospy.is_shutdown():
            twist = self.calcTwist()
            #print(twist)
            self.vel_pub.publish(twist)
            r.sleep()
            twist = Twist()
            self.vel_pub.publish(twist)


if __name__ == '__main__':
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('myTeleop')
    bot = MyTeleop('myTeleop')
    print msg
    bot.strategy()

