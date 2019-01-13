// C
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
// #include <unistd.h> // for sleep()
#include <stdio.h>
#include <stdlib.h>

// C++
// #include <chrono>
#include <string>
#include <iostream>

#include "mbeacon.hpp"
#include "time.hpp"


using namespace std;


Beacon::Beacon(string grp): group(grp), port(1900), MSGBUFSIZE(255) {}

int Beacon::initSocket(bool reuse){

    // create what looks like an ordinary UDP socket
    fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) {
        perror("Beacon::initSocket");
        return 1;
    }

    // allow multiple sockets to use the same PORT number
    if (reuse){
        u_int yes = 1;
        int err = setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, (char*) &yes, sizeof(yes));
        if (err < 0){
           perror("Reusing ADDR failed");
           return 1;
        }
    }

    // set up destination address
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(group.c_str());
    addr.sin_port = htons(port);

    return 0;
}

bool Beacon::send(string message){
    int nbytes = sendto(
        fd,
        message.c_str(),
        message.size(),
        0,
        (struct sockaddr*) &addr,
        sizeof(addr)
    );
    if (nbytes < 0) return true;
    return false;
}

bool Beacon::ready(int usec){
    struct timeval tv;
    fd_set readfds;
    int err;

    tv.tv_sec = 0;
    tv.tv_usec = usec;

    FD_ZERO(&readfds);
    FD_SET(fd, &readfds);
    // FD_SET(0, &readfds);  // standard in

    // don't care about writefds and exceptfds:
    err = select(fd+1, &readfds, NULL, NULL, &tv);
    if (err < 0) cout << "** select issue: " << err << endl;

    if (FD_ISSET(fd, &readfds)) return true;
    // else if (FD_ISSET(0, &readfds)) {
    //     cout << "key" << endl;
    //     return false;
    // }
    else return false;
}

bool Beacon::recv(string& msg){
    char msgbuf[MSGBUFSIZE];
    socklen_t addrlen = sizeof(addr);
    int nbytes = recvfrom(
        fd,
        msgbuf,
        MSGBUFSIZE,
        0,
        (struct sockaddr *) &addr,
        &addrlen
    );
    if (nbytes < 0) return true;

    msgbuf[nbytes] = '\0';
    msg = msgbuf;

    return false;
}

void Beacon::print(string kind){
    // cout << kind << "----------------------------------" << endl;
    // cout << " addr: " << group << endl;
    // cout << " port: " << to_string(port) << endl;
    // cout << "   fd: " << to_string(fd) << endl;
    printf(
        "%-8s ------------------------------- \n"
        " addr: %s \n"
        " port: %d \n"
        "   fd: %d \n", kind.c_str(), group.c_str(), port, fd);
}



Listener::Listener(): Beacon("239.255.255.250"){
    Beacon::initSocket(true);
    Beacon::print("Listener");
    // cout << "Listener [" << group << ":" << to_string(port) << "]";
    // cout << " fd: " << to_string(fd) << endl;
}

int Listener::listen(){

    // bind to all interfaces to receive address
    struct sockaddr_in aaddr;
    memset(&aaddr, 0, sizeof(aaddr));
    aaddr.sin_family = AF_INET;
    aaddr.sin_addr.s_addr = inet_addr("0.0.0.0"); // need to send response back
    aaddr.sin_port = htons(port);
    if (::bind(fd, (struct sockaddr*) &aaddr, sizeof(aaddr)) < 0) {
        perror("Listener::listen() --> bind");
        return 1;
    }

    // use setsockopt() to request that the kernel join a multicast group
    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr = inet_addr(group.c_str());
    mreq.imr_interface.s_addr = htonl(INADDR_ANY);
    int err = setsockopt(fd, IPPROTO_IP, IP_ADD_MEMBERSHIP, (char*) &mreq, sizeof(mreq));
    if (err < 0){
        perror("Listener::listen() --> setsockopt");
        return 1;
    }

    // now just enter a read-print loop
    while (1) {
        string msg;
        bool err = Beacon::recv(msg);
        if (err) perror("Listener::listen --> recv");
        // else cout << "listener: "<< msg << endl;

        // if (msg == "kevin") break;
        if (msg == "kevin") {
            cout << ">> listener sees good message " << endl;
            err = Beacon::send("walchko");
            if (err) perror("Listener::listen -> walchko");
        }
    }

    return 0;
}


Search::Search(): Beacon("239.255.255.250"){
    Beacon::initSocket(false);
    Beacon::print("Search");
    // sleep(1); // give listener time to spin up
}

string Search::find(string message){
    // string message = "kevin";
    string ans;
    // std::cout << "find" << std::endl;
    for(int cnt = 50; cnt > 0; --cnt) {
        bool err = Beacon::send("kevin");
        if (err) perror("Search::find");
        // else cout << "> ping: " << message << endl;

        bool data = Beacon::ready(1000);

        if (data){
            err = Beacon::recv(ans);
            if (err) perror("Search::find -> recv");
            else cout << ">> search got answer: " << ans << endl;
            break;
        }
        // else cout << "*** data lost ***" << endl;
        // usleep(100000);
        Time::msleep(100);
    }
    return ans;
}
