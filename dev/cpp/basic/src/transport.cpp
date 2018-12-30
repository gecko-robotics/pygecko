#include "transport.hpp"
#include "zmq.hpp"
#include <iostream>
// #include <unistd.h>  // usleep

using namespace std;
// using zmq::context_t;

zmq::context_t zmqBase::gContext(1);
// zmq::context_t gContext(1);


// zmq::context_t zmqBase::gContext(1);

// zmqBase::zmqBase():

/*
typedef struct
{
    void* //socket//;
    int //fd//;
    short //events//;
    short //revents//;
} zmq_pollitem_t;
*/
bool zmqBase::check(int retry){
    zmq_pollitem_t items[] = {
      {sock, 0, ZMQ_POLLIN, 0},
    };

    for (int count = retry; count > 0; --count){
        int ret = zmq_poll(items, 1, 10);  // wait 10 msec
        cout << count << endl;
        if (ret < 0){
            cout << "zmqBase::checck failed: " << ret << endl;
            return false;
        }
        if (ret > 0) return true;
    }
    return false;
}

Publisher::Publisher(): zmqBase(ZMQ_PUB)
{
    // zmqBase::sock(gContext, ZMQ_PUB);
    // publisher.bind(addr + string(":") + to_string(port));
}

/*
Will bind or connect to an address (tcp://x.x.x.x:*, where * can be replacced
with a port number if desired)
https://stackoverflow.com/questions/16699890/connect-to-first-free-port-with-tcp-using-0mq
*/
Publisher::Publisher(string addr, bool bind): zmqBase(ZMQ_PUB)
{
    if (bind){
        sock.bind(addr);
    }
    else {
        sock.connect(addr);
    }
    char port[1024]; //make this sufficiently large to avoid invalid argument.
    size_t size = sizeof(port);
    sock.getsockopt( ZMQ_LAST_ENDPOINT, &port, &size );
    port_number = port;
    cout << "socket is bound at port " << port_number << endl;
}

void Publisher::pub(zmq::message_t& msg){
    sock.send(msg);
}

void Publisher::serialize(){}


///////////////////////////////////////////////////

Subscriber::Subscriber(): zmqBase(ZMQ_SUB)
{
    // subscriber.connect(addr + string(":") + to_string(port));
    // subscriber.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.length());
}

Subscriber::Subscriber(string addr, string topic, bool bind): zmqBase(ZMQ_SUB)
{
    sock.connect(addr);
    sock.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.length());
}

zmq::message_t Subscriber::recv(){
    zmq::message_t msg;
    sock.recv(&msg);
    return msg;
}

////////////////////////////////////////////////////

Reply::Reply(): zmqBase(ZMQ_REP) {;}

void Reply::listen(void (*callback)(zmq::message_t&)){
    zmq::message_t request;
    sock.recv (&request);
    callback(request);

    string smsg;

    //  create the reply
    zmq::message_t reply (smsg.size());
    memcpy ((void *) reply.data (), smsg.c_str(), smsg.size());
    sock.send (reply);
}

////////////////////////////////////////////////////

// template <typename T>
// Request<T>::Request(string& addr): sock(gContext, ZMQ_REQ) {
//     sock.connect(addr);
// }
//
// template <typename T>
// T Request<T>::get(T& req){
//     string s;
//     req.SerializeToString(&s);
//     zmq::message_t msg(s.size());
//     memcpy((void*) msg.data(), s.c_str(), s.size());
//     sock.send(msg);
//
//     zmq::message_t rep;
//     sock.recv(&rep);
//     T preply;
//     preply.ParseFromArray(rep.data(), rep.size());
//     return preply;
// }

////////////////////////////////////////////////////

// template <typename T>
// Publisher2<T>::Publisher(string addr, int port): publisher(gContext, ZMQ_PUB)
// {
//     publisher.bind(addr + string(":") + to_string(port));
// }
//
// template <typename T>
// void Publisher2<T>::pub(T& msg){
//     publisher.send(msg);
// }
//
// void Publisher2::serialize(){}
