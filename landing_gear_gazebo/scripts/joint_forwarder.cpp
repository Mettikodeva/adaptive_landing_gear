#include <ros/ros.h>
#include <gazebo_msgs/SetModelConfiguration.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>
#include <sensor_msgs/JointState.h>

#include <boost/algorithm/string.hpp>
#include <gazebo_msgs/GetJointProperties.h>
#include <iostream>
#include <ros/console.h>



std_msgs::Float64MultiArray angle;


// void leg1_callback(const std_msgs::Float64::ConstPtr& msg){
//     ROS_INFO("leg1_callback");
//     angle.data.push_back(msg->data);
// }

// void leg2_callback(const std_msgs::Float64::ConstPtr& msg){
//     ROS_INFO("leg2_callback");
//     angle.data.push_back(msg->data);
// }

// void leg3_callback(const std_msgs::Float64::ConstPtr& msg){
//     angle.data.push_back(msg->data);
// }

void jointStatesCallback(const sensor_msgs::JointState::ConstPtr& msg){
    ROS_INFO("joint_states_callback");
    angle.data.clear();
    angle.data = {
        msg->position[0],
        msg->position[1],
        msg->position[2]
    };

    std::cout << "angle.data.size(): " << angle.data.size() << std::endl;
    for (int i = 0; i < angle.data.size(); i++)
    {
        std::cout << "pos: " << msg->position[i];
        std::cout << "angle: " << angle.data[i] << std::endl;
    }
}


int main(int argc, char **argv){
    ros::init(argc, argv, "joint_forwarder");
    if( ros::console::set_logger_level(ROSCONSOLE_DEFAULT_NAME, ros::console::levels::Debug) ) {
   ros::console::notifyLoggerLevelsChanged();
}
    ROS_INFO("ROS INITIALIZED");
    ros::NodeHandle n;
    


    // ros::Subscriber leg1_sub = n.subscribe("/landing_gear/base_leg_1_joint_position_controller/command", 1000, leg1_callback);
    // ros::Subscriber leg2_sub = n.subscribe("/landing_gear/base_leg_2_joint_position_controller/command", 1000, leg2_callback);
    // ros::Subscriber leg3_sub = n.subscribe("/landing_gear/base_leg_3_joint_position_controller/command", 1000, leg3_callback);
    

    ros::Duration(1).sleep();
     
    if(angle.data.size() == 0){
        angle.data.push_back(0);
        angle.data.push_back(0);
        angle.data.push_back(0);
    }
    
    ros::Subscriber joint_states_sub = n.subscribe("/landing_gear/joint_states", 1000, jointStatesCallback);
    ros::ServiceClient set_model_state = n.serviceClient<gazebo_msgs::SetModelConfiguration>("/gazebo/set_model_configuration");
    ROS_INFO("create get_joint_properties service client");
    ros::ServiceClient get_joint_properties = n.serviceClient<gazebo_msgs::GetJointProperties>("/gazebo/get_joint_properties");
    

    ROS_INFO("model");
    gazebo_msgs::SetModelConfiguration model;

    ROS_INFO("model created");


    model.request.model_name = "lg";
    model.request.joint_names = {
        "base_link2_leg_1_joint",
        "base_link2_leg_2_joint",
        "base_link2_leg_3_joint"
    };
    ROS_INFO("model.request.joint_names");
    std::cout << "angles" << std::endl;
    for (int i = 0; i < angle.data.size(); i++)
    {
        std::cout << angle.data[i] << std::endl;
    }

    model.request.joint_positions = {
        angle.data.at(0),
        angle.data.at(1),
        angle.data.at(2)}
        ;
    ROS_INFO("model.request.joint_positions");
    ROS_INFO("angle.data[0]: %f", angle.data[0]);
    ROS_INFO("angle.data[1]: %f", angle.data[1]);
    ROS_INFO("angle.data[2]: %f", angle.data[2]);

    
    set_model_state.call(model);
    ROS_INFO("call");

    ros::Rate loop_rate(60);
    
    while(ros::ok()){   

        ROS_INFO_THROTTLE(1, "joint_forwarder loop");
        model.request.joint_positions = {
        angle.data.at(0),
        angle.data.at(1),
        angle.data.at(2)
        };
        set_model_state.call(model);
        loop_rate.sleep();
        ros::spinOnce();
        model.request.joint_positions.clear();
    }

}
