#include <iostream>
# ifndef m_data
# define m_data

class m_data {

    private:
    
        //Trip = boolvalue or status that activates an alarm or a unsafe condition alert (eg. low pressure trip, leak trip)

        //-GLOBAL INITIALIZE-//
        string Status = "Safe"; // 
        bool Interlock = true; //Only becomes false when in firing mode and ready to launch

        // GN2 Check Valve
        bool gcv_open = false;

        bool gpr_open = false;  // GN2 Pressure Regulator

        bool gbp_open = false; //GN2 Back Pressurizing Solenoid

        double fps_open = false; //Fuel Purging Solenoid
        double fmv_open = false; //Fuel Main Valve
        double fcv_open = false; //Fuel Check Valve
        double omv_open = 0.00; //Oxidizer Main Valve
        double ocv_open = false; //Oxidizer Check Valve
        double ccv_open = false; //Chiller Check Valve
        double orips_open = false; //Oxidizer Run Tank Purge Solenoid
        double cps_open = false; //Chiller Purge Solenoid
        double cms_open = false; //Chiller Main Solenoid

        double ksi_gallons = 0.0000; // 2Ksi tank fill in gallons
        double ert_gallons = 0.0000; // Ethanol Run tank fill in gallons
        double n_run_gallons = 0.0000; // N20 run tank fill in gallons
        double n_kbottle_gallons = 0.0000; // N20 K-Bottle tank fill in gallons

        //-TRIPS-//
        bool ksi_online = false; //If true: KSI Sensors not obtaining readings
        bool ert_online = false; //If true: ERT Sensors not obtaining readings
        bool n_run_online = false; //If true: N20RUN Sensors not obtaining readings
        bool n_kbottle_online = false; //If true: N20KBOT Sensors not obtaining readings
    public:

};
#endif