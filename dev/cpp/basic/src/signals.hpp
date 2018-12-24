#pragma once

class SigCapture {
public:
    SigCapture();
    static void my_handler(int s);

protected:
    static bool ok;
};
