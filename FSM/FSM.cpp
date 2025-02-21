#include "FSM.h"
#include <iostream>

MainFSM::MainFSM() {
    currentState = nullptr;
    nextState = nullptr;
}

MainFSM::~MainFSM() {
    // Cleanup resources if needed
}

void MainFSM::initState(State* state) {
    currentState = state;
}

void MainFSM::updateState() {
    if (nextState != nullptr) {
        currentState = nextState;
        nextState = nullptr;
    }

    // Call update on the current state
    if (currentState != nullptr) {
        currentState->update();
    }
}

void MainFSM::changeState(State* newState) {
    nextState = newState;
}

std::string MainFSM::getStateName() const {
    return currentState ? currentState->getName() : "No State";
}