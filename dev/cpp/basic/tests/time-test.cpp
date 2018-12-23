#include <iostream>
// #include <chrono>
// #include <ctime>
#include <thread>
#include "time.hpp"

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


// using namespace std::chrono;
using namespace std;

// class Time {
// public:
//     long now();
// };

// long Time::now(){
//     // auto now = system_clock::now();
//     auto now_ms = time_point_cast<milliseconds>(system_clock::now());
//     auto epic = now_ms.time_since_epoch();
//     long time = epic.count();
//     return time;
// }

// class Rate {
// public:
//     Rate(double);
//     void sleep(void);
// protected:
//     std::chrono::time_point<std::chrono::system_clock> last_time;
//     // std::chrono::duration<double> dt;
//     milliseconds dt;
//
// };

// Rate::Rate(double hertz){
//     last_time = time_point_cast<milliseconds>(system_clock::now());
//     // dt = std::chrono::milliseconds(int(1000/hertz));
//     dt = milliseconds(int(1000/hertz));
//
//     // cout << dt.count() << endl;
//     //
//     // // last_time = time_point_cast<milliseconds>(system_clock::now());
//     //
//     // std::this_thread::sleep_for(std::chrono::milliseconds(100));
//     //
//     // auto now = time_point_cast<milliseconds>(system_clock::now());
//     //
//     // auto diff = duration_cast<std::chrono::milliseconds>(now - last_time);
//     //
//     // // cout << now << endl;
//     // //
//     // // cout << last_time << endl;
//     //
//     // cout << diff.count() << endl;
//     // // cout << diff << endl;
// }
//
// void Rate::sleep(void){
//     auto now = time_point_cast<milliseconds>(system_clock::now());
//
//     auto diff = duration_cast<std::chrono::milliseconds>(now - last_time);
//     if (diff < dt){
//         this_thread::sleep_for(dt - diff);
//     }
//     last_time = time_point_cast<milliseconds>(system_clock::now());
// }

int main (){
    // auto now = system_clock::now();
    // auto now_ms = time_point_cast<milliseconds>(now);
    //
    // auto value = now_ms.time_since_epoch();
    // long duration = value.count();
    //
    // cout << duration << endl;
    //
    // milliseconds dur(duration);
    //
    // time_point<system_clock> dt(dur);
    //
    // if (dt != now_ms)
    //     std::cout << "Failure." << std::endl;
    // else
    //     std::cout << "Success." << std::endl;
    Rate r(5);

    Time a;
    long s, f;
    // cout << a.now() << endl;
    s = a.now();

    // usleep(1E6);
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    f = a.now();

    cout << ">> sleep for 1000: " << f-s << endl;
}
