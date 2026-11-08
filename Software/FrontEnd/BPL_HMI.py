#
#██████╗ ██╗      █████╗  ██████╗██╗  ██╗██████╗ ███████╗ █████╗ ██████╗ ██████╗     ███████╗██████╗  ██████╗ ███╗   ██╗████████╗
#██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝
#██████╔╝██║     ███████║██║     █████╔╝ ██████╔╝█████╗  ███████║██████╔╝██║  ██║    █████╗  ██████╔╝██║   ██║██╔██╗ ██║   ██║   
#██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██╔══██╗██╔══╝  ██╔══██║██╔══██╗██║  ██║    ██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║   ██║   
#██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██████╔╝███████╗██║  ██║██║  ██║██████╔╝    ██║     ██║  ██║╚██████╔╝██║ ╚████║   ██║   
#╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
#

# 𝔅𝔩𝔦𝔫𝔫 𝔓𝔯𝔬𝔭𝔲𝔩𝔰𝔦𝔬𝔫 𝔏𝔞𝔟𝔬𝔯𝔞𝔱𝔬𝔯𝔦𝔢𝔰
# V1.00.00  :  9/29/2026     

# # Everett mitchell was caught playing mario kart wii in the student center at 9/30/2026 at 9:29 AM
# God rewards you for not ending it, so embrace.                                                                                                                           
# Standard Libraries (No installation required)

# Todo:
# 1. Add button for connection testing -- DONEZO -troy
# 2. Fix the weird visual caused by resizing the Window

from __future__ import annotations
import random
import socket
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
import webbrowser
from dataclasses import dataclass, fields
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
import cv2
from PIL import Image, ImageDraw, ImageTk

# =============================================================================
# Configuration
# =============================================================================
BASE_DIR = Path.home() / "Desktop" / "Blinn Propulsion Labs"

SOFT_VER = "V1.40"
PROGRAM_DEBUG = True
PROGRAM_START = time.perf_counter()
TELEMETRY_REFRESH_MS = 100  # how often the on-screen readings refresh
DESIGN_W, DESIGN_H = 1400, 850
TEXT_BOOST = 1.3  # makes all P&ID text, symbols and valve boxes this much bigger

# Window / diagram colors
COLOR_TOP = "#161517"
COLOR_BOTTOM = "#252023"
COLOR_PANEL = "#1b1a1d"
COLOR_PID_BG = "#121113"
COLOR_LINE = "#e5e7eb"      # pipes and outlines
COLOR_SYMBOL = "#1b1a1d"    # manual-valve fill
COLOR_OPEN = "#16a34a"      # green
COLOR_CLOSED = "#dc2626"    # red
COLOR_READING = "#38bdf8"   # sensor readings
COLOR_WARN = "#f59e0b"      # manual control ON

# //--DEBUG / EXPERIMENTS--// [WARNING! IF ANY EXPERIMENT IS ON, THE ENGINE CANNOT FIRE!]
EXPERIMENTS = {
    "Config_Party": False,  # (unused so far)
    "Test_Express": False,  # Creates mock log files
    "SetUp": True,          # Utility: creates logging directory structure + a log
}

# =============================================================================
# State, telemetry & settings structures
# =============================================================================
@dataclass
class ValveState:
  gb_solenoid: bool = False  # GN2 Back Pressurizing Solenoid
  fuel_purge: bool = False   # Fuel Purging Solenoid
  fuel_main: bool = False    # Fuel Main Valve
  ox_main: bool = False      # Oxidizer Main Valve
  ORIPS: bool = False        # Oxidizer Run Tank Purge Solenoid (ORTPS on the P&ID)
  CPS: bool = False          # Chiller Purge Solenoid
  CMS: bool = False          # Chiller Main Solenoid

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

@dataclass
class AppSettings:
  manual_control: bool = False  # valves are NOT user-controllable by default
  host_ip: str = "127.0.0.1"
  socket: int = 5000

valves = ValveState()
telemetry = TelemetryData()
state = SystemState()
engine = EngineInfo()
settings = AppSettings()
local_logs: list[dict] = []


# =============================================================================
# Valve & sensor registries
# =============================================================================
# P&ID tag -> (ValveState attribute, description, box x, box y, box anchor)
# Box x/y are in diagram coordinates (REF_W x REF_H below).
VALVE_LAYOUT: dict[str, tuple[str, str, int, int, str]] = {
    "GBS":   ("gb_solenoid", "GN2 Back Pressurizing Solenoid",   350, 130, "n"),
    "FPS":   ("fuel_purge",  "Fuel Purging Solenoid",            440, 385, "n"),
    "FMV":   ("fuel_main",   "Fuel Main Valve",                  720, 385, "n"),
    "OMV":   ("ox_main",     "Oxidizer Main Valve",              720, 655, "n"),
    "ORTPS": ("ORIPS",       "Oxidizer Run Tank Purge Solenoid", 566, 684, "ne"),
    "CPS":   ("CPS",         "Chiller Purge Solenoid",           192, 685, "nw"),
    "CMS":   ("CMS",         "Chiller Main Solenoid",            410, 655, "n"),
}

# Passive valves / parts that appear on the drawing but are not controllable
PASSIVE_PARTS = {
    "GPR": "GN2 Pressure Regulator",
    "GPRV": "GN2 Pressure Relief Valve",
    "GCV": "GN2 Check Valve",
    "FCV": "Fuel Check Valve",
    "OCV": "Oxidizer Check Valve",
    "CCV": "Chiller Check Valve",
}

