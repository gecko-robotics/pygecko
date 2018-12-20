#pragma once

/*
https://beej.us/guide/bgnet/html/multi/gethostbynameman.html
PLEASE NOTE: these two functions are superseded by getaddrinfo() and
getnameinfo()! In particular, gethostbyname() doesn't work well with IPv6.
*/

// #include <stdio.h>
// #include <stdlib.h>
// #include <unistd.h>
// #include <errno.h>
// #include <netdb.h>
// #include <sys/types.h>
// #include <sys/socket.h>
// #include <netinet/in.h>
// #include <arpa/inet.h>
#include <string>
// #include <iostream>

class HostInfo {
public:
    HostInfo();
    std::string hostname;
    std::string addr;
};
