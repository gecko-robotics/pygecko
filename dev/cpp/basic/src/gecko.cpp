#include "gecko.hpp"
#include <iostream>
#include "transport.hpp"
#include "network.hpp"
#include "rep_req.pb.h"

using namespace std;

string Gecko::core_addr;
string Gecko::host_addr;
bool Gecko::initialized = false;
// static bool ok = true;

void Gecko::init(int argc, char* argv[]){
    if (initialized) return;

    HostInfo h = HostInfo();
    host_addr = h.addr;

    if(argc < 2) core_addr = string("tcp://") + host_addr + ":11311";
    else core_addr = string("tcp://") + string(argv[1]) + ":11311";
    //
    // HostInfo h = HostInfo();
    // host_addr = h.addr;

    Request req(core_addr);
    string msg = req.get(string("ping"));

    if (msg == "ok") initialized = true;
    else {
        cout << "*** Couldn't find GeckoCore [" << core_addr << "] ***" << endl;
        exit(1);
    }
}

Publisher* Gecko::Gecko::advertise(std::string topic, int queue=10){
    Request req(core_addr);

    string addr = string("tcp://") + host_addr + string(":*");  // bind to next available port

    Publisher *p = new Publisher(addr, true);
    return p;
}

void Gecko::subscribe(std::string topic, int queue=10, void(*callback)(std::string)=NULL){
    Request req(core_addr);
    // Subscriber *s = new Subscriber(addr, topic, false);
    // callbacks.push_back(s);
    // return Subscriber(core_addr, topic);
}

void Gecko::spin(int hertz=50){
    Rate rate(hertz);
    while(ok){
        for(int i=0; i < subs.size(); ++i){
            zmq::message_t msg = subs[i]->recv();
        }
        rate.sleep();
    }
}