# P&ID tag -> (TelemetryData field, description, unit)
# Edit this table if a sensor is wired to a different field or reads in other units.
SENSORS: dict[str, tuple[str, str, str]] = {
    "P1": ("gpressure_press", "GN2 Regulated Pressure", "PSI"),
    "P2": ("k_bottle_press",  "N2O K-Bottle",           "PSI"),
    "P3": ("chiller_press",   "Chiller",                "PSI"),
    "P4": ("e_run_press",     "Ethanol Run Tank",       "PSI"),
    "P5": ("n2o_press",       "N2O Run Tank",           "PSI"),
    "P6": ("fuel_c_press",    "Fuel Chamber",           "PSI"),
    "P7": ("oxi_c_press",     "Oxidizer Chamber",       "PSI"),
    "T":  ("n2o_temp",        "N2O Run Tank Temp",      "\u00b0C"),
}


def get_valve(key: str) -> bool:
  return getattr(valves, VALVE_LAYOUT[key][0])

def set_valve(key: str, is_open: bool) -> None:
  """Single entry point for changing a valve (hook your Teensy command here)."""
  setattr(valves, VALVE_LAYOUT[key][0], is_open)
  i_send("valve_cmd", key, "OPEN" if is_open else "CLOSED")

def format_reading(tag: str) -> str:
  field, _desc, unit = SENSORS[tag]
  return f"{getattr(telemetry, field):.1f} {unit}"

# =============================================================================
# File system
# =============================================================================
def engine_dir() -> Path:
  return BASE_DIR / engine.engine_name

def integrity_checker() -> Path:
  """Creates the project folder structure (if missing) and returns its root."""
  root = engine_dir()
  for sub in ("configs", "logs", "program_files"):
    (root / sub).mkdir(parents=True, exist_ok=True)
  print(f"Folder structure ready at: {root}")
  return root

# =============================================================================
# Comms
# =============================================================================
def receiver(sock: socket.socket) -> None:
  """Reads 'name,value' lines from the Teensy and stores them in `telemetry`.

  `name` must match a TelemetryData field (e.g. "e_run_press,412.7").
  Runs on a worker thread; the UI picks the values up on its own refresh timer.
  """
  with sock.makefile("r") as stream:
    for line in stream:
      name, _, value = line.strip().partition(",")
      try:
        number = float(value)
      except ValueError:
        print(f"[from teensy] bad line skipped: {line!r}")
        continue
      if hasattr(telemetry, name):
        setattr(telemetry, name, number)
      else:
        print(f"[from teensy] unknown channel skipped: {name!r}")


def i_send(itype: str, *args) -> None:
  if PROGRAM_DEBUG:
    print(f"[COMM] {itype}:", *args)

# =============================================================================
# Utilities
# =============================================================================
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

  lines = [timestamp, "This is a new log entry. May the wind guide your hand\n"]
  lines.extend(f"[{i + 1}] {entry}" for i, entry in enumerate(local_logs))

  filepath.write_text("\n".join(lines), encoding="utf-8")
  return filepath


def local_state(pa_un_state: str, pa_co_state: str, pre_req: str | None = None) -> None:
  """Updates unit and internal code state status flags."""
  state.unit_state = pa_un_state.lower()
  state.code_state = pa_co_state.lower()

  if state.unit_state == "firing":
    i_send("state_receive", state.unit_state)
    state.kstart = True
  elif state.unit_state == "safe" and pre_req is not None:
    i_send("state_receive", state.unit_state)


# =============================================================================
# User interface
# =============================================================================
def enable_high_dpi() -> None:
  """Make Windows render the UI at native resolution instead of stretching it."""
  if sys.platform != "win32":
    return
  import ctypes

  try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
  except (AttributeError, OSError):
    try:
      ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
      pass


