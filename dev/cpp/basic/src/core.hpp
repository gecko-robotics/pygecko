#pragma once

#include <map>
#include <string>
// #include <tuple>

namespace gecko {

class SigCapture {
public:
    SigCapture();
    static void my_handler(int s);

protected:
    static bool shutdown;
};

class Core: protected SigCapture {
public:
    Core(int port, int hertz=100);
    void run(void);

protected:
    int handle_reply();

    std::map<std::string, std::string> directory;
    // bool shutdown;
};

}
