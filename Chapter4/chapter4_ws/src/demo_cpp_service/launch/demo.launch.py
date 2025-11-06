import launch
import launch_ros

def generate_launch_description():
    # 1.declare a launch param
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument('launch_arg_bg', default_value="150")

    # 2.manually pass the launch parameter to a node
    # generate the description of launch
    action_node_turtlesim_node = launch_ros.actions.Node(
        package = 'turtlesim',
        executable = 'turtlesim_node',
        # obtain the launch value
        parameters=[{'background_g': launch.substitutions.LaunchConfiguration('launch_arg_bg', default="150")}],
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
        action_declare_arg_background_g,
        action_node_turtlesim_node,
        action_node_turtle_control,
        action_node_partol_client
    ])
