#ifndef STATE_H
#define STATE_H

#include <string>

class FSM; 

class State {
public:
    virtual ~State() = default;
    virtual void handle(FSM* fsm) = 0;
    virtual std::string getName() const = 0;
};

#endif 
