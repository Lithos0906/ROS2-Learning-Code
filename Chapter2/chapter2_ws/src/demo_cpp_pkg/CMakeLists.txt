cmake_minimum_required(VERSION 3.8)
project(demo_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)    # find the head files and library files
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(cpp_node src/cpp_node.cpp)

# message(STSTUS ${rclcpp_INCLUDE_DIRS})    # head-files and head-files rclcpp depends on
# message(STSTUS ${rclcpp_LIBRARIES})    # library-files and library-files rclcpp depends on

# target_include_directories(cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS})    # head-files included
# target_link_libraries(cpp_node ${rclcpp_LIBRARIES})    # library-files linked

ament_target_dependencies(cpp_node rclcpp)

install(TARGETS cpp_node
  DESTINATION lib/${PROJECT_NAME}
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
