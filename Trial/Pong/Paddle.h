#pragma once

#include <iostream>

class paddle {
   public:
    paddle() { x = y = 0; }
    paddle(int posx, int posy) {
        origx = posx;
        origy = posy;
        x = posx;
        y = posy;
    }
    inline void reset() {
        x = origx;
        y = origy;
    }
    inline int getx() { return x; }
    inline int gety() { return y; }
    inline void moveup() { y--; }
    inline void movedown() { y++; }

    friend std::ostream& operator<<(std::ostream& o, paddle c) {
        o << "Paddle [" << c.x << "," << c.y << "]" << std::endl;
        return o;
    }

   private:
    int x, y;
    int origx, origy;
};