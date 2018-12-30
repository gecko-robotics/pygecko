#pragma once

/*
https://www.geeksforgeeks.org/chrono-in-c/

system_clock-It is the current time according to the system (regular clock
  which we see on the toolbar of the computer). It is written as-
  std::chrono::system_clock
steady_clock-It is a monotonic clock that will never be adjusted.It goes at a
  uniform rate. It is written as- std::chrono::steady_clock
high_resolution_clock– It provides the smallest possible tick period. It is
  written as-std::chrono::high_resolution_clock
*/

#include <chrono>
// #include <ctime>
// #include <thread>
#include <google/protobuf/util/time_util.h>

class Time {
public:
    long now();  // chrono seconds since epic
    // google::protobuf::Timestamp unixNow();  // unix based timestamp
    google::protobuf::Timestamp unix();  // unix based timestamp
    void msleep(int);
    void sleep(int);
};


class Rate {
public:
    Rate(double);
    void sleep(void);
protected:
    std::chrono::time_point<std::chrono::system_clock> last_time;
    // std::chrono::duration<double> dt;
    std::chrono::milliseconds dt;
};
