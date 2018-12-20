// https://www.geeksforgeeks.org/c-program-display-hostname-ip-address/
// C program to display hostname
// and IP address
// #include <stdio.h>
// #include <stdlib.h>
// #include <unistd.h>
// #include <errno.h>
// #include <netdb.h>
// #include <sys/types.h>
// #include <sys/socket.h>
// #include <netinet/in.h>
// #include <arpa/inet.h>

// // Returns hostname for the local computer
// void checkHostName(int hostname)
// {
//     if (hostname == -1)
//     {
//         perror("gethostname");
//         exit(1);
//     }
// }
//
// // Returns host information corresponding to host name
// void checkHostEntry(struct hostent * hostentry)
// {
//     if (hostentry == NULL)
//     {
//         perror("gethostbyname");
//         exit(1);
//     }
// }
//
// // Converts space-delimited IPv4 addresses
// // to dotted-decimal format
// void checkIPbuffer(char *IPbuffer)
// {
//     if (NULL == IPbuffer)
//     {
//         perror("inet_ntoa");
//         exit(1);
//     }
// }

// /*
// https://beej.us/guide/bgnet/html/multi/gethostbynameman.html
// PLEASE NOTE: these two functions are superseded by getaddrinfo() and
// getnameinfo()! In particular, gethostbyname() doesn't work well with IPv6.
// */
//
// #include <string>
// #include <iostream>
//
// using namespace std;
//
// class HostInfo {
// public:
//     HostInfo();
//     std::string hostname;
//     std::string addr;
// };

// HostInfo::HostInfo(){
//     char hostbuffer[256];
//     char *IPbuffer;
//     struct hostent *host_entry;
//
//     // To retrieve hostname
//     int err = gethostname(hostbuffer, sizeof(hostbuffer));
//     if (err == -1) cout << "hostname error" << endl;
//     hostname = hostbuffer;
//
//     // To retrieve host information
//     host_entry = gethostbyname(hostbuffer);
//     if (host_entry == NULL) cout << "gethostbyname() error" << endl;
//
//     // To convert an Internet network
//     // address into ASCII string
//     addr = inet_ntoa(*((struct in_addr*) host_entry->h_addr_list[0]));
//     if (addr.empty()) cout << "IP address error" << endl;
// }

#include "network.hpp"
#include <iostream>

using namespace std;


int main(){
    HostInfo h = HostInfo();
    cout << h.hostname << " [" << h.addr << "]" << endl;
    return 0;
}
