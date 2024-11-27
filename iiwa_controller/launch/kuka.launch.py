import os
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    package_dir = get_package_share_directory('iiwa_controller')
    robot_description_path = os.path.join(package_dir, 'config', 'LBRiiwa7R800.urdf')
    
    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'kuka_world.wbt')
    )
    
    lbr_driver = WebotsController(
        robot_name='LBRiiwa7R800',
        parameters=[
            {'robot_description': robot_description_path},
        ],
        respawn=True
    )
    
    position_publisher = Node(
		package='iiwa_controller',
		executable='positionPublisher'
	)
    
    return LaunchDescription([
        webots,
        lbr_driver,
        position_publisher,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])