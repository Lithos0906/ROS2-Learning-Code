#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "chapter4_interface/srv/partol.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"

using Partol = chapter4_interface::srv::Partol;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;

class TurtleController: public rclcpp::Node
{
private:
    OnSetParametersCallbackHandle::SharedPtr parameter_callback_handle_;
    rclcpp::Service<Partol>::SharedPtr partol_service_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_subscription_;
    double target_x_{1.0};
    double target_y_{1.0};
    double k_{1.0};
    double max_speed_{3.0};

public:
    explicit TurtleController(const std::string& node_name): Node(node_name)
    {
        this->declare_parameter("k", 1.0);
        this->declare_parameter("max_speed", 1.0);
        this->get_parameter("k", k_);
        this->get_parameter("max_speed", max_speed_);
        // Methods for setting parameters of its own node.
        // this->set_parameter(rclcpp::Parameter("k", 2.0));

        parameter_callback_handle_ = this->add_on_set_parameters_callback([&](const std::vector<rclcpp::Parameter> & parameters)->
            rcl_interfaces::msg::SetParametersResult{
                rcl_interfaces::msg::SetParametersResult result;
                result.successful = true;
                for(const auto & parameter : parameters)
                {
                    RCLCPP_INFO(this->get_logger(), "update the value of param %s=%f", parameter.get_name().c_str(), parameter.as_double());
                    if(parameter.get_name() == "k")
                    {
                        k_ = parameter.as_double();
                    }
                    if(parameter.get_name() == "max_speed")
                    {
                        max_speed_ = parameter.as_double();
                    }
                }
                return result;
        });

        partol_service_ = this->create_service<Partol>("partol", [&](const Partol::Request::SharedPtr request, Partol::Response::SharedPtr response) -> void{
            if((0<request->target_x && request->target_x<12.0f) && (0<request->target_y && request->target_y<12.0f))
            {
                this->target_x_ = request->target_x;
                this->target_y_ = request->target_y;
                response->result = Partol::Response::SUCCESS;
            }
            else
            {
                response->result = Partol::Response::FAIL;
            }
        });
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        pose_subscription_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose", 10, std::bind(&TurtleController::on_pose_received_, this, std::placeholders::_1));
    }

private:
    void on_pose_received_(const turtlesim::msg::Pose::SharedPtr pose)
    {
        auto message = geometry_msgs::msg::Twist();
        double current_x = pose->x;
        double current_y = pose->y;
        RCLCPP_INFO(this->get_logger(), "current position: (x=%f, y=%f)", current_x, current_y);

        double distance = std::sqrt((target_x_ - current_x) * (target_x_ - current_x) + (target_y_ - current_y) * (target_y_ - current_y));
        double angle = std::atan2(target_y_ - current_y, target_x_ - current_x) - pose->theta;

        if(distance > 0.1)
        {
            if(fabs(angle)>0.2)
            {
                message.angular.z = fabs(angle);
            }
            else
            {
                message.linear.x = k_ * distance;
            }
        }

        if(message.linear.x > max_speed_)
        {
            message.linear.x = max_speed_;
        }
        velocity_publisher_->publish(message);
    }
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleController>("turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
