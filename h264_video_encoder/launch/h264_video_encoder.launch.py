# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch.actions import OpaqueFunction
from launch.actions import LogInfo
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    node_name = LaunchConfiguration("node_name")
    config_filename = LaunchConfiguration("config_filename")

    config_filepath = PathJoinSubstitution(
        [FindPackageShare("h264_video_encoder"), "config", config_filename]
    )

    encoder_node = Node(
        package="h264_video_encoder",
        executable="h264_video_encoder",
        name=node_name,
        parameters=[config_filepath],
    )

    output_log_actions = [LogInfo(msg=config_filepath)]
    return output_log_actions + [encoder_node]


def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "node_name",
            default_value="h264_color_video_encoder",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "config_filename",
            default_value="color.yaml",
        )
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
