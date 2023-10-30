#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
def poseCallback(pose_message):
    # Los valores de x,y, yaw vendrán del topico /turtle1/pose
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta
    
def move(velocity_publisher, speed, distance, is_forward):
        #Se declara el mensaje de velocidad
        velocity_message = Twist()
        global x, y
        x0=x
        y0=y

        if (is_forward):
            velocity_message.linear.x =abs(speed)
        else:
        	velocity_message.linear.x =-abs(speed)

        distance_moved = 0.0
        loop_rate = rospy.Rate(10) # Se publicaran 10 mensajes por segundo
        
        while True :
                rospy.loginfo("Turtlesim moves forwards")
                #Se publica la velocidad
                velocity_publisher.publish(velocity_message)

                loop_rate.sleep()
                
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                print  (f"Distancia recorrida : {distance_moved}")
                print(f"Posición turtlesim : {x}")
                if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break
        
        #Freno de la turtulesim cuando llega a la distancia establecida 
        velocity_message.linear.x =0
        velocity_publisher.publish(velocity_message)
if __name__ == '__main__':
    try:
        # Nombre del nodo usando rosnode list
        rospy.init_node('move_straight', anonymous=True)

        #Declaramos el topico y el publisher
        cmd_vel_topic='/turtle1/cmd_vel' # Publicara al topico cmd_vel_topic un mensaje Twist y tendrá una cola de 0 mensajes
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        #Declaramos el topico y el suscriber que escuchará la posición de la turtlesim
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        
        #Detiene el codigo 2 segungos para esperar a que se obtengan x,y,z del pose_subscriber,
        # es decir,  permite que el nodo de ROS tenga tiempo para establecer conexiones  
        time.sleep(2)
        
        #Se ejecuta la función move 
        move(velocity_publisher, 10, 5, True)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
