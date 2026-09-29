# ifndef pid_data
# define pid_data

/*-------------------------------------------------------
@BPL-2, Avionics
This is the p&id data file
Contains variables for valves, tanks, and sensors
See P&ID.jpeg in drive for more info
----------------------------------------------------------*/

class pid_data {

    private:

        //GLOBAL INITIALIZE
        std::string Status = "Safe"; // 
        bool Interlock = true; //Only becomes false when in firing mode and ready to launch

        //VALVE BOOLEANS
        bool gcv_open = false; // GN2 Check Valve
        bool gpr_open = false; // GN2 Pressure Regulator
        bool gbp_open = false; //GN2 Back Pressurizing Solenoid
        bool fps_open = false; //Fuel Purging Solenoid
        bool fmv_open = false; //Fuel Main Valve
        bool fcv_open = false; //Fuel Check Valve
        bool omv_open = false; //Oxidizer Main Valve
        bool ocv_open = false; //Oxidizer Check Valve
        bool ccv_open = false; //Chiller Check Valve
        bool orips_open = false; //Oxidizer Run Tank Purge Solenoid
        bool cps_open = false; //Chiller Purge Solenoid
        bool cms_open = false; //Chiller Main Solenoid

        //TANK VOLUMES
        double ksi_gallons = 0.0000; // 2Ksi tank fill in gallons
        double ert_gallons = 0.0000; // Ethanol Run tank fill in gallons
        double n_run_gallons = 0.0000; // N20 run tank fill in gallons
        double n_kbottle_gallons = 0.0000; // N20 K-Bottle tank fill in gallons

        //CHECK-ALERT SYSTEMS
        bool ksi_online = false; //If true: KSI Sensors not obtaining readings
        bool ert_online = false; //If true: ERT Sensors not obtaining readings
        bool n_run_online = false; //If true: N20RUN Sensors not obtaining readings
        bool n_kbottle_online = false; //If true: N20KBOT Sensors not obtaining readings
    public:



};
#endif