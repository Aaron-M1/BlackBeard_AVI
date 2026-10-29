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
from __future__ import annotations # importing the future of the universe to run entirely on your laptop...
import math
import mailbox
import os
import random
import sys
import time
import socket
import threading
import ctypes
import random
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from dataclasses import dataclass, fields
from dataclasses import dataclass
from datetime import datetime
from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget, QCheckBox, QDialog, QButtonGroup, QToolButton, QListView,)

# # Third-party packages (Install via: pip install numpy cffi pyserial)
# import numpy as np  # Fast numerical computation and array handling
# import cffi         # C Foreign Function Interface (alternative to ctypes)
# import serial       # Serial communication library (installed as pyserial)

# --- Global Configuration & Experiments ---
PROGRAM_DEBUG = True
PROGRAM_START = time.perf_counter()

# ========== define directory =============
BASE_DIR = Path.home() / "Desktop" / "Blinn Propulsion Labs"

#//--DEBUG / EXPERIMENTS--// [WARNING! IF ANY EXPERIMENT IS ON, THE ENGINE CANNOT FIRE!]
EXPERIMENTS = {
    "Config_Party": False,  # (unused so far)
    "Test_Express": False,  # Creates mock log files
    "SetUp": False,  # Utility: creates logging directory structure + a log
    "Launch_UI": True,  # Opens the (temporary) HMI window
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
        for f in fields(self):
            setattr(self, f.name, False)

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
    code_state: str = "idle"  # extraneous status layers (idle / active / actor)

@dataclass
class EngineInfo:
    engine_name: str = "Blackbeard 1"

# Instantiate system components
valves = ValveState()
telemetry = TelemetryData()
state = SystemState()
engine = EngineInfo()
local_logs: list[dict] = []

# --- File System ---
def engine_dir() -> Path:
    return BASE_DIR / engine.engine_name

def integrity_checker() -> Path:
    """Creates the project folder structure (if missing) and returns its root."""
    root = engine_dir()
    for sub in ("configs", "logs", "program_files"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    print(f"Folder structure ready at: {root}")
    return root

# --- Comms ---
def receiver(sock: socket.socket) -> None:
    """Reads 'name,value' lines from the Teensy and prints them."""
    # makefile() gives line-based reads, so framing is handled for us
    with sock.makefile("r") as stream:
        for line in stream:
            name, _, value = line.strip().partition(",")
            try:
                print(f"[from teensy] {name} = {float(value)}")
            except ValueError:
                print(f"[from teensy] bad line skipped: {line!r}")

def i_send(itype: str, *args) -> None:
    if PROGRAM_DEBUG:
        print(f"[COMM] {itype}:", *args)


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
    if tst == "mini":
        return now.strftime("%S.%f")[:-3]
    return now.strftime("%H:%M:%S")


def create_log() -> Path:
    """Compiles local log entries and writes to disk."""
    timestamp = time_thread("full")
    log_dir = engine_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    filepath = log_dir / f"{timestamp}.txt"

    lines = [
        timestamp,
        "This is a new log entry. May the wind guide your hand\n",
    ]
    lines.extend(f"[{i + 1}] {entry}" for i, entry in enumerate(local_logs))

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath


def local_state(
    pa_un_state: str, pa_co_state: str, pre_req: str | None = None
) -> None:
    """Updates unit and internal code state status flags."""
    state.unit_state = pa_un_state.lower()
    state.code_state = pa_co_state.lower()

    if state.unit_state == "firing":
        i_send("state_receive", state.unit_state)
        state.kstart = True
    elif state.unit_state == "safe" and pre_req is not None:
        i_send("state_receive", state.unit_state)


# --- TEMP UI (placeholder until the real control interface is built) ---
def launch_ui() -> None:
    """Temporary blank HMI: menu bar (File/View/Tools/Help) + a blank Monitor window."""
    root = tk.Tk()
    root.title(f"BPL HMI - {engine.engine_name}")
    root.geometry("1000x650")

    monitor_window: tk.Toplevel | None = None

    def open_monitor() -> None:
        nonlocal monitor_window
        # If it's already open, just bring it forward instead of stacking copies
        if monitor_window is not None and monitor_window.winfo_exists():
            monitor_window.lift()
            monitor_window.focus_force()
            return
        monitor_window = tk.Toplevel(root)
        monitor_window.title("Monitor")
        monitor_window.geometry("700x500")

    def show_about() -> None:
        messagebox.showinfo("About", "Blinn Propulsion Labs HMI\n(temporary UI)")

    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    view_menu = tk.Menu(menubar, tearoff=0)
    view_menu.add_command(label="Monitor", command=open_monitor)
    menubar.add_cascade(label="View", menu=view_menu)

    tools_menu = tk.Menu(menubar, tearoff=0)
    tools_menu.add_command(label="(nothing yet)", state="disabled")
    menubar.add_cascade(label="Tools", menu=tools_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)
    root.mainloop()


# --- Experiments ---
def test_express() -> None:
    test_limit = 500
    period = 1.0
    for i in range(test_limit):
        local_logs.append({"T": time_thread("runtime"), "A": random.random() * 25})

        # Dynamic sleep timing loop logic
        time.sleep(random.random() / (3 * period))
        print(f"Working... ({i + 1}/{test_limit})")
        period /= 0.95
    create_log()


def init() -> None:
    """Initializes rocket valve hardware and runs active experiments."""
    valves.reset()
    state.runlogs = True
    integrity_checker()

    # Execute active configuration experiments
    if EXPERIMENTS.get("Test_Express"):
        test_express()
    if EXPERIMENTS.get("SetUp"):
        create_log()


# --- Execution Entry ---
if __name__ == "__main__":
    init()
    if EXPERIMENTS.get("Launch_UI"):
        launch_ui()

"""
'data or commands'
String format:

Sensor data:

[name of sensor]:[value]

Commands:

command:[command_type]

"""