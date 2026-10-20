
#pragma once
#include <string>
#include <cstdint>
/*-------------------------------------------------------
@BPL-2, Avionics
This is the solenoid header file
Creates a solenoid object to use in foreign files
----------------------------------------------------------*/

class solenoid {
    public:
        solenoid(uint8_t pin, bool default_state);
        ~solenoid(void);

        void togglesolenoid();
        void setState(bool state);

        uint8_t getPin();
        bool getState();
    
    private:
        bool isOpen;
        bool defaultState;
        uint8_t SOLENOID_PIN;


};