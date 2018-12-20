#include <transport.hpp>


zmq::context_t gContext(1);


Publisher::Publisher(std::string addr, int port): publisher(gContext, ZMQ_PUB)
{
    publisher.bind(addr + std::string(":") + std::to_string(port));
}

void Publisher::pub(zmq::message_t& msg){
    publisher.send(msg);
}

void Publisher::serialize(){}


///////////////////////////////////////////////////

Subscriber::Subscriber(std::string addr, int port, std::string topic): subscriber(gContext, ZMQ_SUB)
{
    subscriber.connect(addr + std::string(":") + std::to_string(port));
    subscriber.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.length());
}

zmq::message_t Subscriber::recv(){
    zmq::message_t msg;
    subscriber.recv(&msg);
    return msg;
}