def create_vertical_gradient(width: int, height: int, start_hex: str, end_hex: str) -> ImageTk.PhotoImage:
  """Generates a vertical gradient image between two hex colors."""
  height = max(1, height)
  start = tuple(int(start_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
  end = tuple(int(end_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

  img = Image.new("RGB", (max(1, width), height))
  draw = ImageDraw.Draw(img)
  for y in range(height):
    t = y / height
    draw.line([(0, y), (width, y)], fill=tuple(int(s + (e - s) * t) for s, e in zip(start, end)))
  return ImageTk.PhotoImage(img)


# Size of the coordinate system the diagram is drawn in. Everything is scaled
# from this to whatever size the canvas currently is.
REF_W, REF_H = 1040, 780

# ---- Settings window building blocks -------------------------------------
def settings_section(parent, title: str) -> tk.LabelFrame:
  """A titled box. Everything related goes inside one of these."""
  frame = tk.LabelFrame(parent, text=f" {title} ", fg="#ffffff", bg=COLOR_PANEL,
                        bd=1, relief="solid", font=("Consolas", 9, "bold"))
  frame.pack(fill="x", padx=15, pady=5)
  return frame

def settings_note(parent, text: str) -> None:
  """Small grey help text under a control."""
  tk.Label(parent, text=text, fg="#9ca3af", bg=COLOR_PANEL, justify="left",
           font=("Consolas", 8)).pack(anchor="w", padx=10, pady=(0, 6))

def settings_checkbox(parent, text: str, variable: tk.BooleanVar, command) -> None:
  tk.Checkbutton(parent, text=text, variable=variable, command=command,
                 fg="#ffffff", bg=COLOR_PANEL, selectcolor="#2d2b30",
                 activebackground=COLOR_PANEL, activeforeground="#ffffff",
                 font=("Consolas", 10, "bold"), cursor="hand2").pack(anchor="w", padx=10, pady=(6, 2))

def settings_entry(parent, label: str, variable: tk.StringVar, width: int = 12) -> None:
  """One row: a label on the left, a text box on the right. Use for text AND integers."""
  row = tk.Frame(parent, bg=COLOR_PANEL)
  row.pack(anchor="w", padx=10, pady=2)
  tk.Label(row, text=label, fg="#d1d5db", bg=COLOR_PANEL, width=10, anchor="w",
           font=("Consolas", 9, "bold")).pack(side="left")
  tk.Entry(row, textvariable=variable, width=width, bg="#2d2b30", fg="#ffffff",
           insertbackground="#ffffff", relief="flat", font=("Consolas", 10)).pack(side="left")


def settings_button(parent, text: str, command) -> tk.Button:
  btn = tk.Button(parent, text=text, command=command, bg="#2d2b30", fg="#ffffff",
                  activebackground="#3f3c44", activeforeground="#ffffff", relief="flat",
                  font=("Consolas", 9, "bold"), padx=10)
  btn.pack(anchor="w", padx=10, pady=(4, 8))
  return btn


def settings_status(parent) -> tk.Label:
  """A line of feedback text you can update after pressing Apply."""
  lbl = tk.Label(parent, text="", fg="#9ca3af", bg=COLOR_PANEL, font=("Consolas", 8))
  lbl.pack(anchor="w", padx=10)
  return lbl

class PIDCanvas(tk.Canvas):
  """Native P&ID with live sensor readings and a status + toggle box per valve.

  Layout is organized in three bands, left to right:
    top    - GN2 pressurization line into the ethanol run tank
    middle - ethanol run tank and fuel line into the TCA
    bottom - N2O K-bottle -> chiller -> N2O run tank -> oxidizer line into the TCA
  """

  def __init__(self, parent, on_toggle, get_open, get_reading, **kwargs):
    super().__init__(parent, **kwargs)
    self.on_toggle = on_toggle     # callback(valve_key)
    self.get_open = get_open       # callback(valve_key) -> bool
    self.get_reading = get_reading  # callback(sensor_tag) -> str
    self.controls_enabled = False  # toggle buttons locked until manual control is on
    self.scale = 1.0
    self.ox = self.oy = 0.0        # offset that centers the diagram
    self.lw = max(1.5, 2.0 * self.scale)
    self.boxes: dict[str, dict] = {}

    # Fonts for the valve boxes (resized with the window)
    self.f_tag = tkfont.Font(family="Consolas", size=-10, weight="bold")
    self.f_status = tkfont.Font(family="Consolas", size=-10, weight="bold")
    self.f_btn = tkfont.Font(family="Consolas", size=-9, weight="bold")

    self._redraw_job = None
    self.bind("<Configure>", self._schedule_redraw)

  def _schedule_redraw(self, event) -> None:
    if self._redraw_job is not None:
      self.after_cancel(self._redraw_job)
    self._redraw_job = self.after(50, self.redraw)

  def _run_redraw(self) -> None:
    self._redraw_job = None
    self.redraw()

  # ---------------------------------------------------------------- layout --
  def redraw(self) -> None:
    cw, ch = self.winfo_width(), self.winfo_height()
    if cw < 50 or ch < 50:
      return
    self.scale = min(cw / REF_W, ch / REF_H)
    self.ox = (cw - REF_W * self.scale) / 2
    self.oy = (ch - REF_H * self.scale) / 2
    self.lw = max(1.0, 1.6 * self.scale)

    self._resize_box_fonts()
    self.delete("diagram")
    self._draw_diagram()
    self._place_boxes()

  def _t(self, x: float, y: float) -> tuple[float, float]:
    return self.ox + x * self.scale, self.oy + y * self.scale

  # ------------------------------------------------------------ primitives --
  def _line(self, pts, color=COLOR_LINE, tags=(), **kw) -> None:
    flat = [c for p in pts for c in self._t(*p)]
    kw.setdefault("width", self.lw)
    self.create_line(*flat, fill=color, tags=("diagram", *tags), **kw)

  def _poly(self, pts, fill="", tags=(), **kw) -> None:
    flat = [c for p in pts for c in self._t(*p)]
    kw.setdefault("outline", COLOR_LINE)
    self.create_polygon(*flat, fill=fill, width=self.lw, tags=("diagram", *tags), **kw)

  def _rect(self, x0, y0, x1, y1, fill=COLOR_PID_BG, outline=COLOR_LINE, tags=()) -> None:
    ax, ay = self._t(x0, y0)
    bx, by = self._t(x1, y1)
    self.create_rectangle(ax, ay, bx, by, fill=fill, outline=outline,
                          width=self.lw, tags=("diagram", *tags))

  def _rounded(self, x0, y0, x1, y1, r=14, dash=None) -> None:
    pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r, x1, y1 - r, x1, y1,
           x1 - r, y1, x0 + r, y1, x0, y1, x0, y1 - r, x0, y0 + r, x0, y0]
    flat = [c for i in range(0, len(pts), 2) for c in self._t(pts[i], pts[i + 1])]
    self.create_polygon(*flat, smooth=True, fill=COLOR_PID_BG, outline=COLOR_LINE,
                        width=self.lw, dash=dash, tags="diagram")

  def _circle(self, x, y, text, r=13) -> None:
    ax, ay = self._t(x - r, y - r)
    bx, by = self._t(x + r, y + r)
    self.create_oval(ax, ay, bx, by, fill=COLOR_PID_BG, outline=COLOR_LINE,
                     width=self.lw, tags="diagram")
    self._text(x, y, text, size=11)

  def _text(self, x, y, text, size=11, anchor="center", color=COLOR_LINE,
            bold=True, tags=()) -> None:
    px = max(9, round(size * self.scale * TEXT_BOOST))
    weight = "bold" if bold else "normal"
    self.create_text(*self._t(x, y), text=text, fill=color, anchor=anchor,
                     justify="center", font=("Consolas", -px, weight),
                     tags=("diagram", *tags))

  def _arrow(self, x0, y0, x1, y1) -> None:
    self._line([(x0, y0), (x1, y1)], arrow=tk.LAST, arrowshape=(8, 10, 4))

  # --------------------------------------------------------------- symbols --
  def _symbol_fill(self, key: str | None) -> str:
    if key is None:
      return COLOR_SYMBOL
    return COLOR_OPEN if self.get_open(key) else COLOR_CLOSED

  def _bowtie(self, x, y, orient="h", key=None, solenoid=False) -> None:
    """Gate/solenoid valve symbol. Keyed valves are colored by their state."""
    fill = self._symbol_fill(key)
    tags = (f"sym_{key}",) if key else ()
    d, hh = 15, 10
    if orient == "h":
      tris = [[(x - d, y - hh), (x, y), (x - d, y + hh)],
              [(x + d, y - hh), (x, y), (x + d, y + hh)]]
    else:
      tris = [[(x - hh, y - d), (x, y), (x + hh, y - d)],
              [(x - hh, y + d), (x, y), (x + hh, y + d)]]
    for tri in tris:
      self._poly(tri, fill=fill, tags=tags)

    if solenoid:  # little actuator square, like the P&ID key
      if orient == "h":
        self._line([(x, y), (x, y - 13)])
        self._rect(x - 5, y - 24, x + 5, y - 13)
      else:
        self._line([(x, y), (x - 13, y)])
        self._rect(x - 24, y - 5, x - 13, y + 5)

  def _check(self, x, y, orient="h", key=None) -> None:
    """Check valve symbol (hinged flap + seat). Colored if it has a state."""
    color = COLOR_LINE if key is None else self._symbol_fill(key)
    tags = (f"sym_{key}",) if key else ()
    if orient == "h":
      self._rect(x - 12, y - 8, x + 12, y + 8, outline=COLOR_PID_BG)     # gap in pipe
      self._line([(x - 11, y), (x + 5, y - 12)], color, tags)            # flap
      self._line([(x + 11, y - 10), (x + 11, y + 10)], color, tags)      # seat
    else:
      self._rect(x - 8, y - 12, x + 8, y + 12, outline=COLOR_PID_BG)
      self._line([(x, y - 11), (x + 12, y + 5)], color, tags)
      self._line([(x - 10, y + 11), (x + 10, y + 11)], color, tags)
  
  def _sensor(self, tag: str, x: float, y: float, side: str, r: int = 16) -> None:
    """Sensor bubble plus its live reading placed above/below/left/right of it."""
    self._circle(x, y, tag, r)
    if side == "above":
      pos, anchor = (x, y - r - 14), "center"
    elif side == "below":
      pos, anchor = (x, y + r + 14), "center"
    elif side == "left":
      pos, anchor = (x - r - 6, y), "e"
    else:
      pos, anchor = (x + r + 6, y), "w"
    self._text(*pos, self.get_reading(tag), size=10, anchor=anchor,
               color=COLOR_READING, tags=(f"read_{tag}",))

  # --------------------------------------------------------------- diagram --
  def _draw_diagram(self) -> None:
    # ---- Pipes first, so symbols and tanks sit on top of them ----
    # GN2 line: bottle -> ethanol tank (top band, y=105)
    self._line([(95, 105), (580, 105), (580, 190)])
    self._line([(270, 86), (270, 105)])                              # P1 tap
    self._line([(440, 105), (440, 93), (434, 88), (446, 81),         # GPRV tap + spring
                (434, 74), (446, 67), (440, 62)])
    self._arrow(440, 62, 440, 38)                                    # GPRV vent
    self._rect(438, 103, 442, 107, fill=COLOR_LINE)                  # junction dot

    # Fuel line: ethanol tank -> TCA (middle band, y=360)
    self._line([(580, 280), (580, 360)])                             # tank outlet
    self._line([(440, 360), (900, 360)])                             # FPS .. FMV .. FCV .. TCA
    self._line([(580, 305), (630, 305)])                             # P4 tap
    self._line([(875, 322), (875, 360)])                             # P6 tap
    self._arrow(350, 360, 423, 360)                                  # ambient vent into FPS
    self._rect(578, 358, 582, 362, fill=COLOR_LINE)                  # junction dot

    # N2O / oxidizer line (bottom band, y=630), rises on the right into the TCA
    self._line([(95, 630), (215, 630)])                              # K-bottle -> chiller
    self._line([(365, 630), (810, 630), (810, 420), (900, 420)])     # oxidizer line -> TCA
    self._line([(600, 590), (600, 706)])                             # N2O run tank -> ORTPS
    self._line([(170, 606), (170, 630)])                             # P2 tap
    self._line([(470, 606), (470, 630)])                             # P3 tap
    self._line([(645, 525), (662, 525)])                             # T tap
    self._line([(645, 568), (659, 568)])                             # P5 tap
    self._line([(870, 420), (870, 452)])                             # P7 tap
    self._line([(170, 630), (170, 704)])                             # CPS branch
    self._rect(598, 628, 602, 632, fill=COLOR_LINE)                  # junction dot

    # ---- Tanks / vessels (compact, not to scale) ----
    self._rounded(15, 55, 95, 155)
    self._text(55, 105, "GN2\n2Ksi", size=11)
    self._rounded(535, 190, 625, 280)
    self._text(580, 235, "Ethanol\nRun Tank", size=11)
    self._rounded(555, 500, 645, 590)
    self._text(600, 545, "N2O\nRun Tank", size=11)
    self._rounded(15, 585, 95, 675)
    self._text(55, 630, "N2O\nK-Bottle", size=11)
    self._rounded(215, 595, 365, 665, r=12, dash=(5, 4))
    self._text(225, 610, "N2O Chiller", anchor="w", size=11, bold=False)
    self._line([(215, 630), (365, 630)], dash=(2, 4))                # through the chiller

    # ---- Thrust chamber assembly ----
    self._poly([(900, 325), (950, 325), (1010, 290), (1010, 490), (950, 455), (900, 455)],
               fill=COLOR_PID_BG)
    ax, ay = self._t(995, 290)
    bx, by = self._t(1025, 490)
    self.create_oval(ax, ay, bx, by, outline=COLOR_LINE, width=self.lw, tags="diagram")
    self._text(925, 390, "TCA", size=14)

    # ---- GN2 section ----
    self._bowtie(130, 105)                                  # manual valve at bottle
    self._rect(175, 93, 199, 117)                           # GPR
    self._arrow(170, 121, 204, 90)
    self._text(187, 70, "GPR", size=11)
    self._sensor("P1", 270, 70, "above")
    self._bowtie(350, 105, "h", key="GBS", solenoid=True)
    self._text(440, 18, "GPRV", size=11)
    self._check(510, 105, "h")
    self._text(510, 130, "GCV", size=11)
    self._bowtie(580, 150, "v")                             # manual valve at ethanol tank

    # ---- Fuel section ----
    self._sensor("P4", 646, 305, "right")
    self._bowtie(440, 360, "h", key="FPS", solenoid=True)
    self._bowtie(720, 360, "h", key="FMV", solenoid=True)
    self._check(830, 360, "h")
    self._text(830, 384, "FCV", size=11)
    self._sensor("P6", 875, 306, "above")

    # ---- Oxidizer / chiller section ----
    self._bowtie(130, 630)                                  # manual valve at K-bottle
    self._sensor("P2", 170, 590, "above")
    self._bowtie(170, 685, "v", key="CPS", solenoid=True)
    for dx in (0, -14, 14):                                 # ambient exhaust under CPS
      self._arrow(170, 708, 170 + dx, 732)
    self._bowtie(410, 630, "h", key="CMS", solenoid=True)
    self._sensor("P3", 470, 590, "above")
    self._check(520, 630, "h")
    self._text(520, 654, "CCV", size=11)
    self._sensor("T", 675, 525, "right", r=13)
    self._sensor("P5", 675, 568, "right")
    self._bowtie(600, 690, "v", key="ORTPS", solenoid=True)
    for dx in (0, -14, 14):                                 # ambient exhaust under ORTPS
      self._arrow(600, 712, 600 + dx, 736)
    self._bowtie(720, 630, "h", key="OMV", solenoid=True)
    self._check(810, 490, "v")
    self._text(792, 490, "OCV", anchor="e", size=11)
    self._sensor("P7", 870, 468, "below")
  
  # ----------------------------------------------------- valve control boxes --
  def add_valve_box(self, key: str, x: int, y: int, anchor: str, is_open: bool) -> None:
    """Small box: valve tag, status dot + OPEN/CLOSED, and a TOGGLE button."""
    bg = "#0f0e10"
    box = tk.Frame(self, bg=bg, highlightbackground="#6b7280", highlightthickness=1)

    tk.Label(box, text=key, fg="#9ca3af", bg=bg, font=self.f_tag).pack(
        fill="x", padx=3, pady=(1, 0))

    row = tk.Frame(box, bg=bg)
    row.pack(fill="x", padx=3)
    dot = tk.Canvas(row, width=12, height=12, bg=bg, highlightthickness=0)
    dot_id = dot.create_oval(1, 1, 11, 11, outline="#ffffff", width=1,
                             fill=COLOR_OPEN if is_open else COLOR_CLOSED)
    dot.pack(side="left")
    status = tk.Label(row, text="OPEN" if is_open else "CLOSED", fg="#ffffff",
                      bg=bg, font=self.f_status)
    status.pack(side="left", padx=(3, 0))

    button = tk.Button(box, font=self.f_btn, relief="flat", bd=0, pady=1,
                       command=lambda k=key: self.on_toggle(k))
    button.pack(fill="x", padx=3, pady=(2, 3))

    item = self.create_window(0, 0, window=box, anchor=anchor)
    self.boxes[key] = {"item": item, "x": x, "y": y, "dot": dot, "dot_id": dot_id,
                       "status": status, "button": button}
    self._style_button(button)

  def _style_button(self, button: tk.Button) -> None:
    if self.controls_enabled:
      button.config(state="normal", text="TOGGLE", bg="#2d2b30", fg="#ffffff",
                    activebackground="#3f3c44", activeforeground="#ffffff", cursor="hand2")
    else:
      button.config(state="disabled", text="LOCKED", bg="#1f1e22",
                    disabledforeground="#6b7280", cursor="arrow")

  def set_controls_enabled(self, enabled: bool) -> None:
    """Unlock / lock every valve toggle button (driven by Settings)."""
    self.controls_enabled = enabled
    for info in self.boxes.values():
      self._style_button(info["button"])

  def _resize_box_fonts(self) -> None:
    def px(n: int) -> int:
      return -max(9, round(n * self.scale * TEXT_BOOST))
    self.f_tag.configure(size=px(10))
    self.f_status.configure(size=px(10))
    self.f_btn.configure(size=px(9))
    d = max(10, round(12 * self.scale * TEXT_BOOST))
    for info in self.boxes.values():
      info["dot"].config(width=d, height=d)
      info["dot"].coords(info["dot_id"], 1, 1, d - 1, d - 1)

  def _place_boxes(self) -> None:
    for info in self.boxes.values():
      self.coords(info["item"], *self._t(info["x"], info["y"]))
      self.tag_raise(info["item"])

  def update_valve_status(self, key: str, is_open: bool) -> None:
    info = self.boxes.get(key)
    if info is None:
      return
    color = COLOR_OPEN if is_open else COLOR_CLOSED
    info["dot"].itemconfig(info["dot_id"], fill=color)
    info["status"].config(text="OPEN" if is_open else "CLOSED")
    self.itemconfig(f"sym_{key}", fill=color)  # recolor the symbol on the diagram

  def update_readings(self) -> None:
    for tag in SENSORS:
      self.itemconfig(f"read_{tag}", text=self.get_reading(tag))


def launch_ui() -> None:
  """Primary HMI window: menu bar + camera monitor + 2/3 native P&ID + sidebar."""
  enable_high_dpi()

  root = tk.Tk()
  root.title(f"BPL HMI - {engine.engine_name}")
  root.geometry("1400x850")
  root.minsize(1100, 700)
  base_tk_scaling = float(root.tk.call("tk", "scaling"))

  # --- Gradient background ---
  canvas = tk.Canvas(root, highlightthickness=0, bg=COLOR_BOTTOM)
  canvas.pack(fill="both", expand=True)
  bg_image = None  # keep a reference so Tk doesn't garbage-collect it

  ui_container = tk.Frame(canvas, bg=COLOR_BOTTOM)
  container_window = canvas.create_window((0, 0), window=ui_container, anchor="nw")

  resize_job = None
  applied_scale = 0.0
  last_size = (0, 0)

  def apply_heavy_layout(width: int, height: int, scale: float) -> None:
    """Expensive work: runs once after resizing pauses, not on every event."""
    nonlocal bg_image, resize_job, applied_scale
    resize_job = None

    w, h = int(DESIGN_W * scale), int(DESIGN_H * scale)
    canvas.coords(container_window, (width - w) // 2, (height - h) // 2)
    canvas.itemconfig(container_window, width=w, height=h)

    bg_image = create_vertical_gradient(width, height, COLOR_TOP, COLOR_BOTTOM)
    canvas.delete("gradient")
    canvas.create_image(0, 0, image=bg_image, anchor="nw", tags="gradient")
    canvas.tag_lower("gradient")

    # Only touch Tk's scaling if it actually changed meaningfully
    if abs(scale - applied_scale) > 0.02:
      root.tk.call("tk", "scaling", base_tk_scaling * scale)
      applied_scale = scale

    root.config(menu=menubar)  # force the menu bar to repaint cleanly

  def update_layout(event) -> None:
    nonlocal resize_job, last_size
    if event.width <= 1 or event.height <= 1:
      return
    if (event.width, event.height) == last_size:
      return
    last_size = (event.width, event.height)

    scale = min(event.width / DESIGN_W, event.height / DESIGN_H)

    if resize_job is not None:
      canvas.after_cancel(resize_job)
    resize_job = canvas.after(150, apply_heavy_layout, event.width, event.height, scale)

  canvas.bind("<Configure>", update_layout)

  # Left 2/3 = P&ID, right 1/3 = sidebar
  ui_container.columnconfigure(0, weight=1)   # P&ID takes everything the sidebar doesn't need
  ui_container.columnconfigure(1, weight=0)   # sidebar keeps its natural width
  ui_container.rowconfigure(0, weight=1)

  # --- Left panel: native P&ID ---
  pid_frame = tk.LabelFrame(ui_container, text=" SYSTEM P&ID DIAGRAM ", fg="#ffffff",
                            bg=COLOR_PANEL, bd=1, relief="solid",
                            font=("Consolas", 10, "bold"))
  pid_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=15)

  def toggle_valve(key: str) -> None:
    if not settings.manual_control:  # belt and braces: buttons are disabled anyway
      return
    new_state = not get_valve(key)
    set_valve(key, new_state)
    pid_canvas.update_valve_status(key, new_state)
    refresh_valve_summary()

  pid_canvas = PIDCanvas(pid_frame, on_toggle=toggle_valve, get_open=get_valve,
                         get_reading=format_reading, bg=COLOR_PID_BG,
                         highlightthickness=0)
  pid_canvas.pack(fill="both", expand=True, padx=5, pady=5)

  for key, (_attr, _desc, bx, by, anchor) in VALVE_LAYOUT.items():
    pid_canvas.add_valve_box(key, bx, by, anchor, is_open=get_valve(key))

  def close_all_valves() -> None:
    """Always available: closing everything is the safe direction."""
    for key in VALVE_LAYOUT:
      if get_valve(key):
        set_valve(key, False)
      pid_canvas.update_valve_status(key, False)
    refresh_valve_summary()

# Breathe in the air.
  # --- Right panel: telemetry & controls ---
  sidebar = tk.LabelFrame(ui_container, text=" TELEMETRY & CONTROLS ", fg="#ffffff",
                          bg=COLOR_PANEL, bd=1, relief="solid",
                          font=("Consolas", 10, "bold"))
  sidebar.grid(row=0, column=1, sticky="nsew", padx=(7, 15), pady=15)

  tk.Label(sidebar, text=f"STATUS: {state.unit_state.upper()}", fg="#22c55e",
           bg=COLOR_PANEL, font=("Consolas", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 2))

  manual_label = tk.Label(sidebar, text="MANUAL CONTROL: OFF", fg="#9ca3af",
                          bg=COLOR_PANEL, font=("Consolas", 10, "bold"))
  manual_label.pack(anchor="w", padx=10, pady=(0, 8))

  tk.Button(sidebar, text="CLOSE ALL VALVES", command=close_all_valves, bg="#7f1d1d",
            fg="#ffffff", activebackground="#991b1b", activeforeground="#ffffff",
            font=("Consolas", 9, "bold")).pack(anchor="w", padx=10, pady=(0, 10))

  # Sensor readings table
  tk.Label(sidebar, text="SENSORS", fg="#9ca3af", bg=COLOR_PANEL,
           font=("Consolas", 9, "bold")).pack(anchor="w", padx=10)
  sensor_grid = tk.Frame(sidebar, bg=COLOR_PANEL)
  sensor_grid.pack(anchor="w", padx=10, pady=(2, 10), fill="x")
  sensor_labels: dict[str, tk.Label] = {}
  for row, (tag, (_field, desc, _unit)) in enumerate(SENSORS.items()):
    tk.Label(sensor_grid, text=tag, fg="#ffffff", bg=COLOR_PANEL, width=3, anchor="w",
             font=("Consolas", 9, "bold")).grid(row=row, column=0, sticky="w")
    tk.Label(sensor_grid, text=desc, fg="#d1d5db", bg=COLOR_PANEL, anchor="w",
             font=("Consolas", 9)).grid(row=row, column=1, sticky="w", padx=(4, 12))
    value = tk.Label(sensor_grid, text="", fg=COLOR_READING, bg=COLOR_PANEL, anchor="e",
                     font=("Consolas", 9, "bold"))
    value.grid(row=row, column=2, sticky="e")
    sensor_labels[tag] = value
  sensor_grid.columnconfigure(1, weight=1)

  # Valve summary + legend
  tk.Label(sidebar, text="VALVES", fg="#9ca3af", bg=COLOR_PANEL,
           font=("Consolas", 9, "bold")).pack(anchor="w", padx=10)
  valve_grid = tk.Frame(sidebar, bg=COLOR_PANEL)
  valve_grid.pack(anchor="w", padx=10, pady=(2, 8), fill="x")
  valve_labels: dict[str, tk.Label] = {}
  for row, (tag, (_a, desc, *_rest)) in enumerate(VALVE_LAYOUT.items()):
    tk.Label(valve_grid, text=tag, fg="#ffffff", bg=COLOR_PANEL, width=6, anchor="w",
             font=("Consolas", 9, "bold")).grid(row=row, column=0, sticky="w")
    tk.Label(valve_grid, text=desc, fg="#d1d5db", bg=COLOR_PANEL, anchor="w",
             font=("Consolas", 9)).grid(row=row, column=1, sticky="w", padx=(4, 12))
    status = tk.Label(valve_grid, text="", bg=COLOR_PANEL, anchor="e",
                      font=("Consolas", 9, "bold"))
    status.grid(row=row, column=2, sticky="e")
    valve_labels[tag] = status
  valve_grid.columnconfigure(1, weight=1)

  for tag, desc in PASSIVE_PARTS.items():
    tk.Label(sidebar, text=f"{tag:<6}{desc}", fg="#6b7280", bg=COLOR_PANEL,
             font=("Consolas", 8), justify="left").pack(anchor="w", padx=10)

  def refresh_valve_summary() -> None:
    for tag, lbl in valve_labels.items():
      is_open = get_valve(tag)
      lbl.config(text="OPEN" if is_open else "CLOSED",
                 fg=COLOR_OPEN if is_open else COLOR_CLOSED)

  def poll_telemetry() -> None:
    """Runs on the Tk thread; safe to read values the receiver thread writes."""
    pid_canvas.update_readings()
    for tag, lbl in sensor_labels.items():
      lbl.config(text=format_reading(tag))
    root.after(TELEMETRY_REFRESH_MS, poll_telemetry)

  refresh_valve_summary()
  poll_telemetry()

  # --- Manual control + Settings window ---
  def apply_manual_control(enabled: bool) -> None:
    settings.manual_control = enabled
    pid_canvas.set_controls_enabled(enabled)
    manual_label.config(text=f"MANUAL CONTROL: {'ON' if enabled else 'OFF'}",
                        fg=COLOR_WARN if enabled else "#9ca3af")
    i_send("manual_control", "ON" if enabled else "OFF")

  settings_win: tk.Toplevel | None = None

  def open_settings() -> None:
    nonlocal settings_win
    if settings_win is not None and settings_win.winfo_exists():
      settings_win.deiconify()
      settings_win.lift()
      settings_win.focus_force()
      return

    win = tk.Toplevel(root)
    settings_win = win
    win.title("Settings")
    win.configure(bg=COLOR_PANEL)
    win.resizable(False, False)
    win.transient(root)

    tk.Label(win, text="SETTINGS", fg="#ffffff", bg=COLOR_PANEL,
             font=("Consolas", 12, "bold")).pack(anchor="w", padx=15, pady=(12, 6))

    # ---------------- Section: Manual Control ----------------
    manual_box = settings_section(win, "MANUAL CONTROL")
    manual_var = tk.BooleanVar(value=settings.manual_control)

    def on_manual_changed() -> None:
      if manual_var.get():
        if state.unit_state == "firing":
          messagebox.showwarning("Manual Control",
                                 "Manual valve control cannot be enabled while firing.",
                                 parent=win)
          manual_var.set(False)
          return
        if not messagebox.askokcancel(
            "Enable Manual Control",
            "This unlocks the TOGGLE buttons on every valve.\n\nEnable manual valve control?",
            icon="warning", parent=win):
          manual_var.set(False)
          return
        if not messagebox.askokcancel(
            "Are you sure?",
            "Valves will be commandable by hand. Confirm?",
            icon="warning", parent=win):
          manual_var.set(False)
          return
      apply_manual_control(manual_var.get())
    
    settings_checkbox(manual_box, "Enable manual valve control", manual_var, on_manual_changed)
    settings_note(manual_box, "Off: toggle buttons are locked.\nOn: each valve can be opened / closed by hand.")

    # ---------------- Section: UDP Relay ----------------
    udp_box = settings_section(win, "UDP RELAY")
    host_var = tk.StringVar(value=settings.host_ip)
    port_var = tk.StringVar(value=str(settings.socket))
    udp_status = settings_status(udp_box)
    udp_status.config(text=f"Sending to {settings.host_ip}:{settings.socket}")

    settings_entry(udp_box, "Host", host_var, width=18)
    settings_entry(udp_box, "Port", port_var, width=7)

    def apply_udp() -> None:
      try:
        set_udp_target(host_var.get().strip(), int(port_var.get()))
      except (ValueError, OSError) as exc:
        udp_status.config(text=f"Not applied: {exc}", fg=COLOR_CLOSED)
        return
      udp_status.config(text=f"Sending to {settings.udp_host}:{settings.udp_port}", fg=COLOR_OPEN)

    settings_button(udp_box, "Apply", apply_udp)
    
    tk.Button(win, text="Close", command=win.destroy, bg="#2d2b30", fg="#ffffff",
              activebackground="#3f3c44", activeforeground="#ffffff", relief="flat",
              width=10, font=("Consolas", 9, "bold")).pack(side="bottom", pady=12)

  # --- Camera feed ---
  # Running away is easy, it's the leaving that's hard.
  camera_thread: threading.Thread | None = None
  camera_running = False

  def run_camera_feed() -> None:
    nonlocal camera_running
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    rval, frame = vc.read() if vc.isOpened() else (False, None)

    while rval and camera_running:
      cv2.imshow("preview", frame)
      rval, frame = vc.read()
      key = cv2.waitKey(20)
      if key in (ord("q"), 27) or cv2.getWindowProperty("preview", cv2.WND_PROP_VISIBLE) < 1:
        break

    camera_running = False
    cv2.destroyWindow("preview")
    vc.release()

  def open_monitor() -> None:
    nonlocal camera_thread, camera_running
    if camera_running and camera_thread is not None and camera_thread.is_alive():
      return
    camera_running = True
    camera_thread = threading.Thread(target=run_camera_feed, daemon=True)
    camera_thread.start()

  def show_about() -> None:
    messagebox.showinfo(
        "Acknowledgements",
        f"Blinn Propulsion Labs HMI\n({SOFT_VER})\n\nProgramming:\nAaron"
        " Mathews\nParker Pevehouse\nTroy Martell\nZimife Onovo",
    )

  def read_me() -> None:
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
      webbrowser.open(readme_path.resolve().as_uri())
    else:
      messagebox.showerror("Error", f"Documentation file not found:\n{readme_path}")

  def on_exit() -> None:
    nonlocal camera_running
    camera_running = False
    root.destroy()

  # --- Menu bar ---
  menubar = tk.Menu(root)

  file_menu = tk.Menu(menubar, tearoff=0)
  file_menu.add_command(label="Settings", command=open_settings)
  file_menu.add_command(label="File Integrity", state="disabled")
  file_menu.add_separator()
  file_menu.add_command(label="Exit", command=on_exit)
  menubar.add_cascade(label="File", menu=file_menu)

  view_menu = tk.Menu(menubar, tearoff=0)
  view_menu.add_command(label="Open Telemetry")
  view_menu.add_command(label="Open Monitor", state="disabled")
  menubar.add_cascade(label="View", menu=view_menu)

  tools_menu = tk.Menu(menubar, tearoff=0)
  tools_menu.add_command(label="Teensy Connector")
  tools_menu.add_command(label="Test Connection")
  tools_menu.add_command(label="Simulation Mode")
  menubar.add_cascade(label="Tools", menu=tools_menu)

  help_menu = tk.Menu(menubar, tearoff=0)
  help_menu.add_command(label="Docs", command=read_me)
  help_menu.add_command(label="Acknowledgements", command=show_about)
  menubar.add_cascade(label="Help", menu=help_menu)

  root.config(menu=menubar)
  def toggle_fullscreen(_event=None) -> None:
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

  root.bind("<F11>", toggle_fullscreen)
  root.bind("<Escape>", lambda _e: root.attributes("-fullscreen", False))
  root.protocol("WM_DELETE_WINDOW", on_exit)
  root.mainloop()

# =============================================================================
# Experiments & entry point
# =============================================================================
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
  settings.manual_control = False  # always start locked
  state.runlogs = True
  integrity_checker()

  if EXPERIMENTS.get("Test_Express"):
    test_express()
  if EXPERIMENTS.get("SetUp"):
    create_log()

if __name__ == "__main__":
  init()
  launch_ui()