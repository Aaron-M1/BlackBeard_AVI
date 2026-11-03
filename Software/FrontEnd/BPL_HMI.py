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
from __future__ import annotations  # importing the future of the universe to run entirely on your laptop...
from dataclasses import dataclass, fields
from datetime import datetime
import os
from pathlib import Path
import random
import socket
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser

import cv2

# ========== define directory =============
BASE_DIR = Path.home() / "Desktop" / "Blinn Propulsion Labs"

# --- Global Configuration & Experiments ---
soft_ver = "V1.10"
PROGRAM_DEBUG = True
PROGRAM_START = time.perf_counter()

# //--DEBUG / EXPERIMENTS--// [WARNING! IF ANY EXPERIMENT IS ON, THE ENGINE CANNOT FIRE!]
EXPERIMENTS = {
    "Config_Party": False,  # (unused so far)
    "Test_Express": False,  # Creates mock log files
    "SetUp": True,  # Utility: creates logging directory structure + a log
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


# --- User Interface ---
def enable_high_dpi() -> None:
  """Make Windows render the UI at native resolution instead of stretching it."""
  if sys.platform != "win32":
    return
  try:
    import ctypes

    ctypes.windll.shcore.SetProcessDpiAwareness(2)
  except (AttributeError, OSError):
    try:
      import ctypes

      ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
      pass


def launch_ui() -> None:
  """Primary HMI window: menu bar + camera feed monitor."""
  enable_high_dpi()

  root = tk.Tk()
  root.title(f"BPL HMI - {engine.engine_name}")
  root.geometry("1000x650")

  camera_thread: threading.Thread | None = None
  camera_running = False

  def run_camera_feed() -> None:
    nonlocal camera_running
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():
      rval, frame = vc.read()
    else:
      rval = False

    while rval and camera_running:
      cv2.imshow("preview", frame)
      rval, frame = vc.read()
      key = cv2.waitKey(20)
      # Check if window was closed or 'q' was pressed
      if (
          key == ord("q")
          or key == 27
          or cv2.getWindowProperty("preview", cv2.WND_PROP_VISIBLE) < 1
      ):
        break

    camera_running = False
    cv2.destroyWindow("preview")
    vc.release()

  def open_monitor() -> None:
    nonlocal camera_thread, camera_running
    # Prevent starting duplicate camera threads if already open
    if camera_running and camera_thread is not None and camera_thread.is_alive():
      return

    camera_running = True
    camera_thread = threading.Thread(target=run_camera_feed, daemon=True)
    camera_thread.start()

  def show_about() -> None:
    messagebox.showinfo(
        "Acknowledgements",
        f"Blinn Propulsion Labs HMI\n({soft_ver})\n\nProgramming:\nAaron"
        " Mathews\nParker Pevehouse\nTroy Martell\nZimife Onovo",
    )

  def read_me() -> None:
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
      webbrowser.open(readme_path.resolve().as_uri())
    else:
      messagebox.showerror(
          "Error", f"Documentation file not found:\n{readme_path}"
      )

  def on_exit() -> None:
    nonlocal camera_running
    camera_running = False
    root.destroy()

  menubar = tk.Menu(root)

  file_menu = tk.Menu(menubar, tearoff=0)
  file_menu.add_command(label="Settings", state="disabled")
  file_menu.add_command(label="File Integrity", state="disabled")
  file_menu.add_command(label="Exit", command=on_exit)
  menubar.add_cascade(label="File", menu=file_menu)

  view_menu = tk.Menu(menubar, tearoff=0)
  view_menu.add_command(label="Open Telemetry")
  view_menu.add_command(label="Open Monitor", command=open_monitor)
  menubar.add_cascade(label="View", menu=view_menu)

  tools_menu = tk.Menu(menubar, tearoff=0)
  tools_menu.add_command(label="(nothing yet)", state="disabled")
  menubar.add_cascade(label="Tools", menu=tools_menu)

  help_menu = tk.Menu(menubar, tearoff=0)
  help_menu.add_command(label="Docs", command=read_me)
  help_menu.add_command(label="Acknowledgements", command=show_about)
  menubar.add_cascade(label="Help", menu=help_menu)

  root.config(menu=menubar)
  root.protocol("WM_DELETE_WINDOW", on_exit)
  root.mainloop()


# --- Experiments ---
def test_express() -> None:
  test_limit = 500
  period = 1.0
  for i in range(test_limit):
    local_logs.append({"T": time_thread("runtime"), "A": random.random() * 25})
    time.sleep(random.random() / (3 * period))
    print(f"Working... ({i + 1}/{test_limit})")
    period /= 0.95
  create_log()


def init() -> None:
  """Initializes rocket valve hardware and runs active setup routines."""
  valves.reset()
  state.runlogs = True
  integrity_checker()

  if EXPERIMENTS.get("Test_Express"):
    test_express()
  if EXPERIMENTS.get("SetUp"):
    create_log()


# --- Execution Entry ---
if __name__ == "__main__":
  init()
  launch_ui()  # Permanent startup execution