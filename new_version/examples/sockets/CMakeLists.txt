cmake_minimum_required(VERSION 3.4)

project(test)
# set(CMAKE_CXX_STANDARD 14)

# find_package(Protobuf REQUIRED)
# find_package (Boost COMPONENTS REQUIRED thread system)

# c++ sources
add_executable(server srv.c)
add_executable(client cli.c)

# target_link_libraries(test ${Boost_LIBRARIES})
