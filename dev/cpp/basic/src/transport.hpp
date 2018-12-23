#pragma once

#include <string>
#include "zmq.hpp"

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



class GeckoMsg {
public:
    zmq::message_t serialize();

};


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
