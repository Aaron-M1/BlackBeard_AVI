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
import socket
import threading
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
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import random
import time

# --- Global Configuration & Experiments ---
PROGRAM_DEBUG = True
PROGRAM_START = time.perf_counter()

EXPERIMENTS = {
    "Config_Party": False,
    "Test_Express": False,  # Creates mock log files
    "SetUp": False,  # Utility: creates logging directory structure
}

# --- State & Telemetry Structures ---
@dataclass
class ValveState:
    gc_check: bool = False  # GN2 Check Valve
    gb_solenoid: bool = False  # GN2 Back Pressurizing Solenoid
    fuel_purge: bool = False  # Fuel Purging Solenoid
    fuel_main: bool = False  # Fuel Main Valve
    ox_main: bool = False  # Oxidizer Main Valve
    ORIPS: bool = False  # Oxidizer Run Tank Purge Solenoid
    CPS: bool = False  # Chiller Purge Solenoid
    CMS: bool = False  # Chiller Main Solenoid
    def reset(self) -> None:
        for field in self.__dataclass_fields__:
            setattr(self, field, False)


@dataclass
class TelemetryData:
    gpressure_press: float = 0.00
    k_bottle_press: float = 0.00
    chiller_press: float = 0.00
    e_run_press: float = 0.00
    n2o_press: float = 0.00
    fuel_c_press: float = 0.00
    oxi_c_press: float = 0.00
    n2o_temp: float = 0.00
    lcell_a: float = 0.00
    lcell_b: float = 0.00
    lcell_c: float = 0.00

@dataclass
class SystemState:
    runlogs: bool = False
    kstart: bool = False
    unit_state: str = "safe"  # defined statuses from BPL reqs.
    code_state: str = (
        "idle"  # extraneous status layers (idle / active / actor)
    )

# Instantiate system components
valves = ValveState()
telemetry = TelemetryData()
state = SystemState()

local_logs: list[dict] = []

def receiver(): # Return string and figure and parse string returned from function.
    # makefile() gives line-based reads, so framing is handled for us
    for line in sock.makefile("r"):
        name, _, value = line.strip().partition(",")
        print(f"[from teensy] {name} = {float(value)}")

# --- Utility Functions ---
def time_thread(tstype: str) -> str:
    tst = tstype.lower()

    if tst == "runtime":
        elapsed_us = int((time.perf_counter() - PROGRAM_START) * 1_000_000)
        minutes, rem = divmod(elapsed_us, 60_000_000)
        seconds, rem = divmod(rem, 1_000_000)
        millis, micros = divmod(rem, 1_000)
        return f"{minutes:02d}:{seconds:02d}:{millis:03d}:{micros:03d}"

    now = datetime.now()
    if tst == "full":
        return now.strftime("%Y-%m-%d_%H-%M-%S")
    elif tst == "mini":
        return now.strftime("%S.%f")[:-3]
    return now.strftime("%H:%M:%S")

def create_log() -> Path:
    """Compiles local log entries and writes to disk."""
    timestamp = time_thread("full")
    log_dir = Path.home() / "OneDrive" / "Desktop" / "BlackBeard_Logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    filepath = log_dir / f"{timestamp}.txt"
    lines = [
        timestamp,
        "This is a new log entry. May the wind guide your hand\n",
    ]
    lines.extend(
        f"[{i + 1}] {entry}" for i, entry in enumerate(local_logs)
    )

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath

def i_send(itype: str, *args) -> None:
    if PROGRAM_DEBUG:
        print(f"[COMM] {itype}:", *args)

def local_state(
    pa_un_state: str, pa_co_state: str, pre_req: str | None = None
) -> None:
    """Updates unit and internal code state status flags."""
    state.unit_state = pa_un_state.lower()
    state.code_state = pa_co_state.lower()

    if state.unit_state == "firing":
        i_send("state_recieve", state.unit_state)
        state.kstart = True
    elif state.unit_state == "safe" and pre_req is not None:
        i_send("state_recieve", state.unit_state)


def test_express() -> None:
    test_limit = 500
    period = 1.0
    for i in range(test_limit):
        gen = random.random() * 25
        ncop = {"T": time_thread("runtime"), "A": gen}
        local_logs.append(ncop)

        # Dynamic sleep timing loop logic
        time.sleep(random.random() / (3 * period))
        print(f"Working... ({i + 1}/{test_limit})")
        period /= 0.95
    create_log()


def init():
    """Initializes rocket valve hardware and runs active experiments."""
    valves.reset()
    state.runlogs = True
    # Execute active configuration experiments
    if EXPERIMENTS.get("Test_Express"):
        test_express()
    if EXPERIMENTS.get("SetUp"):
        create_log()

# --- Execution Entry ---
if __name__ == "__main__":
    init()

"""
'data or commands'
String format:

Sensor data:

[name of sensor]:[value]

Commands:

command:[command_type]

"""