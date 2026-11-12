
#pragma once
#include <string>


/*-------------------------------------------------------
@BPL-2, Avionics
This is the p&id header file
Contains variables for valves, tanks, and sensors
See P&ID.jpeg in drive for more info
----------------------------------------------------------*/

class pid_data {

    public:
        pid_data(void);
        ~pid_data(void);


        //SETTERS
        void setNPS(bool is_open);
        void setGPS(bool is_open);
        void setFMV(bool is_open);
        void setOMV(bool is_open);
        void setOPS(bool is_open);


        void setPressure1(double pressure);
        void setPressure2(double pressure);
        void setPressure3(double pressure);
        void setPressure4(double pressure);
        void setPressure5(double pressure);



        //GETTERS
        bool getNPS();
        bool getOPS();
        bool getGPS();
        bool getFMV();
        bool getOMV();

        double getPressure1();
        double getPressure2();
        double getPressure3();
        double getPressure4();
        double getPressure5();
    private:
        //VALVE BOOLEANS
        bool nps_open; //Nitrous Propellant Solenoid
        bool ops_open; //Oxidizer Propellant Solenoid
        bool gps_open; //Gas Propellant Solenoid
        bool fmv_open; //Fuel Main Valve
        bool omv_open; //Oxidizer Main Valve

        //PRESSURE TRANDUCER VALUES
        double pressure_1; //TODO: Figure out what valves pressure is being read from
        double pressure_2; //TODO: Figure out what valves pressure is being read from
        double pressure_3; //TODO: Figure out what valves pressure is being read from
        double pressure_4; //TODO: Figure out what valves pressure is being read from
        double pressure_5; //TODO: Figure out what valves pressure is being read from
};
