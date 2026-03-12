import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os
import launch.launch_description_sources

def generate_launch_description():
    # obtain the default xacro path
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_xacro_path = os.path.join(urdf_package_path, 'urdf', 'fishbot/fishbot.urdf.xacro')
    # default_rviz_configure_path = os.path.join(urdf_package_path, 'configure', 'display_robot_model.rviz')
    default_gazebo_world_path = os.path.join(urdf_package_path, 'world', 'custom_room.world')
    # declare a content param of urdf
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_xacro_path), description="path of loading model file"
    )
    # the content is obtained from the file path
    # and converted into a parameter value object
    # to be passed to robot_state_publisher
    substitutions_command_result = launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result, value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description_value}]
    )

    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']
        ),
        launch_arguments=[('world',default_gazebo_world_path),('verbose','true')]
    )

    action_spawn_entity = launch_ros.actions.Node(
        package = 'gazebo_ros',
        executable = 'spawn_entity.py',
        arguments = ['-topic','/robot_description','-entity','fishbot']
    )

    # action_rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     arguments=['-d', default_rviz_configure_path]
    # )

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity
    ])
