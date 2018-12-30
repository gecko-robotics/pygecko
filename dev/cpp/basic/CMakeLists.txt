cmake_minimum_required(VERSION 3.6)
project(gecko)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# include(tests/catch.cmake)

find_package(Protobuf REQUIRED)
if ( Protobuf_FOUND )
    include_directories(${Protobuf_INCLUDE_DIRS})
    include_directories(${CMAKE_CURRENT_BINARY_DIR})
    message( STATUS "Protobuf version : ${Protobuf_VERSION}" )
    message( STATUS "Protobuf include path : ${Protobuf_INCLUDE_DIRS}" )
    message( STATUS "Protobuf libraries : ${Protobuf_LIBRARIES}" )
    message( STATUS "Protobuf compiler libraries : ${Protobuf_PROTOC_LIBRARIES}")
    message( STATUS "Protobuf lite libraries : ${Protobuf_LITE_LIBRARIES}")

    set(
        MSG_PROTOS
        msgs/imu.proto
        msgs/vector.proto
        msgs/image.proto
        msgs/rep_req.proto
    )
    protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${MSG_PROTOS})
else()
    message( WARNING "Protobuf package not found -> specify search path via PROTOBUF_ROOT variable")
endif()


# Get msgpack -----------------------------------------------------
include_directories(/usr/local/include)
link_directories(/usr/local/lib)

# Add local directories -------------------------------------------
include_directories(src)

# ZeroMQ ----------------------------------------------------------
# https://github.com/zeromq/cppzmq
include_directories(zmq)

# Load in pkg-config support --------------------------------------
find_package(PkgConfig)
find_package(Threads REQUIRED)

# ZeroMQ ----------------------------------------------------------
pkg_check_modules(ZMQ REQUIRED libzmq)
# add_compile_definitions(ZMQ_BUILD_DRAFT_API)
# add_compile_definitions(ZMQ_CPP11)
include_directories(${ZMQ_INCLUDE_DIRS})

# Messages --------------------------------------------------------
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "include: ${ZMQ_INCLUDE_DIRS}")
message(STATUS "zmq lib: ${ZMQ_LIBRARIES}")
message(STATUS "thread lib: ${CMAKE_THREAD_LIBS_INIT}")

# Build library ----------------------------------------------
file(GLOB SOURCES src/*.cpp)

set(ALL_LIBS ${Protobuf_LIBRARIES} ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_library(${PROJECT_NAME} SHARED ${SOURCES} ${PROTO_SRCS} ${PROTO_HDRS})
target_link_libraries(${PROJECT_NAME} ${Protobuf_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

# Tests --------------------------------------------------------------
add_executable(core-test tests/core-test.cpp)
target_link_libraries(core-test ${PROJECT_NAME})

add_executable(zmq-test tests/zmq-test.cpp)
target_link_libraries(zmq-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})


# add_executable(all-test tests/all-test.cpp ${PROTO_SRCS} ${PROTO_HDRS})
# target_link_libraries(all-test ${PROJECT_NAME} ${Protobuf_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})


# add_executable(msgpack-test tests/msgpack-test.cpp)

add_executable(time-test tests/time-test.cpp)
target_link_libraries(time-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(ip-test tests/ip-test.cpp)
target_link_libraries(ip-test ${PROJECT_NAME})

add_executable(proc-test tests/proc-test.cpp)
target_link_libraries(proc-test ${PROJECT_NAME})

add_executable(protobuf-test tests/protobuf-test.cpp ${PROTO_SRCS} ${PROTO_HDRS})
target_link_libraries(protobuf-test ${Protobuf_LIBRARIES} ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(node-test tests/node-test.cpp)
target_link_libraries(node-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(gecko-test tests/gecko-test.cpp)
target_link_libraries(gecko-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(zmq-message-test tests/zmq-message-test.cpp)
target_link_libraries(zmq-message-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})

add_executable(simple-zmq-test tests/simple-zmq-test.cpp)
target_link_libraries(simple-zmq-test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})


# add_executable(
#     unit_test
#     tests/ctest-test.cpp
# )
# add_dependencies(unit_test catch)
# target_include_directories(unit_test PUBLIC ${CATCH_INCLUDE_DIR})
# target_link_libraries(unit_test ${PROJECT_NAME} ${CMAKE_THREAD_LIBS_INIT} ${ZMQ_LIBRARIES})
# add_test(
#   NAME
#     unit
#   COMMAND
#     ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/unit_test
# )
