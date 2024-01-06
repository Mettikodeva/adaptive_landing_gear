import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from math import radians, degrees, pi
from random import randint

pub_link2_leg1 = rospy.Publisher("/landing_gear/base_leg_link2_joint_position_controller/command", Float64, queue_size=10)
pub_link2_leg2 = rospy.Publisher("/landing_gear/base_leg_2_link2_joint_position_controller/command", Float64, queue_size=10)
pub_link2_leg3 = rospy.Publisher("/landing_gear/base_leg_3_link2_joint_position_controller/command", Float64, queue_size=10)
pub_leg1 = rospy.Publisher("/landing_gear/base_leg_joint_position_controller/command", Float64, queue_size=10)
pub_leg2 = rospy.Publisher("/landing_gear/base_leg_2_joint_position_controller/command", Float64, queue_size=10)
pub_leg3 = rospy.Publisher("/landing_gear/base_leg_3_joint_position_controller/command", Float64, queue_size=10)
pos = JointState()

def update_joint_link2(data:JointState):
    global pos
    pos = data.position
    l1 = Float64(pos[2])
    l2 = Float64(pos[0])
    l3 = Float64(pos[1])
    pub_link2_leg1.publish(l1)
    pub_link2_leg2.publish(l2)
    pub_link2_leg3.publish(l3)


if __name__ == "__main__":
    rospy.init_node("demo_landing_gear")
    sub = rospy.Subscriber("/landing_gear/joint_states", JointState, update_joint_link2)
    start = rospy.Time().now().secs
    r = rospy.Rate(0.5)
    rospy.loginfo("mulai")
    while rospy.Time().now().secs - start < 30:
        pub_leg1.publish(Float64(-randint(0,31415)/10000))
        pub_leg2.publish(Float64(-randint(0,31415)/10000))
        pub_leg3.publish(Float64(-randint(0,31415)/10000))
        r.sleep()
    rospy.loginfo("end")
    rospy.signal_shutdown("selesai demo")
    