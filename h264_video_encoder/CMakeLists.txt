cmake_minimum_required(VERSION 3.5)
project(h264_video_encoder)

## Compile as C++14
set(CMAKE_CXX_STANDARD 14)

find_package(h264_encoder_core REQUIRED)
find_package(aws_common REQUIRED)
find_package(aws_ros2_common REQUIRED)
find_package(image_transport REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(kinesis_video_msgs REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(rmw_implementation REQUIRED)

set(H264_VIDEO_ENCODER_LIBRARY_TARGET ${PROJECT_NAME}_lib)

###########
## Build ##
###########

add_library(${H264_VIDEO_ENCODER_LIBRARY_TARGET}
        src/h264_video_encoder.cpp
        )
ament_target_dependencies(${H264_VIDEO_ENCODER_LIBRARY_TARGET}
        ament_cmake
        rclcpp
        image_transport
        aws_common
        aws_ros2_common
        h264_encoder_core
        kinesis_video_msgs
        )

## Specify additional locations of header files
include_directories(
  include
  )

## Declare a C++ executable
add_executable(${PROJECT_NAME}
  src/main.cpp
  )
target_link_libraries(${PROJECT_NAME}
  ${H264_VIDEO_ENCODER_LIBRARY_TARGET}
  )

#############
## Install ##
#############

install(TARGETS ${PROJECT_NAME} ${H264_VIDEO_ENCODER_LIBRARY_TARGET}
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION lib/${PROJECT_NAME}
        )
install(DIRECTORY include/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h"
        )
install(DIRECTORY config/
        DESTINATION share/${PROJECT_NAME}/config
        )
install(DIRECTORY launch/
        DESTINATION share/${PROJECT_NAME}/launch
        )

ament_export_include_directories(include)

ament_export_dependencies(ament_cmake)
ament_export_dependencies(rclcpp)
ament_export_dependencies(rmw_implementation)
ament_export_dependencies(image_transport)
ament_export_dependencies(aws_common)
ament_export_dependencies(aws_ros2_common)
ament_export_dependencies(h264_encoder_core)
ament_export_dependencies(kinesis_video_msgs)

ament_package()

#############
## Tests ##
#############

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ## Add gtest based cpp test target and link libraries
  ament_add_gtest(test_h264_video_encoder
    test/h264_video_encoder_test.cpp
  )
  target_include_directories(test_h264_video_encoder
  PRIVATE include ${h264_video_encoder_INCS})
  target_link_libraries(test_h264_video_encoder
    ${H264_VIDEO_ENCODER_LIBRARY_TARGET}
    ${h264_video_encoder_LIBS}
    ${GMOCK_BOTH_LIBRARIES}
  )
endif()
