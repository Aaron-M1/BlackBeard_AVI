"""
Rocket Engine Test Dashboard - Starter Version

This is Step 1: a working window with buttons and simulated live data.
Once this feels good, we'll swap the simulated data for real sensor
input over a serial connection (pyserial) from your DAQ hardware.

Run with:  python rocket_dashboard.py

this was so vibecoded to start with because idkwtf im doing gng
just roll with it, I can fix some of the shit here
"""

import mailbox
import math
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
 
class RocketDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solid Rocket Engine Test Dashboard")
        self.resize(600, 400)
 
        self.running = False
        self.alarm_count = 0
 
        # --- Top-level tabs ---
        # This is the row of menu-style tabs across the top of the window.
        # Add new tabs here later just by calling tabs.addTab(widget, "Name").
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
 
        # Make the tabs themselves taller. Adjust the numbers here to taste.
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                height: 40px;
                min-width: 100px;
                padding: 6px 12px;
            }
        """)
 
        self.tabs.addTab(self._build_operation_tab(), "Operation")
        self.tabs.addTab(self._build_placeholder_tab("Functions"), "Functions")
        self.tabs.addTab(self._build_placeholder_tab("Programming"), "Programming")
        self.tabs.addTab(self._build_placeholder_tab("Telemetry"), "Telemetry")
 
        # Keep the index so we can update this tab's label/color later
        # whenever the alarm count changes.
        self.alarms_tab_index = self.tabs.count()
        self.tabs.addTab(self._build_alarms_tab(), "Alarms")
 
    def _build_operation_tab(self):
        """Everything that used to be the whole window now lives in here,
        as the content of the 'Operation' tab."""
        central = QWidget()
        main_layout = QVBoxLayout(central)
 
        # --- Stats display ---
        stats_box = QGroupBox("Live Stats (simulated for now)")
        stats_layout = QGridLayout(stats_box)

        self.thrust_label = QLabel("0.00 N")
        self.pressure_label = QLabel("0.00 psi")
        self.temperature_label = QLabel("0.00 \u00b0C")
 
        for lbl in (self.thrust_label, self.pressure_label, self.temperature_label):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 22px; font-weight: bold;")
 
        stats_layout.addWidget(QLabel("Thrust:"), 0, 0)
        stats_layout.addWidget(self.thrust_label, 0, 1)
        stats_layout.addWidget(QLabel("Chamber Pressure:"), 1, 0)
        stats_layout.addWidget(self.pressure_label, 1, 1)
        stats_layout.addWidget(QLabel("Nozzle Temp:"), 2, 0)
        stats_layout.addWidget(self.temperature_label, 2, 1)
 
        main_layout.addWidget(stats_box)
 
        # --- Status line ---
        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: gray;")
        main_layout.addWidget(self.status_label)
 
        # --- Buttons ---
        button_row = QHBoxLayout()
 
        self.start_button = QPushButton("Start Test")
        self.stop_button = QPushButton("Stop Test")
        self.reset_button = QPushButton("Reset")
 
        self.stop_button.setEnabled(False)
 
        self.start_button.clicked.connect(self.start_test)
        self.stop_button.clicked.connect(self.stop_test)
        self.reset_button.clicked.connect(self.reset_stats)
 
        button_row.addWidget(self.start_button)
        button_row.addWidget(self.stop_button)
        button_row.addWidget(self.reset_button)
 
        main_layout.addLayout(button_row)
 
        # --- Timer that fakes incoming sensor data ---
        # Later: replace this with a serial read loop from your DAQ.
        self.timer = QTimer()
        self.timer.setInterval(200)  # ms between updates
        self.timer.timeout.connect(self.update_stats)
 
        return central
 
    # Severity definitions used throughout the Alarms tab. Each one maps
    # to a symbol/color pair that fills the icon column of the table.
    # (No image files needed -- these render as text glyphs.)
    SEVERITY_STYLES = {
        "notice": {"symbol": "\u2139", "color": "#1e88e5"},    # blue "i" notice
        "warning": {"symbol": "\u26A0", "color": "#f9a825"},   # amber warning triangle
        "alarm": {"symbol": "\U0001F514", "color": "#e53935"}, # red alarm bell
    }

    def _build_alarms_tab(self):
        """Content for the 'Alarms' tab: a set of sub-tabs (Active Alarms /
        Alarm History / Alarm Timer) modeled on a typical HMI alarm panel,
        with the active alarms shown in a table."""
        self.alarms = []          # active (unacknowledged) alarms
        self.alarm_history = []   # acknowledged alarms, moved here for later

        alarms_widget = QWidget()
        outer_layout = QVBoxLayout(alarms_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # --- Sub-tabs, like the "Active alarms / Alarm history / Alarm
        # timer" row across the top of the reference panel ---
        self.alarms_subtabs = QTabWidget()
        self.alarms_subtabs.addTab(self._build_active_alarms_view(), "Active Alarms")
        self.alarms_subtabs.addTab(self._build_placeholder_tab("Alarm History"), "Alarm History")
        self.alarms_subtabs.addTab(self._build_placeholder_tab("Alarm Timer"), "Alarm Timer")

        outer_layout.addWidget(self.alarms_subtabs)
        return alarms_widget

    def _build_active_alarms_view(self):
        """The actual alarm table: icon / name / event time / message
        columns, plus a small toolbar to acknowledge alarms and a status
        row showing counts -- similar layout to the reference image."""
        view = QWidget()
        layout = QVBoxLayout(view)

        # --- Table ---
        self.alarms_table = QTableWidget(0, 4)
        self.alarms_table.setHorizontalHeaderLabels(["", "Alarm Name", "Event Time", "Message"])
        self.alarms_table.verticalHeader().setVisible(False)
        self.alarms_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.alarms_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.alarms_table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        header = self.alarms_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.alarms_table.setColumnWidth(0, 40)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        layout.addWidget(self.alarms_table, stretch=1)

        # --- Acknowledge / test toolbar ---
        button_row = QHBoxLayout()

        ack_button = QPushButton("Acknowledge Selected")
        ack_button.clicked.connect(self.acknowledge_selected_alarms)

        ack_all_button = QPushButton("Acknowledge All")
        ack_all_button.clicked.connect(self.acknowledge_all_alarms)

        button_row.addWidget(ack_button)
        button_row.addWidget(ack_all_button)
        button_row.addStretch()

        # Stand-ins for real alarm conditions (e.g. over-pressure,
        # over-temp) tripping automatically once you're reading live
        # sensor data. One per severity so you can see all three styles.
        notice_button = QPushButton("Trigger Notice")
        notice_button.clicked.connect(
            lambda: self.add_alarm("Sensor Notice", "Sensor calibration recommended", "notice")
        )
        warning_button = QPushButton("Trigger Warning")
        warning_button.clicked.connect(
            lambda: self.add_alarm("Pressure Warning", "Chamber pressure approaching limit", "warning")
        )
        alarm_button = QPushButton("Trigger Alarm")
        alarm_button.clicked.connect(
            lambda: self.add_alarm("Over-Temp Alarm", "Nozzle temperature exceeded safe limit", "alarm")
        )

        button_row.addWidget(notice_button)
        button_row.addWidget(warning_button)
        button_row.addWidget(alarm_button)

        layout.addLayout(button_row)

        # --- Status row (counts), like the bar along the bottom of the
        # reference panel ---
        status_row = QHBoxLayout()
        self.alarms_total_label = QLabel("Total: 0")
        self.alarms_active_label = QLabel("Active: 0")
        self.alarms_ack_label = QLabel("Acknowledged: 0")

        for lbl in (self.alarms_total_label, self.alarms_active_label, self.alarms_ack_label):
            lbl.setStyleSheet("font-size: 13px; color: #333;")

        status_row.addWidget(self.alarms_total_label)
        status_row.addWidget(self.alarms_active_label)
        status_row.addWidget(self.alarms_ack_label)
        status_row.addStretch()

        layout.addLayout(status_row)

        self._refresh_alarms_table()
        return view

    def add_alarm(self, name="Test Alarm", message="Test alarm triggered", severity="alarm"):
        """Call this whenever a real alarm condition is detected later
        (e.g. chamber pressure or temperature out of safe range).
        severity must be one of: "notice", "warning", "alarm"."""
        self.alarms.append({
            "name": name,
            "message": message,
            "severity": severity,
            "time": QDateTime.currentDateTime().toString("MM/dd/yyyy h:mm:ss AP"),
        })
        self._refresh_alarms_table()

    def acknowledge_selected_alarms(self):
        selected_rows = sorted({index.row() for index in self.alarms_table.selectedIndexes()}, reverse=True)
        for row in selected_rows:
            self.alarm_history.append(self.alarms.pop(row))
        self._refresh_alarms_table()

    def acknowledge_all_alarms(self):
        self.alarm_history.extend(self.alarms)
        self.alarms = []
        self._refresh_alarms_table()

    def clear_alarms(self):
        """Wipe everything -- active and history."""
        self.alarms = []
        self.alarm_history = []
        self._refresh_alarms_table()

    def _refresh_alarms_table(self):
        """Rebuilds the table from self.alarms and updates the counts
        and the tab badge. Called any time the alarm list changes."""
        self.alarms_table.setRowCount(0)

        icon_font = QFont()
        icon_font.setPointSize(14)

        for row, alarm in enumerate(self.alarms):
            self.alarms_table.insertRow(row)

            style = self.SEVERITY_STYLES.get(alarm["severity"], self.SEVERITY_STYLES["alarm"])
            icon_item = QTableWidgetItem(style["symbol"])
            icon_item.setTextAlignment(Qt.AlignCenter)
            icon_item.setForeground(QColor(style["color"]))
            icon_item.setFont(icon_font)

            name_item = QTableWidgetItem(alarm["name"])
            time_item = QTableWidgetItem(alarm["time"])
            message_item = QTableWidgetItem(alarm["message"])

            self.alarms_table.setItem(row, 0, icon_item)
            self.alarms_table.setItem(row, 1, name_item)
            self.alarms_table.setItem(row, 2, time_item)
            self.alarms_table.setItem(row, 3, message_item)

        total = len(self.alarms) + len(self.alarm_history)
        self.alarms_total_label.setText(f"Total: {total}")
        self.alarms_active_label.setText(f"Active: {len(self.alarms)}")
        self.alarms_ack_label.setText(f"Acknowledged: {len(self.alarm_history)}")

        self._update_alarm_badge()

    def _update_alarm_badge(self):
        """This is the actual badge: the tab's text and color update
        to show the current active-alarm count, right next to the tab
        title."""
        count = len(self.alarms)
        if count > 0:
            label = f"Alarms ({count})"
            color = Qt.red
        else:
            label = "Alarms"
            color = Qt.black

        self.tabs.setTabText(self.alarms_tab_index, label)
        self.tabs.tabBar().setTabTextColor(self.alarms_tab_index, color)
 
    def _build_placeholder_tab(self, name):
        """Empty stand-in tab. Swap this out for real content
        (Functions, Programming, Telemetry, Logs) as we build each one."""
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        label = QLabel(f"{name} tab \u2014 coming soon")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: gray;")
        layout.addWidget(label)
        return placeholder
 
    def start_test(self):
        self.running = True
        self.timer.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Running")
        self.status_label.setStyleSheet("font-size: 14px; color: green;")
 
    def stop_test(self):
        self.running = False
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("font-size: 14px; color: darkred;")
 
    def reset_stats(self):
        self.thrust_label.setText("0.00 N")
        self.pressure_label.setText("0.00 psi")
        self.temperature_label.setText("0.00 \u00b0C")
        self.status_label.setText("Status: Idle")
        self.status_label.setStyleSheet("font-size: 14px; color: gray;")
 
    def update_stats(self):
        # Placeholder random walk to simulate a live sensor feed.
        # Swap this out for real values read from pyserial later.
        thrust = random.uniform(800, 1200)
        pressure = random.uniform(400, 600)
        temperature = random.uniform(1200, 1800)
 
        self.thrust_label.setText(f"{thrust:.2f} N")
        self.pressure_label.setText(f"{pressure:.2f} psi")
        self.temperature_label.setText(f"{temperature:.2f} \u00b0C")
 
 
def apply_light_theme(app):
    """Force a plain white/light look regardless of whether Windows is
    set to light or dark mode. Fusion is used because it respects a
    custom QPalette consistently; the default Windows style sometimes
    ignores palette overrides for certain widgets."""
    app.setStyle("Fusion")
 
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#ffffff"))
    palette.setColor(QPalette.WindowText, QColor("#000000"))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.AlternateBase, QColor("#f0f0f0"))
    palette.setColor(QPalette.Text, QColor("#000000"))
    palette.setColor(QPalette.Button, QColor("#f0f0f0"))
    palette.setColor(QPalette.ButtonText, QColor("#000000"))
    palette.setColor(QPalette.Highlight, QColor("#3399ff"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
 
    app.setPalette(palette)
    
def main():
    app = QApplication(sys.argv)
    apply_light_theme(app)
    window = RocketDashboard()
    window.show()
    sys.exit(app.exec())
 
if __name__ == "__main__":
    main()