import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from controller_manager_msgs.srv import ListControllersRequest, ListControllers, ListControllersResponse
from controller_manager_msgs.msg import ControllerState
# ground_link_pub = rospy.Publisher("/landing_gear/ground_link_controller/command", Float64, queue_size=10)


def joint_callback(data:JointState):
    rospy.loginfo(data.name)
        # 1 = 1
        # 2 = 3
        # 3 = 5
        # 4 = 2
        # 5 = 4
        # 6 = 6

    controller_publishers[0].publish(data.position[0])
    controller_publishers[1].publish(data.position[2])
    controller_publishers[2].publish(data.position[4])
    controller_publishers[3].publish(data.position[1])
    controller_publishers[4].publish(data.position[3])
    controller_publishers[5].publish(data.position[5])

    # for i,j in enumerate(controller_publishers):
    #     j.publish(data.position[i])
    #     rospy.loginfo(f"[{i}]-publishing {data.name[i]} to {j.name}")
    # r.sleep()
# def update_joint_link2(data:JointState):
#     global pos
#     pos = data.position
#     l1 = Float64(pos[2])
#     l2 = Float64(pos[0])
#     l3 = Float64(pos[1])
#     pub_link2_leg1.publish(l1)
#     pub_link2_leg2.publish(l2)
#     pub_link2_leg3.publish(l3)
        


if __name__ == "__main__":
    rospy.init_node("joint_forwarder")
    list_controllers = rospy.ServiceProxy("/landing_gear/controller_manager/list_controllers", ListControllers)
    res = list_controllers()
    controllers = [res.controller[i].name for i in range(len(res.controller))]
    # controllers.pop()
    # joint_sub = rospy.Subscriber("/landing_gear/joint_states", JointState, update_joint_link2)
    joint_state_sub = rospy.Subscriber("/joint_states", JointState, joint_callback)
    rospy.loginfo(f"avail controllers:{controllers}")
    controller_publishers = [rospy.Publisher(f"/landing_gear/{i}/command", Float64, queue_size=10) for i in controllers]
    r = rospy.Rate(5)
    rospy.spin()

    