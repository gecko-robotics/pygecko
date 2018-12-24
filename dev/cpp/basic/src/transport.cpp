#include <transport.hpp>
#include <iostream>

using namespace std;


zmq::context_t gContext(1);


// zmqBase::zmq::context_t gContext(1);


Publisher::Publisher(): sock(gContext, ZMQ_PUB)
{
    // publisher.bind(addr + std::string(":") + std::to_string(port));
}

/*
Will bind or connect to an address (tcp://x.x.x.x:*, where * can be replacced
with a port number if desired)
https://stackoverflow.com/questions/16699890/connect-to-first-free-port-with-tcp-using-0mq
*/
Publisher::Publisher(std::string addr, bool bind): sock(gContext, ZMQ_PUB)
{
    if (bind){
        sock.bind(addr);
        char port[1024]; //make this sufficiently large.
                 //otherwise an error will be thrown because of invalid argument.
        size_t size = sizeof(port);
        sock.getsockopt( ZMQ_LAST_ENDPOINT, &port, &size );
        port_number = port;
        cout << "socket is bound at port " << port_number << endl;
    }
    else {
        // sock.connect()
    }
}

void Publisher::pub(zmq::message_t& msg){
    sock.send(msg);
}

void Publisher::serialize(){}


///////////////////////////////////////////////////

Subscriber::Subscriber(): sock(gContext, ZMQ_SUB)
{
    // subscriber.connect(addr + std::string(":") + std::to_string(port));
    // subscriber.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.length());
}

Subscriber::Subscriber(std::string addr, std::string topic, bool bind): sock(gContext, ZMQ_SUB)
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

Reply::Reply(): sock(gContext, ZMQ_REP) {;}

void Reply::listen(void (*callback)(std::string)){
    ;
}

////////////////////////////////////////////////////

Request::Request(std::string addr): sock(gContext, ZMQ_REQ) {
    sock.connect(addr);
}

std::string Request::get(std::string s){
    zmq::message_t msg;
    sock.send(msg);
}

////////////////////////////////////////////////////

// template <typename T>
// Publisher2<T>::Publisher(std::string addr, int port): publisher(gContext, ZMQ_PUB)
// {
//     publisher.bind(addr + std::string(":") + std::to_string(port));
// }
//
// template <typename T>
// void Publisher2<T>::pub(T& msg){
//     publisher.send(msg);
// }
//
// void Publisher2::serialize(){}
