#include "Arduino.h"
#include "StepperQueue.h"

StepperQueue::StepperQueue(int DIR, int ENA, int PUL, int microdelay)
{
    this->DIR = DIR;
    this->ENA = ENA;
    this->PUL = PUL;
    this->microdelay;

    pinMode(ENA, OUTPUT);
    pinMode(PUL, OUTPUT);
    pinMode(DIR, OUTPUT);
}

void StepperQueue::queueForward()
{
    digitalWrite(this->DIR,LOW);
    digitalWrite(this->ENA,HIGH);
    digitalWrite(this->PUL,HIGH);
    delayMicroseconds(this->microdelay);
    digitalWrite(this->PUL,LOW);
    delayMicroseconds(this->microdelay);
}

void StepperQueue::queueBackward()
{
    digitalWrite(this->DIR,HIGH);
    digitalWrite(this->ENA,HIGH);
    digitalWrite(this->PUL,HIGH);
    delayMicroseconds(this->microdelay);
    digitalWrite(this->PUL,LOW);
    delayMicroseconds(this->microdelay);
}

void StepperQueue::queueStop()
{
    digitalWrite(this->DIR,LOW);
    digitalWrite(this->ENA,LOW);
    digitalWrite(this->PUL,LOW);
}