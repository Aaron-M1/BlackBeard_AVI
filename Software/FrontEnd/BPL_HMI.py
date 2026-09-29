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

#///- INIT VARIABLES -///

# 0 - 100 open percentage
# %34.55 = 0.3455

#assign these I think
PacketSend = [
    ["GCV",0.00],
    ["GPR",0.00],
    ["GBS",0.00],
    ["GPRV",0.00],
    ["FPS",0.00],
    ["FMV",0.00],
    ["FCV",0.00],
    ["OMV",0.00],
    ["OCV",0.00],
    ["CCV",0.00],
    ["ORIPS",0.00],
    ["CPS",0.00],
    ["CMS",0.00],
]

# True is Open / False is Close

gc_check = False # GN2 Check Valve
gb_solenoid = False #GN2 Back Pressurizing Solenoid
fuel_purge = False #Fuel Purging Solenoid
fuel_main = False #Fuel Main Valve
ox_main = False #Oxidizer Main Valve
ORIPS = False #Oxidizer Run Tank Purge Solenoid
CPS = False #Chiller Purge Solenoid
CMS = False #Chiller Main Solenoix 

p1 = 0.00 # NEEDS DEFINING
p2 = 0.00 # NEEDS DEFINING
p3 = 0.00 # NEEDS DEFINING
p4 = 0.00 # NEEDS DEFINING
p5 = 0.00 # NEEDS DEFINING
p6 = 0.00 # NEEDS DEFINING
p7 = 0.00 # NEEDS DEFINING

Ksi_2GAL = 0.0000 # 2Ksi tank fill in Liters
ERT = 0.0000 # Ethanol Run tank fill in Liters
N20RUN = 0.0000 # N20 run tank fill in Liters
N20KBOT = 0.0000 # N20 K-Bottle tank fill in Liters



print()