#include "rclcpp/rclcpp.hpp"
#include "chapter4_interface/srv/partol.hpp"
#include <chrono>
#include <ctime>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"

using Partol = chapter4_interface::srv::Partol;
using SetP = rcl_interfaces::srv::SetParameters;
using namespace std::chrono_literals;

class PartolClient: public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<Partol>::SharedPtr partol_client_;

public:
    explicit PartolClient() : Node("turtle_controller")
    {
        srand(time(NULL));
        partol_client_ = this->create_client<Partol>("partol");
        timer_ = this->create_wall_timer(10s, [&]()->void{
            // 1.determine if the server is online
            while(!this->partol_client_->wait_for_service(1s))
            {
                if(!rclcpp::ok())
                {
                    RCLCPP_ERROR(this->get_logger(), "While waiting for the service to be launched, rclcpp crashed, so I logged out");
                    return;
                }
                RCLCPP_INFO(this->get_logger(), "While waiting for the service to be launched.....");
            }

            // 2.structure Request
            auto request = std::make_shared<Partol::Request>();
            request->target_x = rand() % 15;
            request->target_y = rand() % 15;
            RCLCPP_INFO(this->get_logger(), "Prepare the target point: %f, %f", request->target_x, request->target_y);

            // 3. send a request and wait for processing to complete
            this->partol_client_->async_send_request(request, [&](rclcpp::Client<Partol>::SharedFuture result_future)->void{
                auto response = result_future.get();
                if(response->result == Partol::Response::SUCCESS)
                {
                    RCLCPP_INFO(this->get_logger(), "Requesting patrol target point successful");
                }
                if(response->result == Partol::Response::FAIL)
                {
                    RCLCPP_INFO(this->get_logger(), "Requesting patrol target point fail");
                }
            });
        });
    }

    // create a client and send request, returning results
    SetP::Response::SharedPtr call_set_parameters(const rcl_interfaces::msg::Parameter &param)
    {
        auto param_client = this->create_client<SetP>("/turtle_control/set_parameters");
        // 1.determine if the server is online
        while(!param_client->wait_for_service(1s))
        {
            if(!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "While waiting for the service to be launched, rclcpp crashed, so I logged out");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(), "While waiting for the service to be launched.....");
        }

        // 2.structure Request
        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(param);

        // 3. send a request and wait for processing to complete
        auto future = param_client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
        auto response = future.get();
        return response;
    }

    // update param K
    void update_server_param_k(double k)
    {
        // 1.create a param orient
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";

        // 2.create value
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;

        // 3.request to update params and handle
        auto response = this->call_set_parameters(param);
        if(response == NULL)
        {
            RCLCPP_INFO(this->get_logger(), "params update failed");
        }
        for(auto result:response->results)
        {
            if(result.successful == false)
            {
                RCLCPP_INFO(this->get_logger(), "params update failed, reason: %s", result.reason.c_str());
            }
            else
            {
                RCLCPP_INFO(this->get_logger(), "params update successfully");
            }
        }
    }
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PartolClient>();
    node->update_server_param_k(4.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
