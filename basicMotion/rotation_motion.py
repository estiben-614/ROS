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

def rotate (velocity_publisher, angular_speed_degree, relative_angle_degree, clockwise):
    #Declaramos el mensaje de velocidad
    velocity_message = Twist()

    #Calculamos la velocidad angular pasando de grados a radianes
    angular_speed=math.radians(abs(angular_speed_degree))

    #Dirección de rotación
    if (clockwise):
        #Recordar que velocity_message es de la forma : { linear : {x, y,z} , angular: {x,y,z}}
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed)

    #Se inicializa el angulo 
    angle_moved = 0.0
    
    #Se publicaran 10 mensajes de velocidad por segundo
    loop_rate = rospy.Rate(10)     
    
    #Se define el topico y se publica el mensaje
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    # Obtiene el tiempo en segundos en el que inicia la simulación
    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        #Mientras se cumpla, envia mensajes de velocidad a la turtlesim
        velocity_publisher.publish(velocity_message)

        # Obtiene el tiempo de cada iteración
        t1 = rospy.Time.now().to_sec()
        
        #El angulo actual será la diferencia de tiempo por la velocidad angular
        # Digamos, la turtlesim se mueve pi/2 cada segundo ( esa es la vel_angular)
        # A los dos segundos giró Pi (180)
        current_angle_degree = (t1-t0)*angular_speed_degree
        print(f"Angulo actual : {current_angle_degree}")
        # Hace la pausa para mantener la frecuencia de 10hz por segundo
        loop_rate.sleep()

        # Si el angulo actual > angulo indicado, rompe el ciclo
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

    #Frena el robot
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)
    
if __name__ == '__main__':
    try:
        # Nombre del nodo usando rosnode list
        rospy.init_node('rotation', anonymous=True)

        #Declaramos el topico y el publisher
        cmd_vel_topic='/turtle1/cmd_vel' # Publicara al topico cmd_vel_topic un mensaje Twist y tendrá una cola de 0 mensajes
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        #Declaramos el topico y el suscriber que escuchará la posición de la turtlesim
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        
        #Detiene el codigo 2 segungos para esperar a que se obtengan x,y,z del pose_subscriber,
        # es decir,  permite que el nodo de ROS tenga tiempo para establecer conexiones  
        time.sleep(2)
        
        #Se ejecuta la función rotate -> True para dirección de las agujas del reloj,
        # false para ir en contra de las agujas 
        rotate(velocity_publisher,20,180,True)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")