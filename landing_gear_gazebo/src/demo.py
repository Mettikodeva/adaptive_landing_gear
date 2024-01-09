import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from math import radians, degrees, pi
from random import randint



def update_joint_link2(data:JointState):
    rospy.loginfo(f"{data.name}")
    print("callback")
    pos = data.position
    l1 = Float64(pos[2])
    l2 = Float64(pos[0])
    l3 = Float64(pos[1])
    pub_link2_leg1.publish(l1)
    pub_link2_leg2.publish(l2)
    pub_link2_leg3.publish(l3)


if __name__ == "__main__":
    rospy.init_node("demo_landing_gear")
    pub_leg1 = rospy.Publisher("/landing_gear/base_leg_1_joint_position_controller/command", Float64, queue_size=10)
    pub_leg2 = rospy.Publisher("/landing_gear/base_leg_2_joint_position_controller/command", Float64, queue_size=10)
    pub_leg3 = rospy.Publisher("/landing_gear/base_leg_3_joint_position_controller/command", Float64, queue_size=10)
    pub_link2_leg1 = rospy.Publisher("/landing_gear/base_leg_1_link2_joint_position_controller/command", Float64, queue_size=10)
    pub_link2_leg2 = rospy.Publisher("/landing_gear/base_leg_2_link2_joint_position_controller/command", Float64, queue_size=10)
    pub_link2_leg3 = rospy.Publisher("/landing_gear/base_leg_3_link2_joint_position_controller/command", Float64, queue_size=10)
    sub = rospy.Subscriber("/landing_gear/joint_states", JointState, update_joint_link2)
    r = rospy.Rate(30)
    rospy.sleep(1)
    start = rospy.Time().now().secs
    rospy.loginfo("mulai")
    flag = True
    angle = 0 
    while rospy.Time().now().secs - start < 30 and not rospy.is_shutdown():
        if flag:
            angle += 1
        else: 
            angle -= 1
        if angle >= 157 or angle <=0:
            flag = not flag
        val = Float64(-angle/100)
        # rospy.loginfo(f"flag = {flag} \n rad = {angle}")
        pub_leg1.publish(val)
        pub_leg2.publish(val)
        pub_leg3.publish(val)
        r.sleep()
    rospy.loginfo("end")
    rospy.signal_shutdown("selesai demo")
    