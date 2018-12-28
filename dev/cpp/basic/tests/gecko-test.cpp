#include "gecko.hpp"
#include <string>
#include <iostream>
using namespace std;


int main(int argc, char* argv[]){
    gecko::init(argc, argv);

    string s("hi");
    cout << "main" << endl;
    // gecko::loginfo(s);

    return 0;
}
