#██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ ██████╗     ███████╗██████╗  ██████╗ ███╗   ██╗████████╗
#██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
#██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝█████╗  ███████║██████╔╝██║  ██║    █████╗  ██████╔╝██║   ██║██╔██╗ ██║   ██║   
#██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██╔══╝  ██╔══██║██╔══██╗██║  ██║    ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║   ██║   
#██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝███████╗██║  ██║██║  ██║██████╔╝    ██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║   
#╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   

# 𝔅𝔩𝔦𝔫𝔫 𝔓𝔯𝔬𝔭𝔲𝔩𝔰𝔦𝔬𝔫 𝔏𝔞𝔟𝔬𝔯𝔞𝔱𝔬𝔯𝔦𝔢𝔰
# V1.00.00  :  9/29/2026     

# # Everett mitchell was caught playing mario kart wii in the student center at 9/30/2026 at 9:29 AM                                                                                                                           

# Standard Libraries (No installation required)
import math
import mailbox
import os
import random
import sys
import time
import ctypes  # C Foreign Function Interface for loading C DLLs/shared objects
from datetime import datetime

# # Third-party packages (Install via: pip install numpy cffi pyserial)
# import numpy as np  # Fast numerical computation and array handling
# import cffi         # C Foreign Function Interface (alternative to ctypes)
# import serial       # Serial communication library (installed as pyserial)

from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget, QCheckBox, QDialog, QButtonGroup, QToolButton, QListView,)

#//--DEBUG / EXPERIMENTS--// [WARNING! IF ANY EXPERIMENT IS ON, THE ENGINE CANNOT FIRE!]
program_debug = True
test_express_Experiment = False # Creates mock log files
Config_Party_Experiment = False # Config file playground
SetUp_Experiment = False # More for utility, adds the proper logging directory to your device (make true → run program → make false)

# Triggers Time Start
PROGRAM_START = time.perf_counter()

#//--Valves--//
gc_check = False # GN2 Check Valve
gb_solenoid = False #GN2 Back Pressurizing Solenoid
fuel_purge = False #Fuel Purging Solenoid
fuel_main = False #Fuel Main Valve
ox_main = False #Oxidizer Main Valve
ORIPS = False #Oxidizer Run Tank Purge Solenoid
CPS = False #Chiller Purge Solenoid
CMS = False #Chiller Main Solenoid

#//--Press & Thermo--//
gpressure_press = 0.00
k_bottle_press = 0.00
chiller_press = 0.00
e_run_press = 0.00
n2o_press = 0.00
Fuel_c_press = 0.00
Oxi_c_press = 0.00
n2o_temp = 0.00

#//--DatRets --//
lcell_a = 0.00
lcell_b = 0.00
lcell_c = 0.00

#//--Local Vars--//
runlogs = False
kstart = False
unit_state = "safe" # defined statuses from BPL reqs.
code_state = "idle" # extraneous status layers for inter-communicative code operations (idle / active / actor)
ll_template = {"T":0, "A":"Action here"}
local_logs = [] # 

def time_thread(tstype):
    tst = tstype.lower()

    if tst == 'runtime':
        # Elapsed time since program start: MM:SS:mmm:uuu
        elapsed_us = int((time.perf_counter() - PROGRAM_START) * 1_000_000)
        minutes, rem = divmod(elapsed_us, 60_000_000)
        seconds, rem = divmod(rem, 1_000_000)
        millis, micros = divmod(rem, 1_000)
        return f"{minutes:02d}:{seconds:02d}:{millis:03d}:{micros:03d}"

    now = datetime.now()
    if tst == 'full':
        return now.strftime('%Y-%m-%d_%H-%M-%S')
    elif tst == 'mini':
        return now.strftime('%S.%f')[:-3]
    else:
        return now.strftime('%H:%M:%S')

def CreateLog():
    totals = 0
    timestamp = time_thread('full')
    filepath = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop', 'BlackBeard_Logs', f'{timestamp}.txt')
    dir_path = os.path.dirname(filepath)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(filepath, "a") as f: #compile local logs
        f.write(timestamp)
        f.write("\nThis is a new log entry. May the wind guide your hand\n\n")
        for entry in local_logs:
            totals += 1
            f.write(f"[{totals}] {entry}\n")
        pass

def iSend(itype, com1, com2, com3, com4): # C++ Communicator Function
    if program_debug == True: print(itype, com1, com2, com3, com4)

def init():
    global gc_check, gb_solenoid, fuel_purge, fuel_main, ox_main
    global ORIPS, CPS, CMS, runlogs
    gc_check = gb_solenoid = fuel_purge = fuel_main = False
    ox_main = ORIPS = CPS = CMS = False
    runlogs = True

    #opens experiments
    if test_express_Experiment == True: test_express()
    if SetUp_Experiment == True: CreateLog()

def local_State(pa_un_State, pa_co_State, pre_req):
    unit_state = str.lower(pa_un_State)
    code_state = str.lower(code_state)
    # Negligable backend logic under conversion
    # if unit_state == "safe":
    #     if pre_req == None: return 
    #     else: 
    #         iSend("state_recieve", unit_state)
    # if unit_state == "firing":
    #     iSend("state_recieve", unit_state)
    #     kstart = True
        
def test_express(): #like chicken express but for testing
    testlimit = 5000
    waits = 0.02
    period = 1
    for i in range(testlimit):
        # Generates a random integer from 1 to 15 (inclusive)
        gen = random.random()*25
        ncop = ll_template.copy()
        ncop["T"] = time_thread('runtime')
        ncop["A"] = gen
        local_logs.append(ncop)
        # Pass ncop to your log function if required
        time.sleep(random.random()/(3*period))
        print(f"Working... ({i+1}/{testlimit})")
        period /= 0.95
    CreateLog()
    
init() # comes last to establish all variables and functions before init