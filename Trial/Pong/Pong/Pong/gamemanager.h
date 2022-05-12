#pragma once
#include <windows.h>

#include <iostream>

#include "Ball.h"
#include "Paddle.h"

class gamemanager {
public:
    gamemanager(int w, int h) {
        srand(time(NULL));
        quit = false;
        up1 = 'w';
        up2 = 'i';
        down1 = 's';
        down2 = 'k';
        score1 = score2 = 0;
        width = w;
        height = h;
        ball = new cBall(w / 2, h / 2);
        p1 = new paddle(1, h / 2 - 3);
        p2 = new paddle(w - 2, h / 2 - 3);
    }
    ~gamemanager() {
        delete ball, p1, p2;
    }
    void scoreup(paddle* player) {
        if (player == p1) score1++;
        if (player == p2) score2++;
        ball->reset();
        p1->reset();
        p2->reset();
    }
    void ClearScreen() {
        COORD cursorPosition;
        cursorPosition.X = 0;
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), cursorPosition);
    }

    void draw() {
        ClearScreen();
        for (int i = 0; i < width + 2; ++i) std::cout << "\xB2" << std::endl;
        for (int i = 0; i < width; ++i) {
            for (int j = 0; j < height; ++j) {
                int ballx = ball->getx();
                int bally = ball->gety();
                int player1x = p1->getx();
                int player1y = p1->gety();
                int player2x = p2->getx();
                int player2y = p2->gety();
                if (i == 0) std::cout << "\xB2" << std::endl;
                if (ballx == i && bally == j)
                    std::cout << "O" << std::endl;
                else if (player1x == i && player1y == j)
                    std::cout << "\xDB" << std::endl;
                else if (player1x == i && player1y + 1 == j)
                    std::cout << "\xDB" << std::endl;
                else if (player1x == i && player1y + 2 == j)
                    std::cout << "\xDB" << std::endl;
                else if (player1x == i && player1y + 3 == j)
                    std::cout << "\xDB" << std::endl;
                else if (player2x == i && player2y == j)
                    std::cout << "\xDB" << std::endl;
                else if (player2x == i && player2y + 1 == j)
                    std::cout << "\xDB" << std::endl;
                else if (player2x == i && player2y + 2 == j)
                    std::cout << "\xDB" << std::endl;
                else if (player2x == i && player2y + 3 == j)
                    std::cout << "\xDB" << std::endl;
                else
                    std::cout << " " << std::endl;
                if (i == width - 1) std::cout << "\xB2" << std::endl;
            }
        }
        for (int i = 0; i < width + 2; ++i) std::cout << "\xB2" << std::endl;
        std::cout << "Score 1: " << score1 << std::endl;
        std::cout << "Score 2: " << score2 << std::endl;
    }

private:
    int width, height, score1, score2;
    bool quit;
    char up1, up2, down1, down2;
    cBall* ball;
    paddle* p1;
    paddle* p2;
};