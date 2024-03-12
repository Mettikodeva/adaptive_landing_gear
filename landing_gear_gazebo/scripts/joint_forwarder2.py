import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from controller_manager_msgs.srv import ListControllersRequest, ListControllers, ListControllersResponse
from controller_manager_msgs.msg import ControllerState


ground_link_pub = rospy.Publisher("/landing_gear/ground_link_controller/command", Float64, queue_size=10)
def joint_callback(data:JointState):    
    ground_link_pub.publish(-data.position[0])  


if __name__ == "__main__":
    rospy.init_node("joint_forwarder")
    
    joint_state_sub = rospy.Subscriber("/joint_states", JointState, joint_callback)
    r = rospy.Rate(5)
    rospy.spin()

    