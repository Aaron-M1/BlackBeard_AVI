#██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ ██████╗     ███████╗██████╗  ██████╗ ███╗   ██╗████████╗
#██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
#██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝█████╗  ███████║██████╔╝██║  ██║    █████╗  ██████╔╝██║   ██║██╔██╗ ██║   ██║   
#██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██╔══╝  ██╔══██║██╔══██╗██║  ██║    ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║   ██║   
#██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝███████╗██║  ██║██║  ██║██████╔╝    ██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║   
#╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   

# 𝔅𝔩𝔦𝔫𝔫 𝔓𝔯𝔬𝔭𝔲𝔩𝔰𝔦𝔬𝔫 𝔏𝔞𝔟𝔬𝔯𝔞𝔱𝔬𝔯𝔦𝔢𝔰
# V1.00.00  :  9/29/2026     

# # Everett mitchell was caught playing mario kart wii in the student center at 9/30/2026 at 9:29 AM                                                                                                                           

import math
import mailbox
import random
import sys
import ctypes #c++ library and calls
import numpy as np #c++ foriegn function interface
import cffi #c++ array passing
import serial

from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget, QCheckBox, QDialog, QButtonGroup, QToolButton, QListView,)

#//--ENABLE DEBUG--//
program_debug = True

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

#//--Local Vars--//
unit_state = "safe" # defined statuses from BPL reqs.
code_state = "idle" # extraneous status layers for inter-communicative code operations (idle / active / actor)

def iSend(itype, com1, com2, com3, com4): # C++ Communicator Function
    if program_debug == True: print(itype, com1, com2, com3, com4)

def init():
    gc_check = False # GN2 Check Valve
    gb_solenoid = False #GN2 Back Pressurizing Solenoid
    fuel_purge = False #Fuel Purging Solenoid
    fuel_main = False #Fuel Main Valve
    ox_main = False #Oxidizer Main Valve
    ORIPS = False #Oxidizer Run Tank Purge Solenoid
    CPS = False #Chiller Purge Solenoid
    CMS = False #Chiller Main Solenoid
    if program_debug: print("Initalizing run pass"); 

init()

def local_State(pa_un_State, pa_co_State, pre_req):
    unit_state = str.lower(pa_un_State)
    code_state = str.lower(code_state)
    if unit_state == "safe":
        if pre_req == None: return 
        else: 
            iSend("state_recieve", "safe")
        
        