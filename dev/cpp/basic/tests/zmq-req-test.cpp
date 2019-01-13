#include <iostream>
#include <thread>
// #include <chrono>
// #include <sstream>
#include <stdio.h>
// #include <stdlib.h>
// #include <stdint.h>
// #include <time.h>
// #include <unistd.h>

// copy header from here
// https://github.com/zeromq/cppzmq
#include "zmq.hpp"
#include "time.hpp"
#include "transport.hpp"
// #include "rep_req.pb.h"
// #include <msgpack.hpp>

using namespace std;
// using namespace google::protobuf::util;


zmq::message_t func(zmq::message_t& msg){
    string s(static_cast<char*>(msg.data()), msg.size());
    printf(">> [FUNC] msg: %s\n", s.c_str());
    zmq::message_t ans("hi",2);
    return ans;
}

void server(int t){
    Reply rep("tcp://*:5556");

    while(true){
        rep.listen(&func);
    }
}

void client(int t){
    Request req("tcp://localhost:5556");

    for (int i = 0; i < 100; i++) {
        printf(">> [REQ] send\n");
        zmq::message_t msg("who u?",6);
        zmq::message_t ans = req.get(msg);
        cout << ">> [REQ] answer: " << ans << endl;
        Time::msleep(1000);
    }
}

int main(){
    std::cout << "start" << std::endl;
    std::thread t1(server, 500);
    std::thread t2(client, 3000);
    t1.join();
    t2.join();

    return 0;
}
