#include "State.h"
#include "FSM.h"
#include <iostream>

class IdleState : public State {
public:
    void handle(FSM* fsm) override {
        std::cout << "[IdleState] 처리 중... 상태 변경: RunningState" << std::endl;
        fsm->changeState(new RunningState());
    }
    std::string getName() const override { return "IdleState"; }
};

class RunningState : public State {
public:
    void handle(FSM* fsm) override {
        std::cout << "[RunningState] 처리 중... 상태 변경: IdleState" << std::endl;
        fsm->changeState(new IdleState());
    }
    std::string getName() const override { return "RunningState"; }
};
