#pragma once

class SigCapture {
public:
    SigCapture();
    static void my_handler(int s);
    // bool ok(){return ok;}

protected:
    static bool ok;
};
