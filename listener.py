#!/usr/bin/python3

import rospy
from std_msgs.msg import String

def chatter_callback(message):
    rospy.loginfo(rospy.get_caller_id() +'I heard %s ', message.data)
def listener():
    # inicializa en nodo listener 
    rospy.init_node('listener', anonymous=True)
    # Se suscribe al topico, y cada vez que recibe
    # un mensaje de tipo String ejecuta el callbacl
    rospy.Subscriber('chatter',String, chatter_callback)  
    
    # Permite que esté escuchando eventos
    rospy.spin()
    

if __name__=='__main__':
    listener()