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

def go_to_goal(velocity_publisher, x_goal, y_goal):
    #Se recupera la posición x,y y angulo theta obtenidos gracias a poseCallback
    global x
    global y, yaw

    # Se declara el mensaje de velocidad
    velocity_message = Twist()

    while (True):
        # K_linear será un controlador Proporcional
        K_linear = 0.5 
        
        #Se calcula la distancia que hay entre la posición del robot y la deseada ( distancia 2 puntos)
        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))

        # El k_linear hace su papel de controlador proporcional
        # A mayor distancia multiplicada por K, mayor velocidad lineal
        #A menor distancia, la velocidad del robot dismimuye
        linear_speed = distance * K_linear
        
        #K_angular será otro controlador proporcional
        K_angular = 4.0
        
        #Se obtiene el angulo deseado entre la distancia actual del robot y la deseada
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        
        #A mayor angulo deseado, mayor vel_angular.
        #A menor angulo, menos vel_angular
        angular_speed = (desired_angle_goal-yaw)*K_angular

        #Se asignan las velocidades al mensaje de velocidad
        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        
        #Se publica
        velocity_publisher.publish(velocity_message)
        
        print (f"x= {x}, , y= {y}, distance to goal: {distance}")

        if (distance <0.01):
            break
    
if __name__ == '__main__':
    try:
        # Nombre del nodo usando rosnode list
        rospy.init_node('go_to_goal', anonymous=True)

        #Declaramos el topico y el publisher
        cmd_vel_topic='/turtle1/cmd_vel' # Publicara al topico cmd_vel_topic un mensaje Twist y tendrá una cola de 0 mensajes
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        #Declaramos el topico y el suscriber que escuchará la posición de la turtlesim
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        
        #Detiene el codigo 2 segungos para esperar a que se obtengan x,y,z del pose_subscriber,
        # es decir,  permite que el nodo de ROS tenga tiempo para establecer conexiones  
        time.sleep(2)
        
        #Se ejecuta la función go_to_goal
        go_to_goal(velocity_publisher,5,5)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")