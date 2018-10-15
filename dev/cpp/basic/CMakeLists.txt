cmake_minimum_required(VERSION 3.6)
project(Test)
set(CMAKE_CXX_STANDARD 14)

## load in pkg-config support
find_package(PkgConfig)
find_package(msgpack REQUIRED)
find_package(Threads REQUIRED)
pkg_check_modules(ZMQ REQUIRED libzmq)

# message(STATUS "include: ${ZMQ_INCLUDE_DIRS}")
# message(STATUS "lib: ${ZMQ_LIBRARIES}")

include_directories(${ZMQ_INCLUDE_DIRS})
add_executable(main main.cpp)
target_link_libraries(main ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})
