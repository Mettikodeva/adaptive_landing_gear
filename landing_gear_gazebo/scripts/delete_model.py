import rospy 
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest, DeleteModelResponse


if __name__ == "__main__":
    rospy.init_node("delete_model")
    service_client = rospy.ServiceProxy("/gazebo/delete_model",DeleteModel)

            
    response = service_client("lg")
    if response.success:
        rospy.loginfo(f"deleted model :{response}")
    else:
        print(f"failed to delete model lg: {response.status_message}")

    