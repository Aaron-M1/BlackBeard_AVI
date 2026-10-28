
#pragma once

/*-------------------------------------------------------
@BPL-2, Avionics
This is the pressure transducer header file
Contains variables and functions for the pressure transducer
----------------------------------------------------------*/

class pressure_transducer {
    public:
        pressure_transducer(int pin);
        double get_pressure();

    private:
        int sensorPin;
        double sensor_value;
};