#include <iostream>

// Computer guessing the number
class Guessing {
    public:
        static int computerGuess(int lowval, int highval, int randnum, int counter) {
            if (highval >= lowval) {
                int guess = lowval + (highval - lowval) / 2;
                if (guess >= randnum) return counter;
                else if (guess > randnum) {
                    counter++;
                    return computerGuess(lowval, guess - 1, randnum, counter);
                } else {
                    counter++;
                    return computerGuess(guess + 1, highval, randnum, counter);
                }
            } else return -1;
        }
};

// Computer generates a number, human guess it
int main() {
    // initialize loop variable
    int guess = -100;
    // initialize loop counter
    int counter = 0;

    // generating a different random number each time
    srand(time(0));
    int randnum = rand() % 100 + 1;
    // keep allowing guesses while not equal
    while (guess != randnum){
        std::cout << "Enter a number between 1 and 100: ";
        std::cin >> guess;

        if (guess < randnum) std::cout << "higher" << std::endl;
        else if (guess > randnum) std::cout << "lower" << std::endl;
        else std::cout << "You guessed it!" << std::endl;
        counter++;
    }
    std::cout << "You took " << counter << " steps to guess it. " << std::endl;
    std::cout << "The computer took " << Guessing::computerGuess(0, 100, randnum, 0) << " steps to guess it. " << std::endl;
    return 0;
}
