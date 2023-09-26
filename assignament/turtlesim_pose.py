#!/usr/bin/python3
import rospy
from turtlesim.msg import Pose

def poseCallback(pose_message):
    # pose_message es un objeto que tiene las instancias x, y, tetha
    print("pose callback")
    print('x = %f' % pose_message.x)
    print('y = %f' % pose_message.y)
    print('yaw = %f' % pose_message.theta)

def listener():
    #Inicializa el nodo
    rospy.init_node('turtlesim_pose', anonymous=True)
    # Se suscribe al topo de pose
    rospy.Subscriber('turtle1/pose', Pose, poseCallback)
    rospy.spin()
if __name__ == '__main__':
    try:
        listener()
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")