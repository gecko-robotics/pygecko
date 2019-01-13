#pragma once

/*
https://beej.us/guide/bgnet/html/multi/gethostbynameman.html
PLEASE NOTE: these two functions are superseded by getaddrinfo() and
getnameinfo()! In particular, gethostbyname() doesn't work well with IPv6.
*/
#include <string>

class HostInfo {
public:
    HostInfo();
    std::string hostname;
    std::string addr;
};
