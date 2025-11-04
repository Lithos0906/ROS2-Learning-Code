#include "rclcpp/rclcpp.hpp"
#include "chapter4_interface/srv/partol.hpp"
#include <chrono>
#include <ctime>

using Partol = chapter4_interface::srv::Partol;
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
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PartolClient>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
