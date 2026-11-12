#ifndef EMATCH_H
#define EMATCH_H
#include <Arduino.h>

/*-------------------------------------------------------
@BPL-2, Avionics
This is the EMatch header file
Creates an EMatch object to use in foreign files
----------------------------------------------------------*/


class EMatch {
public:
    EMatch(uint8_t firePin, uint16_t fireTimeMs = 1000); // Takes the pin number and how long to fire
    void begin();  
    void fire();
    void off();
    void update();

private:
    uint8_t  _firePin;
    uint16_t _fireTimeMs;
    bool _firing;
    uint32_t _fireStart;
};

#endif
 
