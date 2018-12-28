#include "signals.hpp"

#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <iostream>

/*
kevin@Logan build $ kill -l
 1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL
 5) SIGTRAP	 6) SIGABRT	 7) SIGEMT	 8) SIGFPE
 9) SIGKILL	10) SIGBUS	11) SIGSEGV	12) SIGSYS
13) SIGPIPE	14) SIGALRM	15) SIGTERM	16) SIGURG
17) SIGSTOP	18) SIGTSTP	19) SIGCONT	20) SIGCHLD
21) SIGTTIN	22) SIGTTOU	23) SIGIO	24) SIGXCPU
25) SIGXFSZ	26) SIGVTALRM	27) SIGPROF	28) SIGWINCH
29) SIGINFO	30) SIGUSR1	31) SIGUSR2
*/

using namespace std;

bool SigCapture::ok = true;

SigCapture::SigCapture(){
    struct sigaction sigIntHandler;
    // sigIntHandler.sa_handler = SigCapture::my_handler;
    // auto fp = std::bind(&SigCapture::my_handler, *this, std::placeholders::_1);
    // sigIntHandler.sa_handler = fp;

    // sigIntHandler.sa_handler = static_cast<void (*)(int)> (&SigCapture::my_handler);

    sigIntHandler.sa_handler = SigCapture::my_handler;
    sigemptyset(&sigIntHandler.sa_mask);
    sigIntHandler.sa_flags = 0;

    sigaction(SIGINT, &sigIntHandler, NULL);
}

void SigCapture::my_handler(int s){
    // printf("Caught signal %d\n",s);
    cout << " [signal caught: " << s << "] ";
    ok = false;
    // exit(1);
}

void SigCapture::shutdown(){
    ok = false;
}

bool SigCapture::isOk(){
    return ok;
}
