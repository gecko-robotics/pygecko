#pragma once

#include <map>
#include <string>
#include <vector>
#include "signals.hpp"
#include "zmq.hpp"

// namespace gecko {

class Core: protected SigCapture {
    /*
    GeckoCore
    */
public:
    Core(int port=11311);
    void run(int hertz=100);
    void requestLoop(void);
    // static void init(int argc, char* argv[]);
    // static void shutdown(void){shutdown = true;}

protected:
    static zmq::message_t handle_reply(zmq::message_t&);
    // static std::string core_addr;
    static std::map<std::string, std::string> directory;
    // bool shutdown;
    const int bindPort;
};

std::vector<std::string> split(const std::string& s, char delimiter);

// }
