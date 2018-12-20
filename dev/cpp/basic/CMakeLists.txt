cmake_minimum_required(VERSION 3.6)
project(gecko)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# get msgpack
include_directories(/usr/local/include)
link_directories(/usr/local/lib)


include_directories(src)
include_directories(./)

## load in pkg-config support
find_package(PkgConfig)
find_package(Threads REQUIRED)
pkg_check_modules(ZMQ REQUIRED libzmq)

# message(STATUS "include: ${ZMQ_INCLUDE_DIRS}")
# message(STATUS "lib: ${ZMQ_LIBRARIES}")

file(GLOB SOURCES src/*.cpp)

include_directories(${ZMQ_INCLUDE_DIRS})
add_library(${PROJECT_NAME} SHARED ${SOURCES})
target_link_libraries(${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

# add_executable(net src/network.cpp)
add_executable(test test.cpp)
target_link_libraries(test ${PROJECT_NAME})

add_executable(zmq-test tests/zmq-test.cpp)
target_link_libraries(zmq-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(msgpack-test tests/msgpack-test.cpp)

add_executable(time-test tests/time-test.cpp)
target_link_libraries(time-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(ip-test tests/ip-test.cpp)
target_link_libraries(ip-test ${PROJECT_NAME})


add_executable(proc-test tests/proc-test.cpp)
target_link_libraries(proc-test ${PROJECT_NAME})
