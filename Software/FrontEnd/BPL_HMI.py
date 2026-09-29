import math
import mailbox
import random
import sys
from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QDialog,
    QButtonGroup,
    QToolButton,
    QListView,
)

program_debug = True

# True is Open / False is Close

gc_check = False # GN2 Check Valve
gb_solenoid = False #GN2 Back Pressurizing Solenoid
fuel_purge = False #Fuel Purging Solenoid
fuel_main = False #Fuel Main Valve
ox_main = False #Oxidizer Main Valve
ORIPS = False #Oxidizer Run Tank Purge Solenoid
CPS = False #Chiller Purge Solenoid
CMS = False #Chiller Main Solenoix 

gpressure_press = 0.00
k_bottle_press = 0.00
chiller_press = 0.00
e_run_press = 0.00
n2o_press = 0.00
Fuel_c_press = 0.00
Oxi_c_press = 0.00
n2o_temp = 0.00

def init():
    gc_check = False # GN2 Check Valve
    gb_solenoid = False #GN2 Back Pressurizing Solenoid
    fuel_purge = False #Fuel Purging Solenoid
    fuel_main = False #Fuel Main Valve
    ox_main = False #Oxidizer Main Valve
    ORIPS = False #Oxidizer Run Tank Purge Solenoid
    CPS = False #Chiller Purge Solenoid
    CMS = False #Chiller Main Solenoix 
    if program_debug: print("Initalizing run pass"); 


print()