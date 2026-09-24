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

GCV = 0.00 # GN2 Check Valve
GPR = 0.00 #GN2 Pressure Regulator
GBS = 0.00 #GN2 Back Pressurizing Solenoid
GPRV = 0.00 #GN2 Pressure Relief Valve
FPS = 0.00 #Fuel Purging Solenoid
FMV = 0.00 #Fuel Main Valve
FCV = 0.00 #Fuel Check Valve
OMV = 0.00 #Oxidizer Main Valve
OCV = 0.00 #Oxidizer Check Valve
CCV = 0.00 #Chiller Check Valve
ORIPS = 0.00 #Oxidizer Run Tank Purge Solenoid
CPS = 0.00 #Chiller Purge Solenoid
CMS = 0.00 #Chiller Main Solenoid

Ksi_2GAL = 0.0000 # 2Ksi tank fill in gallons
ERT = 0.0000 # Ethanol Run tank fill in gallons
N20RUN = 0.0000 # N20 run tank fill in gallons
N20KBOT = 0.0000 # N20 K-Bottle tank fill in gallons