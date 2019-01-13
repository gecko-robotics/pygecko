#include "transport.hpp"
#include "zmq.hpp"
#include "time.hpp"

using namespace std;

zmq::context_t zmqBase::gContext(1);
zmqBase::zmqBase(int type): sock(gContext, type) {}

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
        // cout << count << endl;
        if (ret < 0){
            cout << "zmqBase::check failed: " << ret << endl;
            return false;
        }
        if (ret > 0) return true;
        // Time::msleep(1);
    }
    return false;
}

void zmqBase::update(){
    std::array<char, 100> e;  // tcp://x.x.x.x:port
    size_t e_size = e.size();
    sock.getsockopt(ZMQ_LAST_ENDPOINT, e.data(), &e_size);

    endpoint.assign(e.data(), e.size());
    std::cout << ">> endpoint: " << endpoint << std::endl;
}

// ~zmqBase(){sock.close(); gContext.close();}
zmqBase::~zmqBase(){
    // any pending sends will block the context destructor
    cout << ">> killing (ZMQ_LINGER): " << endpoint << endl;
    int msec = 5;
    sock.setsockopt(ZMQ_LINGER, &msec, sizeof(msec));
    sock.close();
}

///////////////////////////////////////////////////////////////

Publisher::Publisher(): zmqBase(ZMQ_PUB){}

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
    update();
    // char port[1024]; //make this sufficiently large to avoid invalid argument.
    // size_t size = sizeof(port);
    // sock.getsockopt( ZMQ_LAST_ENDPOINT, &port, &size );
    // endpoint = port;
    // cout << "socket is bound at port " << port_number << endl;
}

void Publisher::pub(zmq::message_t& msg){
    sock.send(msg);
}

// void Publisher::serialize(){}


///////////////////////////////////////////////////

Subscriber::Subscriber(): zmqBase(ZMQ_SUB)
{
    // subscriber.connect(addr + string(":") + to_string(port));
    // subscriber.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.length());
    callback = nullptr;
}

Subscriber::Subscriber(string addr, string topic, bool bind): zmqBase(ZMQ_SUB)
{
    sock.connect(addr);
    sock.setsockopt(ZMQ_SUBSCRIBE, topic.c_str(), topic.length());
    callback = nullptr;
    update();
}

zmq::message_t Subscriber::recv(int flags){
    zmq::message_t msg;
    sock.recv(&msg, flags);
    return msg;
}


void Subscriber::setCallback(void(*cb)(zmq::message_t&)){
    callback = cb;
}

////////////////////////////////////////////////////

Reply::Reply(std::string addr): zmqBase(ZMQ_REP) {
    sock.bind(addr);
    update();
}

void Reply::listen(zmq::message_t (*callback)(zmq::message_t&), int flags){
    zmq::message_t request;

    if (zmqBase::check(1) == false) return;

    sock.recv (&request, flags);

    // if (request.size() == 0) return;

    //  create the reply
    zmq::message_t reply = callback(request);
    printf(">> sending reply\n");
    cout << reply << endl;
    if (reply.size() > 0) sock.send(reply);
}


////////////////////////////////////////////////////

Request::Request(std::string addr): zmqBase(ZMQ_REQ)  {
    sock.connect(addr);
    update();
}

zmq::message_t Request::get(zmq::message_t& msg, int flags){
    sock.send(msg);

    bool msg_ready = zmqBase::check(1);

    zmq::message_t rep;
    if (msg_ready) sock.recv(&rep, flags);

    return rep;
}
