#ifndef FSM_H
#define FSM_H

#include "State.h"

class FSM {
    public:
        virtual ~FSM() {}
    
        virtual void initState(State* state) = 0;
        virtual void updateState() = 0;
        virtual void changeState(State* newState) = 0;
        virtual std::string getStateName() const = 0;
    
    protected:
        State* currentState;
        State* nextState;
};

class QueueFSM : public FSM {
    public:
        QueueFSM();
        ~QueueFSM();
    
        void initState(State* state) override;
        void updateState() override;
        void changeState(State* newState) override;
        std::string getStateName() const override;
    
    private:
        // Specific data members for QueueFSM if needed
};

class MainFSM : public FSM {
    public:
        MainFSM();
        ~MainFSM();
    
        void initState(State* state) override;
        void updateState() override;
        void changeState(State* newState) override;
        std::string getStateName() const override;
    
    private:
        // Specific data members for MainFSM if needed
};

#endif 
