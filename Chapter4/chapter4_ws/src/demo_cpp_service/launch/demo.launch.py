import launch
import launch_ros

def generate_launch_description():
    # generate the description of launch
    action_node_turtlesim_node = launch_ros.actions.Node(
        package = 'turtlesim',
        executable = 'turtlesim_node',
        output = 'screen'
    )

    action_node_turtle_control = launch_ros.actions.Node(
        package = 'demo_cpp_service',
        executable = 'turtle_control',
        output = 'both'
    )

    action_node_partol_client = launch_ros.actions.Node(
        package = 'demo_cpp_service',
        executable = 'partol_client',
        output = 'log'
    )

    return launch.LaunchDescription([
        # actions
        action_node_turtlesim_node,
        action_node_turtle_control,
        action_node_partol_client
    ])
