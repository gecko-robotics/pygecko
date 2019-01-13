#include "core.hpp"
#include <iostream>
#include <thread>
#include <string>
#include "network.hpp"
#include "transport.hpp"
#include "time.hpp"
#include "helpers.hpp"
#include "misc.hpp"

// using namespace gecko;
using namespace std;

////////////////////////////////////////////////////////////////////////////////


std::vector<std::string> split(const std::string& s, char delimiter){
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(s);
    while (std::getline(tokenStream, token, delimiter))
    {
      tokens.push_back(token);
    }
    return tokens;
}

////////////////////////////////////////////////////////////////////////////////

Core::Core(int port): bindPort(port)
{
    // HostInfo h = HostInfo();
    // string addr = zmqTCP(h.addr, to_string(port));
    // auto server = make_tuple(addr, port);
    // cout << h.hostname << "["<< addr << "]" << endl;

    // Reply rep(fmtstr("tcp://*:%d", port));
    // bindPort = port;
}

void Core::run(int hertz){
    thread request(&Core::requestLoop, this);
    request.join();

    Rate rate(hertz);
    while(ok){
        cout << "." << flush;
        rate.sleep();
    }
    cout << "bye" << endl;
}

void Core::requestLoop(void){
    Rate rate(50);
    // Reply rep(fmtstr("tcp://*:%d", bindPort));
    Reply rep(std::string("tcp://*:") + std::to_string(bindPort));
    // using namespace std::placeholders; // for `_1`
    // auto cb = std::bind(&Core::handle_reply);
    while(ok){
        rep.listen_nb(&Core::handle_reply);
        rate.sleep();
    }
}

/*
m: set/get:topic
return: tcp://1.2.3.4:1234
*/
zmq::message_t Core::handle_reply(zmq::message_t& m){
    printf(">> handle_reply\n");
    if (m.size() == 0){
        printf(">> no message\n");
        return zmq::message_t();
        // return zmq::message_t("hi",2);
    }
    string s(static_cast<char*>(m.data()), m.size());
    vector<string> toks = split(s, ':');
    if (toks[0] == "set"){
        printf("set\n");
    }
    else if (toks[0] == "get"){
        printf("get\n");
    }
    string a = zmqTCP("127.0.0.1","1000");
    return zmq::message_t(a.c_str(), a.size());
}
