#pragma once

#include <string>
#include <unistd.h>  // getopt
#include "transport.hpp"
#include "time.hpp"
#include "signals.hpp"



class Gecko: protected SigCapture {
    /*
    Gecko
    knows:
    - GeckoCore address and port
    */
public:
    // Core(int port, int hertz=100);
    // void run(void);
    static void init(int argc, char* argv[]);
    static void shutdown(void){ok = false;}
    // static void ok(){return ok;}

    // static void loginfo(std::string msg, std::string topic){;}
    // static void logwarn(std::string msg, std::string topic){;}
    // static void logerror(std::string msg, std::string topic){;}
    // void loginfo(std::string msg, std::string topic){}
    // Publisher* Publisher(std::string topic, addr=None, int queue_size=5, bool bind=True){return 0;}

    static Publisher* advertise(std::string topic, int queue);
    static void subscribe(std::string topic, int queue, void(*callback)(std::string));
    void spin(int);
protected:
    // int handle_reply();
    static std::string core_addr;
    static std::string host_addr;
    std::vector<Subscriber*> subs;
    static bool initialized;
    // static std::map<std::string, std::string> directory;
    // static bool ok;
};

namespace gecko {
    /*
    class Gecko {
    public:
        core_addr
        host_addr
        subs
        initialized
}
    */
}
