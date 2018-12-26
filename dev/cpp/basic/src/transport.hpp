#pragma once

#include <string>
#include "zmq.hpp"


class zmqBase {
protected:
    static zmq::context_t gContext;
    // zmq::socket_t sock;
};


class Publisher: public zmqBase {
public:
    Publisher();
    Publisher(std::string addr, bool bind=true);  // tcp://x.x.x.x:port
    void pub(zmq::message_t& msg);
    // static Publisher advertise(std::string topic, int queue);
    std::string port_number;
protected:
    void serialize();
    zmq::socket_t sock;

    // static std::string gecko_core;
};


class Subscriber: public zmqBase {
public:
    Subscriber();
    Subscriber(std::string addr, std::string topic, bool bind=false);
    zmq::message_t recv();
protected:
    zmq::socket_t sock;
};

class Reply: public zmqBase {
public:
    Reply();
    void listen(void(*)(zmq::message_t&));
protected:
    zmq::socket_t sock;
};

class Request: public zmqBase {
public:
    Request(std::string);
    std::string get(std::string);
protected:
    zmq::socket_t sock;
};


// template <typename T>
// class Publisher2 {
// public:
//     Publisher(std::string addr, int port);
//     void pub(T& msg);
// protected:
//     void serialize();
//     zmq::socket_t publisher;
// };
//
//
// class Subscriber2 {
// public:
//     Subscriber(std::string addr, int port, std::string topic);
//     zmq::message_t recv();
// protected:
//     zmq::socket_t subscriber;
// };

/*
tuple(msg_id, param1, param2, ...)

https://www.geeksforgeeks.org/tuples-in-c/

class GeckoMsg {
    int a,b,c
    tuple to_tuple();
    GeckoMsg(tuple tp){
        tie(ignore,a,b,c) = tp
    }
}

class Transport<T> {
public:
    msg serialize(T);
    T deserialize(msg);
}


class Publisher<T> {
    publish(T){
        m = sbuffer(T.to_tuple())
        zmq::send(m)
    }
}

class Subscriber<T> {
    T recv(){
        m = zmq::recv()
        tuple = deserialize(m)
        return T(tuple)
    }
}

Publisher<msgs::IMU> pub;
pub.publish(m);


Subscriber<msgs::IMU> sub;
msg = sub.recv()

*/
