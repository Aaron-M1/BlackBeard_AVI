Front end started

Going to start testing about PySide6 which is the Qt designer compiler that converts that .ui file into executable code
SEPERATE LOGIC FROM UI OR UPDATES WILL DELETE WORK1!!!!111!1!1!!

Variable definitions:
unit_state = "safe" # defined statuses from BPL reqs.
code_state = "idle" # extraneous status layers for inter-communicative code operations (idle / active / actor)
    ↑ idle = telemetry on pause, no need to constantly send updates as no firing is going on
    ↑ active = telemetry active, high data transfer between front and back is on-going
    ↑ actor = pretend telemetry state simulating a rocket burn (requires simulating a mock test fire)