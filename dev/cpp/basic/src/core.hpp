#pragma once

#include <map>
#include <string>
// #include <tuple>
// // #include <transport.hpp>
// #include "transport.hpp"
// #include "time.hpp"
#include "signals.hpp"

namespace gecko {

// class SigCapture {
// public:
//     SigCapture();
//     static void my_handler(int s);
//
// protected:
//     static bool shutdown;
// };

class Core: protected SigCapture {
    /*
    GeckoCore
    */
public:
    Core(int port, int hertz=100);
    void run(void);
    // static void init(int argc, char* argv[]);
    // static void shutdown(void){shutdown = true;}

protected:
    int handle_reply();
    // static std::string core_addr;
    static std::map<std::string, std::string> directory;
    // bool shutdown;
};

}
