#include <iostream>
#include <thread>
#include <chrono>
#include <stdio.h>
#include <unistd.h>  // usleep

// copy header from here
// https://github.com/zeromq/cppzmq
#include "zmq.hpp"
#include "zmq_addon.hpp"

using namespace std;

void sub(void){
    zmq::context_t context(1);
    const string protocol = "tcp://localhost:5555";
    zmq::socket_t sock (context, ZMQ_SUB);
    sock.connect(protocol);
    sock.setsockopt(ZMQ_SUBSCRIBE, "", 0);

    while(true){
        zmq::message_t msg;
        // sock.recv(&msg, ZMQ_DONTWAIT); // non-blocking
        sock.recv(&msg, 0); // blocking
        if(msg.size() > 0){
            string s(static_cast<char*>(msg.data()), msg.size());
            printf(">> [SUB] msg[%zu]: %s\n", s.size(), s.c_str());
        }
        else printf("** No data found\n");
        usleep(100000);
    }
    sock.close();
}

void pub(void){
    zmq::context_t context(1);
    const string protocol = "tcp://*:5555";
    zmq::socket_t sock (context, ZMQ_PUB);
    sock.bind(protocol);

    while(true){
        zmq::message_t msg((void*)"kevin", 5);
        sock.send(msg);
        printf(">> [PUB] sent msg\n");
        usleep(1000000);
    }
    sock.close();
}

////////////////////////////////////////////////////////////////
// multipart
void msub(void){
    zmq::context_t context(1);
    const string protocol = "tcp://localhost:5556";
    zmq::socket_t sock (context, ZMQ_SUB);
    sock.connect(protocol);
    string topic = "bob";
    sock.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.size());
    // sock.setsockopt(ZMQ_SUBSCRIBE, "", 0);

    zmq::multipart_t multi;

    while(true){
        // zmq::message_t msg;
        // sock.recv(&msg, ZMQ_DONTWAIT); // non-blocking
        bool ok = multi.recv(sock, ZMQ_DONTWAIT);
        if (ok) printf(">> [SUB] msg size: %zu\n", multi.size());
        else printf("** [SUB] crap crackers\n");
        // while(multi.size() > 0){
        //     zmq::message_t msg = multi.pop();
        //     string s(static_cast<char*>(msg.data()), msg.size());
        //     printf(">> [SUB] msg[%zu]: %s\n", s.size(), s.c_str());
        // }
        // else printf("** No data found\n");
        if(multi.size() == 2){
            zmq::message_t m = multi.pop();
            string msg(static_cast<char*>(m.data()), m.size());
            zmq::message_t t = multi.pop();
            string topic(static_cast<char*>(t.data()), t.size());
            cout <<">> [SUB] "<< topic << ": " << msg << endl;
        }
        else printf("** [SUB] 2 crap crackers\n");

        usleep(500000);
    }
    sock.close();
}

void mpub(void){
    zmq::context_t context(1);
    const string protocol = "tcp://*:5556";
    zmq::socket_t sock (context, ZMQ_PUB);
    sock.bind(protocol);

    zmq::multipart_t multi;

    while(true){
        multi.push(zmq::message_t((void*)"kevin", 5));
        multi.push(zmq::message_t((void*)"bob", 3));
        bool ok = multi.send(sock);
        if (ok) printf(">> [PUB] sent msg\n");
        else printf("** [PUB] crap crackers!!\n");
        sleep(1);
    }
    sock.close();
}

int main(void){
    thread s(msub);
    thread s2(msub);
    thread p(mpub);

    s.join();
    s2.join();
    p.join();

    return 0;
}
