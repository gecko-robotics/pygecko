#pragma once

#include <string>
#include <array>
#include <iostream>
#include "zmq.hpp"
#include "time.hpp"
// #include "rep_req.pb.h"


class zmqBase {
public:
    zmqBase(int type);
    ~zmqBase();

    void update();

    bool check(int retry=5);
    static zmq::context_t gContext;  // context
    zmq::socket_t sock;
    std::string endpoint;
};

class Publisher: public zmqBase {
public:
    Publisher();
    Publisher(std::string addr, bool bind=true);  // tcp://x.x.x.x:port
    void pub(zmq::message_t& msg);
    // static Publisher advertise(std::string topic, int queue);
    // std::string port_number;
protected:
    // void serialize();
};


class Subscriber: public zmqBase {
public:
    Subscriber();
    Subscriber(std::string addr, std::string topic, bool bind=false);
    zmq::message_t recv(int flags=0);
    inline zmq::message_t recv_nb(){return recv(ZMQ_DONTWAIT);}
    void setCallback(void(*callback)(zmq::message_t&));
// protected:
    void(*callback)(zmq::message_t&);
};

class Reply: public zmqBase {
public:
    Reply(std::string addr);
    void listen(zmq::message_t(*)(zmq::message_t&), int flags=0);
    inline void listen_nb(zmq::message_t(*cb)(zmq::message_t&)){listen(cb,ZMQ_DONTWAIT);}
protected:
};


class Request: public zmqBase {
public:
    Request(std::string);
    zmq::message_t get(zmq::message_t&,int flags=0);
    zmq::message_t get_nb(zmq::message_t& req){return get(req, ZMQ_DONTWAIT);}
protected:
};
