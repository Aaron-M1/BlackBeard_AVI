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
import random
import socket
import sys
import threading
import time
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import cv2

# ========== define directory =============
BASE_DIR = Path.home() / "Desktop" / "Blinn Propulsion Labs"

# --- Global Configuration & Experiments ---
soft_ver = "V1.10"
PROGRAM_DEBUG = True
PROGRAM_START = time.perf_counter()
COLOR_TOP = "#161517"
COLOR_BOTTOM = "#252023"
COLOR_OPEN = "#16a34a"    # Green
COLOR_CLOSED = "#dc2626"  # Red

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


def create_vertical_gradient(width: int, height: int, start_hex: str, end_hex: str) -> ImageTk.PhotoImage:
  """Generates a vertical gradient image between two hex colors."""
  # Convert hex colors to RGB tuples
  start_rgb = tuple(int(start_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
  end_rgb = tuple(int(end_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
  
  img = Image.new("RGB", (width, max(1, height)))
  for y in range(height):
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (y / height))
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (y / height))
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (y / height))
    for x in range(width):
      img.putpixel((x, y), (r, g, b))
      
  return ImageTk.PhotoImage(img)

class InteractivePIDCanvas(tk.Canvas):
  """Custom Canvas supporting background PNG loading and drag-and-drop control nodes."""

  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    self.bg_image_raw: Image.Image | None = None
    self.bg_image_tk: ImageTk.PhotoImage | None = None
    self.nodes: dict[str, dict] = {}

    self._drag_data = {"item": None, "x": 0, "y": 0}

    # Canvas bindings for drag and drop (with corrected event sequence strings)
    self.tag_bind("control_node", "<ButtonPress-1>", self._on_node_press)
    self.tag_bind("control_node", "<ButtonRelease-1>", self._on_node_release)
    self.tag_bind("control_node", "<B1-Motion>", self._on_node_drag)

  def load_background_png(self, filepath: str) -> None:
    """Loads a PNG image and displays it scaled to fit the canvas."""
    try:
      self.bg_image_raw = Image.open(filepath)
      self.redraw_background()
    except Exception as e:
      messagebox.showerror("Image Load Error", f"Failed to load image:\n{e}")

  def redraw_background(self) -> None:
    """Rescales and redraws the background PNG without resetting node positions."""
    if self.bg_image_raw is None:
      return

    cw = max(1, self.winfo_width())
    ch = max(1, self.winfo_height())

    img_copy = self.bg_image_raw.copy()
    img_copy.thumbnail((cw, ch), Image.Resampling.LANCZOS)
    self.bg_image_tk = ImageTk.PhotoImage(img_copy)

    self.delete("bg_image")
    self.create_image(
        cw // 2, ch // 2, image=self.bg_image_tk, anchor="center", tags="bg_image"
    )
    self.tag_lower("bg_image")

  def add_control_node(self, node_id: str, label: str, x: int, y: int, is_open: bool = False) -> None:
    """Creates a draggable valve node with status text."""
    tag_name = f"node_{node_id}"
    color = COLOR_OPEN if is_open else COLOR_CLOSED
    status_text = f"{label}: {'OPEN' if is_open else 'CLOSED'}"

    self.create_oval(
        x - 12, y - 12, x + 12, y + 12,
        fill=color, outline="#ffffff", width=2,
        tags=("control_node", tag_name, f"{tag_name}_oval")
    )
    self.create_text(
        x + 18, y,
        text=status_text, fill="#ffffff", anchor="w",
        font=("Consolas", 9, "bold"),
        tags=("control_node", tag_name, f"{tag_name}_text")
    )

    self.nodes[node_id] = {
        "tag": tag_name,
        "label": label,
        "is_open": is_open,
        "x": x,
        "y": y,
    }

  def update_node_status(self, node_id: str, is_open: bool) -> None:
    """Updates the color and text of a control node dynamically."""
    if node_id not in self.nodes:
      return

    node = self.nodes[node_id]
    node["is_open"] = is_open
    color = COLOR_OPEN if is_open else COLOR_CLOSED
    status_text = f"{node['label']}: {'OPEN' if is_open else 'CLOSED'}"

    tag_name = node["tag"]
    self.itemconfig(f"{tag_name}_oval", fill=color)
    self.itemconfig(f"{tag_name}_text", text=status_text)

  def _on_node_press(self, event):
    clicked = self.find_withtag("current")
    if not clicked:
      return
    tags = self.gettags(clicked[0])
    group_tag = next((t for t in tags if t.startswith("node_")), None)

    if group_tag:
      self._drag_data["item"] = group_tag
      self._drag_data["x"] = event.x
      self._drag_data["y"] = event.y

  def _on_node_release(self, event):
    self._drag_data["item"] = None

  def _on_node_drag(self, event):
    group_tag = self._drag_data["item"]
    if not group_tag:
      return

    dx = event.x - self._drag_data["x"]
    dy = event.y - self._drag_data["y"]

    self.move(group_tag, dx, dy)

    self._drag_data["x"] = event.x
    self._drag_data["y"] = event.y

  
def launch_ui() -> None:
  """Primary HMI window: menu bar + camera feed monitor + dynamic 2/3 P&ID canvas."""
  enable_high_dpi()

  root = tk.Tk()
  root.title(f"BPL HMI - {engine.engine_name}")
  root.geometry("1200x750")

  # --- Background Canvas ---
  canvas = tk.Canvas(root, highlightthickness=0)
  canvas.pack(fill="both", expand=True)

  bg_image = None  # Reference to hold generated PhotoImage image in memory

  # --- UI Container ---
  ui_container = tk.Frame(canvas, bg="")
  container_window = canvas.create_window((0, 0), window=ui_container, anchor="nw")

  def update_layout(event):
    nonlocal bg_image
    w, h = event.width, event.height
    if w <= 0 or h <= 0:
      return

    bg_image = create_vertical_gradient(w, h, COLOR_TOP, COLOR_BOTTOM)
    canvas.delete("gradient")
    canvas.create_image(0, 0, image=bg_image, anchor="nw", tags="gradient")
    canvas.tag_lower("gradient")

    canvas.itemconfig(container_window, width=w, height=h)
    pid_canvas.redraw_background()

  canvas.bind("<Configure>", update_layout)

  # Column configuration: Left (2/3 width) and Right (1/3 width)
  ui_container.columnconfigure(0, weight=2)
  ui_container.columnconfigure(1, weight=1)
  ui_container.rowconfigure(0, weight=1)

  # --- Left Panel: 2/3 Interactive P&ID Workspace ---
  pid_frame = tk.LabelFrame(
      ui_container,
      text=" SYSTEM P&ID DIAGRAM ",
      fg="#ffffff",
      bg="#1b1a1d",
      bd=1,
      relief="solid",
      font=("Consolas", 10, "bold"),
  )
  pid_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=15)

  # Top Toolbar inside P&ID Panel
  toolbar = tk.Frame(pid_frame, bg="#1b1a1d")
  toolbar.pack(fill="x", padx=5, pady=2)

  def upload_png():
    file_path = filedialog.askopenfilename(
        title="Select P&ID Diagram Image",
        filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")],
    )
    if file_path:
      pid_canvas.load_background_png(file_path)

  upload_btn = tk.Button(
      toolbar,
      text="Upload P&ID PNG",
      command=upload_png,
      bg="#2d2b30",
      fg="#ffffff",
      relief="flat",
      font=("Consolas", 8, "bold"),
  )
  upload_btn.pack(side="left", padx=2)

  # Dynamic Interactive P&ID Canvas
  pid_canvas = InteractivePIDCanvas(pid_frame, bg="#121113", highlightthickness=0)
  pid_canvas.pack(fill="both", expand=True, padx=5, pady=5)

  # Initialize default valve indicators
  pid_canvas.add_control_node("FMV", "Fuel Main (FMV)", x=100, y=100, is_open=valves.fuel_main)
  pid_canvas.add_control_node("GC_CHECK", "GN2 Check Valve", x=100, y=160, is_open=valves.gc_check)

  # --- Right Panel: 1/3 Telemetry & Control Panel ---
  sidebar_frame = tk.LabelFrame(
      ui_container,
      text=" TELEMETRY & CONTROLS ",
      fg="#ffffff",
      bg="#1b1a1d",
      bd=1,
      relief="solid",
      font=("Consolas", 10, "bold"),
  )
  sidebar_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 15), pady=15)

  tk.Label(
      sidebar_frame,
      text=f"STATUS: {state.unit_state.upper()}",
      fg="#22c55e",
      bg="#1b1a1d",
      font=("Consolas", 12, "bold"),
  ).pack(anchor="w", padx=10, pady=(10, 5))

  # Test Toggle Button for FMV status
  def toggle_fmv():
    valves.fuel_main = not valves.fuel_main
    pid_canvas.update_node_status("FMV", valves.fuel_main)

  toggle_btn = tk.Button(
      sidebar_frame,
      text="Toggle FMV State",
      command=toggle_fmv,
      bg="#2d2b30",
      fg="#ffffff",
      font=("Consolas", 9),
  )
  toggle_btn.pack(anchor="w", padx=10, pady=10)

  # --- Camera Feed Logic ---
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

  # --- Menubar Setup ---
  menubar = tk.Menu(root)

  file_menu = tk.Menu(menubar, tearoff=0)
  file_menu.add_command(label="Upload PNG P&ID", command=upload_png)
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