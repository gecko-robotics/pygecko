#pragma once

#include <string>
#include <netinet/in.h>  // sockaddr_in


class Beacon {
public:
    Beacon(std::string);
    int initSocket(bool reuse);
    bool recv(std::string& msg);
    bool send(std::string message);
    bool ready(int usec);
    void print(std::string);

    std::string group;  // ip address
    const int port;     // port number
    int fd;             // socket file descriptor
    struct sockaddr_in addr; // need for send/recv
    const int MSGBUFSIZE;  // change to array?
};

// machine:topic
// machine:topic:ip:port

class Listener: Beacon {
public:
    Listener();
    int listen();  // topic:bob:1.2.3.4:9000
};


class Search: Beacon {
public:
    Search();
    std::string find(std::string);  // topic:bob
};
