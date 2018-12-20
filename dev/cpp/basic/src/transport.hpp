#pragma once

#include <string>
#include "zmq.hpp"


class Publisher {
public:
    Publisher(std::string addr, int port);
    void pub(zmq::message_t& msg);
protected:
    void serialize();
    zmq::socket_t publisher;
};


class Subscriber {
public:
    Subscriber(std::string addr, int port, std::string topic);
    zmq::message_t recv();
protected:
    zmq::socket_t subscriber;
};
