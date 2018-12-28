#include "gecko.hpp"
#include <iostream>
#include <string>
#include "transport.hpp"
#include "network.hpp"
#include "rep_req.pb.h"
#include "signals.hpp"
#include "time.hpp"

using namespace std;
using namespace gecko;
using namespace msg;

/*
This holds the static info for this thread/process. User will never call this
but just access it via the functions below.
*/
// class GeckoCore: public SigCapture {
class GeckoCore{
public:
    GeckoCore();
    ~GeckoCore();
    bool isOk(){return false;}
    void print(){
        cout << "[GeckoCore]--------------------------" << endl;
        cout << "  Status: " << ((initialized) ? "Initialized" : "Not Ready") << endl;
        cout << "  Core: " << core_addr << endl;
        cout << "  Host: " << host_addr << endl;
    }
    string core_addr;  // address geckocore runs at
    string host_addr;  // address of the system this process/thread runs at
    vector<Subscriber*> subs;
    bool initialized;  // has geckocore been initialized yet?
};

GeckoCore::GeckoCore(): initialized(false) {
    cout << "GeckoCore: constructor" << endl;
}

GeckoCore::~GeckoCore(){
    cout << "bye" << endl;
}

// one static instance that holds all of the info
static GeckoCore _geckocore;


void gecko::init(int argc, char* argv[]){
    if (_geckocore.initialized) return;

    HostInfo h = HostInfo();
    _geckocore.host_addr = h.addr;

    if(argc < 2) _geckocore.core_addr = string("tcp://") + _geckocore.host_addr + ":11311";
    else _geckocore.core_addr = string("tcp://") + string(argv[1]) + ":11311";

    Request<PubSub> req(_geckocore.core_addr);
    PubSub reqmsg;
    // PubSub repmsg = req.get(reqmsg);
    PubSub repmsg = req.get(reqmsg);
    cout << "gecko::init " << sizeof(repmsg) << " " << repmsg.DebugString() << endl;
    cout << "ho " << false << true << endl;

    if (repmsg.status() == "ok") _geckocore.initialized = true;
    else {
        cout << "*** Couldn't find GeckoCore [" << _geckocore.core_addr << "] ***" << endl;
        // exit(1);
    }

    _geckocore.print();
}

Publisher* gecko::advertise(string topic, int queue=10){
    // Request<PubSub> req(_geckocore.core_addr);

    string addr = string("tcp://") + _geckocore.host_addr + string(":*");  // bind to next available port

    Publisher *p = new Publisher(addr, true);
    return p;
}

void gecko::subscribe(string topic, int queue=10, void(*callback)(string)=NULL){
    Request<PubSub> req(_geckocore.core_addr);
    // Subscriber *s = new Subscriber(addr, topic, false);
    // callbacks.push_back(s);
    // return Subscriber(core_addr, topic);
}

void gecko::spin(int hertz=50){
    Rate rate(hertz);
    while(_geckocore.isOk()){
        for(int i=0; i < _geckocore.subs.size(); ++i){
            zmq::message_t msg = _geckocore.subs[i]->recv();
        }
        rate.sleep();
    }
}

void gecko::loginfo(std::string msg){
    cout << "[INFO]: " << msg << endl;
}


// string Gecko::core_addr;
// string Gecko::host_addr;
// bool Gecko::initialized = false;
// static bool ok = true;
//
// void Gecko::init(int argc, char* argv[]){
//     if (initialized) return;
//
//     HostInfo h = HostInfo();
//     host_addr = h.addr;
//
//     if(argc < 2) core_addr = string("tcp://") + host_addr + ":11311";
//     else core_addr = string("tcp://") + string(argv[1]) + ":11311";
//     //
//     // HostInfo h = HostInfo();
//     // host_addr = h.addr;
//
//     Request req(core_addr);
//     string msg = req.get(string("ping"));
//
//     if (msg == "ok") initialized = true;
//     else {
//         cout << "*** Couldn't find GeckoCore [" << core_addr << "] ***" << endl;
//         exit(1);
//     }
// }
//
// Publisher* Gecko::Gecko::advertise(std::string topic, int queue=10){
//     Request req(core_addr);
//
//     string addr = string("tcp://") + host_addr + string(":*");  // bind to next available port
//
//     Publisher *p = new Publisher(addr, true);
//     return p;
// }
//
// void Gecko::subscribe(std::string topic, int queue=10, void(*callback)(std::string)=NULL){
//     Request req(core_addr);
//     // Subscriber *s = new Subscriber(addr, topic, false);
//     // callbacks.push_back(s);
//     // return Subscriber(core_addr, topic);
// }
//
// void Gecko::spin(int hertz=50){
//     Rate rate(hertz);
//     while(ok){
//         for(int i=0; i < subs.size(); ++i){
//             zmq::message_t msg = subs[i]->recv();
//         }
//         rate.sleep();
//     }
// }
