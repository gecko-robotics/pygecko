#pragma once

#include <string>
#include <array>
#include <iostream>
#include "zmq.hpp"
#include "time.hpp"
// #include "rep_req.pb.h"


class zmqBase {
public:
    // zmqBase(): gContext(1) {}
    // zmqBase(int type): gContext(1), sock(gContext, type) {}
    zmqBase(int type): sock(gContext, type) {}
    void update(){
        std::array<char, 100> e;  // tcp://x.x.x.x:port
        size_t e_size = e.size();
        sock.getsockopt(ZMQ_LAST_ENDPOINT, e.data(), &e_size);

        endpoint.assign(e.data(), e.size());
        std::cout << "c " << endpoint << std::endl;
    }

    bool check(int retry=5);

    // ~zmqBase(){sock.close(); gContext.close();}
    static zmq::context_t gContext;  // context
    zmq::socket_t sock;
    std::string endpoint;
};

// zmqBase::zmq::context_t gContext(1);

// class zmqBase2 {
// public:
//     // zmqBase(): gContext(1) {}
//     zmqBase2(int type): gContext(1), sock(gContext, type) {}
//     void update(){
//         std::array<char, 100> e;
//         size_t e_size = e.size();
//         sock.getsockopt(ZMQ_LAST_ENDPOINT, e.data(), &e_size);
//
//         endpoint.assign(e.data(), e.size());
//         std::cout << "c " << endpoint << std::endl;
//     }
//     // ~zmqBase(){gContext.close();}
//     zmq::context_t gContext;  // connection: tcp://x.x.x.x:port
//     zmq::socket_t sock;
//     std::string endpoint;
// };

class Publisher: public zmqBase {
public:
    Publisher();
    ~Publisher(){sock.close();}
    Publisher(std::string addr, bool bind=true);  // tcp://x.x.x.x:port
    void pub(zmq::message_t& msg);
    // static Publisher advertise(std::string topic, int queue);
    std::string port_number;
protected:
    void serialize();
    // zmq::socket_t sock;

    // static std::string gecko_core;
};


class Subscriber: public zmqBase {
public:
    Subscriber();
    ~Subscriber(){sock.close();}
    Subscriber(std::string addr, std::string topic, bool bind=false);
    zmq::message_t recv();
protected:
    // zmq::socket_t sock;
};

class Reply: public zmqBase {
public:
    Reply();
    ~Reply(){sock.close();}
    void listen(void(*)(zmq::message_t&));
protected:
    // zmq::socket_t sock;
};

template <typename T>
class Request: public zmqBase {
public:
    Request(std::string&);
    ~Request(){sock.close();}
    T get(T&);
protected:
    // zmq::socket_t sock;
};

template <typename T>
Request<T>::Request(std::string& addr): zmqBase(ZMQ_REQ)  {
    sock.connect(addr);
    update();
    // std::array<char, 100> endpoint;
    // size_t endpoint_size = endpoint.size();
    // sock.getsockopt(ZMQ_LAST_ENDPOINT, endpoint.data(), &endpoint_size);
    //
    // std::string e;
    // e.assign(endpoint.data(), endpoint.size());
    // std::cout << "c " << e << std::endl;
    // for (int i; i < endpoint.size(); i++) std::cout << endpoint[i] << std::flush;
    // std::cout << std::endl;
}

template <typename T>
T Request<T>::get(T& req){
    Rate rate(1);

    std::string s;
    req.SerializeToString(&s);
    zmq::message_t msg(s.size());
    memcpy((void*) msg.data(), s.c_str(), s.size());
    sock.send(msg);

    // zmq::poller_t<> poll;
    // poll.add(sock, ZMQ_POLLIN, nullptr);
    //
    // std::vector<zmq_poller_event_t> events(1);
    // for (int count=5; count > 0; --count){
    //     std::cout << "count: " << count << std::endl;
    //     poll.wait_all(events, std::chrono::microseconds{1});
    //     // poll.wait_all(events, 1000);
    //     if (count == 0) {
    //         std::cout << "poll done" << std::endl;
    //         T None;
    //         return None;
    //     }
    //
    //     rate.sleep();
    // }

    bool msg_ready = zmqBase::check();

    std::cout << "msg ready " << msg_ready << std::endl;

    T preply;
    if (msg_ready){
        zmq::message_t rep;
        sock.recv(&rep);
        preply.ParseFromArray(rep.data(), rep.size());
    }
    return preply;
}


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
