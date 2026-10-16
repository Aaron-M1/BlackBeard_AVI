
#pragma once
#include <string>
#include <cstdint>
/*-------------------------------------------------------
@BPL-2, Avionics
This is the p&id data file
Contains variables for valves, tanks, and sensors
See P&ID.jpeg in drive for more info
----------------------------------------------------------*/

class solenoid {
    public:
        solenoid(uint8_t pin, bool default_state);
        ~solenoid(void);

        void togglesolenoid();
        void setState(bool state);
        uint8_t getPin();
    
    private:
        bool isOpen;
        bool defaultState;
        const uint8_t solenoidPin;


};