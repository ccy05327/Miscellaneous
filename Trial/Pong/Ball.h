#pragma once
#include <iostream>

enum eDir { stop = 0,
            left = 1,
            upleft = 2,
            downleft = 3,
            right = 4,
            upright = 5,
            downright = 6 };
class cBall {
   public:
    cBall(int posx, int posy) {
        origx = posx;
        origy = posy;
        x = posx;
        y = posy;
        direction = stop;
    }
    void reset() {
        x = origx;
        y = origy;
        direction = stop;
    }
    void changedir(eDir d) {
        direction = d;
    }
    void randomdir() {
        direction = (eDir)((rand() % 6) + 1);
    }
    inline int getx() { return x; }
    inline int gety() { return y; }
    inline eDir getdir() { return direction; }
    void move() {
        switch (direction) {
            case stop:
                break;
            case left:
                x--;
                break;
            case right:
                x++;
                break;
            case upleft:
                x--;
                y--;
                break;
            case downleft:
                x--;
                y++;
                break;
            case upright:
                x++;
                y--;
                break;
            case downright:
                x++;
                y++;
                break;
            default:
                break;
        }
    }
    friend std::ostream& operator<<(std::ostream& o, cBall c) {
        o << "Ball [" << c.x << "," << c.y << "][" << c.direction << "]" << std::endl;
        return o;
    }

   private:
    int x, y;
    int origx, origy;
    eDir direction;
};