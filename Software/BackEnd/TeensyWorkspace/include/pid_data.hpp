
#pragma once
#include <string>


/*-------------------------------------------------------
@BPL-2, Avionics
This is the p&id data file
Contains variables for valves, tanks, and sensors
See P&ID.jpeg in drive for more info
----------------------------------------------------------*/

class pid_data {

    public:
        pid_data(void);
        ~pid_data(void);


        //SETTERS
        void setStatus(const std::string& status_input);
        void setInterlock(bool interlock);

        void setGCV(bool is_open);
        void setGPR(bool is_open);
        void setGBP(bool is_open);
        void setFPS(bool is_open);
        void setFMV(bool is_open);
        void setFCV(bool is_open);
        void setOMV(bool is_open);
        void setOCV(bool is_open);
        void setCCV(bool is_open);
        void setORIPS(bool is_open);
        void setCPS(bool is_open);
        void setCMS(bool is_open);

        void setPressure1(double pressure);
        void setPressure2(double pressure);
        void setPressure3(double pressure);
        void setPressure4(double pressure);
        void setPressure5(double pressure);
        void setPressure6(double pressure);
        void setPressure7(double pressure);

        void setNThermocouple(double temperature);

        void setKSIVolume(double volume);
        void setERTVolume(double volume);
        void setNRunVolume(double volume);
        void setNKBottleVolume(double volume);

        void setKSIOnline(bool is_online);
        void setERTOnline(bool is_online);
        void setNRunOnline(bool is_online);
        void setNKBottleOnline(bool is_online);


        //GETTERS
        std::string getStatus();
        bool getInterlock();

        bool getGCV();
        bool getGPR();
        bool getGBP();
        bool getFPS();
        bool getFMV();
        bool getFCV();
        bool getOMV();
        bool getOCV();
        bool getCCV();
        bool getORIPS();
        bool getCPS();
        bool getCMS();

        double getPressure1();
        double getPressure2();
        double getPressure3();
        double getPressure4();
        double getPressure5();
        double getPressure6();
        double getPressure7();

        double getNThermocouple();

        double getKSIVolume();
        double getERTVolume();
        double getNRunVolume();
        double getNKBottleVolume();

        bool getKSIOnline();
        bool getERTOnline();
        bool getNRunOnline();
        bool getNKBottleOnline();
    private:
        //GLOBAL INITIALIZE
        std::string status;
        bool Interlock; //Only becomes false when in firing mode and ready to launch

        //VALVE BOOLEANS
        bool gcv_open; // GN2 Check Valve
        bool gpr_open; // GN2 Pressure Regulator
        bool gbp_open; //GN2 Back Pressurizing Solenoid
        bool fps_open; //Fuel Purging Solenoid
        bool fmv_open; //Fuel Main Valve
        bool fcv_open; //Fuel Check Valve
        bool omv_open; //Oxidizer Main Valve
        bool ocv_open; //Oxidizer Check Valve
        bool ccv_open; //Chiller Check Valve
        bool orips_open; //Oxidizer Run Tank Purge Solenoid
        bool cps_open; //Chiller Purge Solenoid
        bool cms_open; //Chiller Main Solenoid

        //PRESSURE TRANDUCER VALUES
        double pressure_1; //TODO: Figure out what valves pressure is being read from
        double pressure_2; //TODO: Figure out what valves pressure is being read from
        double pressure_3; //TODO: Figure out what valves pressure is being read from
        double pressure_4; //TODO: Figure out what valves pressure is being read from
        double pressure_5; //TODO: Figure out what valves pressure is being read from
        double pressure_6; //TODO: Figure out what valves pressure is being read from
        double pressure_7; //TODO: Figure out what valves pressure is being read from

        //THERMOCOUPLE VALUES
        double n_thermocouple; //Temperature from N20 run tank

        //TANK VOLUMES
        double ksi_volume; // 2Ksi tank fill in gallons or liters
        double ert_volume; // Ethanol Run tank fill in gallons or liters
        double n_run_volume; // N20 run tank fill in gallons or liters
        double n_kbottle_volume; // N20 K-Bottle tank fill in gallons or liters

        //CHECK-ALERT SYSTEMS
        bool ksi_online; //If true: KSI Sensors not obtaining readings
        bool ert_online; //If true: ERT Sensors not obtaining readings
        bool n_run_online; //If true: N20RUN Sensors not obtaining readings
        bool n_kbottle_online; //If true: N20KBOT Sensors not obtaining readings

};
