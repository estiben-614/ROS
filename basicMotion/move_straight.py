#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
def poseCallback(pose_message):
    # Los valores de x,y, yaw vendrán del topico /turtle1/pose y se actualizan cada vez que
    # se actualiza la posicion
    #Se almacenan de forma global
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta
    
def move(velocity_publisher, speed, distance, is_forward):
        #Se declara el mensaje de velocidad
        velocity_message = Twist()
        #Se recupera la posición actual de la tortuga que vienen gracias al poseCallback
        global x, y
        x0=x
        y0=y

        # Si la dirección es hacia adelante
        if (is_forward):
            velocity_message.linear.x =abs(speed)
        else:
        	velocity_message.linear.x =-abs(speed)

        # Se inicializa la distancia en 0
        distance_moved = 0.0
        loop_rate = rospy.Rate(10) # Se publicara 10 mensajes por segundo
        
        while True :
                rospy.loginfo("Turtlesim moves forwards")
                #El publish viene de velocity_publisher
                #Se publica la velocidad
                velocity_publisher.publish(velocity_message)

                loop_rate.sleep()
                
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                print  (distance_moved)
                print(x)
                if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break
        
        #finally, stop the robot when the distance is moved
        velocity_message.linear.x =0
        velocity_publisher.publish(velocity_message)
if __name__ == '__main__':
    try:
        rospy.init_node('move_straight', anonymous=True)

        #declare velocity publisher
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        #Detiene el codigo 2 segungos para esperar a que se obtengan x,y,z del pose_subscriber,
        # es decir,  permite que el nodo de ROS tenga tiempo para establecer conexiones  
        time.sleep(2)
        #Se ejecuta la función move 
        move(velocity_publisher, 1.0, 5, True)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
