
#pragma once
#include <string>

class pressure_transducer {
    public:
        pressure_transducer(int pin);
        double get_pressure();

    private:
        int sensorPin;
        double sensor_value;
};