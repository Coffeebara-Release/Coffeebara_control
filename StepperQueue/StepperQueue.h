#ifndef STEPPERQUEUE_H
#define STEPPERQUEUE_H

class StepperQueue{
    public:
        StepperQueue(int DIR, int ENA, int PUL, int microdelay);

        void forward();
        void backward();
        void stop();

    private:
        int DIR;
        int ENA;
        int PUL;
        int microdelay;

};

#endif