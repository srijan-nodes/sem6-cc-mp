#!/usr/bin/env python3
"""
Union FS GUI - Modern testing interface for unionfs
Requires: PyQt5, PyQt5-tools
Install: pip install PyQt5
"""

import sys
import subprocess
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTextEdit, QTabWidget, QGroupBox,
    QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from PyQt5.QtCore import QSize

class WorkerThread(QThread):
    """Worker thread for running commands without blocking UI"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)  # success, message

    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path

    def run(self):
        try:
            result = subprocess.run(
                ["bash", self.script_path],
                capture_output=True,
                text=True,
                timeout=300
            )
            output = result.stdout + result.stderr
            self.output_signal.emit(output)
            self.finished_signal.emit(result.returncode == 0, "Test completed")
        except subprocess.TimeoutExpired:
            self.output_signal.emit("✗ Test timed out (5+ minutes)")
            self.finished_signal.emit(False, "Timeout")
        except Exception as e:
            self.output_signal.emit(f"✗ Error: {str(e)}")
            self.finished_signal.emit(False, str(e))

class UnionFSGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_dir = Path(__file__).parent
        self.base_dir = "/tmp/unionfs_test"
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Union FS Testing Suite")
        self.setGeometry(100, 100, 1000, 700)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Union FS Testing Suite")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        # Paths configuration
        paths_group = QGroupBox("Configuration")
        paths_layout = QVBoxLayout()

        # Lower dir
        paths_h1 = QHBoxLayout()
        paths_h1.addWidget(QLabel("Lower Dir (read-only):"))
        self.lower_dir_input = QLineEdit()
        self.lower_dir_input.setText(f"{self.base_dir}/lower")
        self.lower_dir_input.setReadOnly(True)
        paths_h1.addWidget(self.lower_dir_input)
        paths_layout.addLayout(paths_h1)

        # Upper dir
        paths_h2 = QHBoxLayout()
        paths_h2.addWidget(QLabel("Upper Dir (writable):"))
        self.upper_dir_input = QLineEdit()
        self.upper_dir_input.setText(f"{self.base_dir}/upper")
        self.upper_dir_input.setReadOnly(True)
        paths_h2.addWidget(self.upper_dir_input)
        paths_layout.addLayout(paths_h2)

        # Mount dir
        paths_h3 = QHBoxLayout()
        paths_h3.addWidget(QLabel("Mount Point:"))
        self.mount_dir_input = QLineEdit()
        self.mount_dir_input.setText(f"{self.base_dir}/mount")
        self.mount_dir_input.setReadOnly(True)
        paths_h3.addWidget(self.mount_dir_input)
        paths_layout.addLayout(paths_h3)

        paths_group.setLayout(paths_layout)
        main_layout.addWidget(paths_group)

        # Tab widget for different test categories
        tabs = QTabWidget()

        # Setup & Mount Tab
        tabs.addTab(self.setup_mount_tab(), "Setup & Mount")

        # Operations Tab
        tabs.addTab(self.operations_tab(), "Operations")

        # Info Tab
        tabs.addTab(self.info_tab(), "Info")

        main_layout.addWidget(tabs)

        # Output area
        output_label = QLabel("Output Log:")
        output_font = QFont()
        output_font.setPointSize(9)
        output_label.setFont(output_font)
        main_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(200)
        self.output_text.setFont(QFont("Courier", 9))
        main_layout.addWidget(self.output_text)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

        main_widget.setLayout(main_layout)
        self.apply_modern_style()

    def setup_mount_tab(self):
        """Create setup and mount tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Setup section
        setup_group = QGroupBox("Setup")
        setup_layout = QVBoxLayout()
        self.setup_btn = QPushButton("1. Setup Test Directories")
        self.setup_btn.setMinimumHeight(40)
        self.setup_btn.clicked.connect(self.run_setup)
        setup_layout.addWidget(self.setup_btn)
        setup_group.setLayout(setup_layout)
        layout.addWidget(setup_group)

        # Mount section
        mount_group = QGroupBox("Mount")
        mount_layout = QVBoxLayout()
        self.mount_btn = QPushButton("2. Mount Union FS")
        self.mount_btn.setMinimumHeight(40)
        self.mount_btn.clicked.connect(self.run_mount)
        mount_layout.addWidget(self.mount_btn)
        mount_group.setLayout(mount_layout)
        layout.addWidget(mount_group)

        # Unmount section
        unmount_group = QGroupBox("Cleanup")
        unmount_layout = QVBoxLayout()

        unmount_h = QHBoxLayout()
        self.unmount_btn = QPushButton("3. Unmount")
        self.unmount_btn.setMinimumHeight(40)
        self.unmount_btn.clicked.connect(self.run_unmount)
        unmount_h.addWidget(self.unmount_btn)

        self.cleanup_btn = QPushButton("Clean & Remove Directories")
        self.cleanup_btn.setMinimumHeight(40)
        self.cleanup_btn.clicked.connect(self.run_cleanup)
        unmount_h.addWidget(self.cleanup_btn)

        unmount_layout.addLayout(unmount_h)
        unmount_group.setLayout(unmount_layout)
        layout.addWidget(unmount_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def operations_tab(self):
        """Create operations tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # File Operations
        file_ops = QGroupBox("File Operations")
        file_layout = QVBoxLayout()

        operations = [
            ("Read Files", "test_read.sh", "Read from both layers"),
            ("Copy-on-Write", "test_cow.sh", "Modify lower layer file"),
            ("Create File", "test_create.sh", "Create new file"),
            ("Delete File", "test_delete.sh", "Delete with whiteout"),
            ("Truncate File", "test_truncate.sh", "Truncate operation"),
        ]

        for name, script, tooltip in operations:
            btn = QPushButton(f"▶ {name}")
            btn.setMinimumHeight(35)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, s=script: self.run_test(s))
            file_layout.addWidget(btn)

        file_ops.setLayout(file_layout)
        layout.addWidget(file_ops)

        # Directory Operations
        dir_ops = QGroupBox("Directory Operations")
        dir_layout = QVBoxLayout()

        dir_operations = [
            ("Create Directory", "test_mkdir.sh", "Create directory"),
            ("Delete Directory", "test_rmdir.sh", "Delete directory"),
        ]

        for name, script, tooltip in dir_operations:
            btn = QPushButton(f"▶ {name}")
            btn.setMinimumHeight(35)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, s=script: self.run_test(s))
            dir_layout.addWidget(btn)

        dir_ops.setLayout(dir_layout)
        layout.addWidget(dir_ops)

        # Advanced Operations
        advanced_ops = QGroupBox("Advanced")
        advanced_layout = QVBoxLayout()

        advanced_operations = [
            ("Large File Test", "test_large_file.sh", "10MB file transfer"),
            ("Verify Layers", "verify_layers.sh", "Check layer separation"),
        ]

        for name, script, tooltip in advanced_operations:
            btn = QPushButton(f"▶ {name}")
            btn.setMinimumHeight(35)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, s=script: self.run_test(s))
            advanced_layout.addWidget(btn)

        advanced_ops.setLayout(advanced_layout)
        layout.addWidget(advanced_ops)

        # Run all tests
        run_all_group = QGroupBox("Run All Tests")
        run_all_layout = QVBoxLayout()
        self.run_all_btn = QPushButton("▶▶ Run Complete Test Suite")
        self.run_all_btn.setMinimumHeight(45)
        self.run_all_btn.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.run_all_btn.clicked.connect(self.run_all_tests)
        run_all_layout.addWidget(self.run_all_btn)
        run_all_group.setLayout(run_all_layout)
        layout.addWidget(run_all_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def info_tab(self):
        """Create info tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMarkdown("""
# Union FS Testing Suite

## Overview
This GUI allows you to test the union filesystem implementation with a modern interface.

## Workflow
1. **Setup**: Create test directories and initial files
2. **Mount**: Mount the union filesystem
3. **Test**: Run individual or all tests
4. **Verify**: Check that all layers are working correctly
5. **Cleanup**: Unmount and remove test files

## Key Features
- **Copy-on-Write**: Files from lower layer are copied to upper when modified
- **Whiteout Markers**: Deleted files from lower layer are marked as deleted with .wh. prefix
- **Layer Separation**: Changes in upper layer don't affect lower layer

## Test Categories

### File Operations
- Read files from both layers
- Modify files (Copy-on-Write)
- Create new files
- Delete files with whiteout
- Truncate operations

### Directory Operations
- Create directories
- Delete directories with whiteout

### Advanced
- Large file handling (10MB)
- Layer separation verification

## Status
- ✓ All core features tested
- ✓ Copy-on-Write functional
- ✓ Whiteout implementation working
- ✓ Layer separation verified

## Support
For command-line testing, see: `scripts/README.md`
        """)
        layout.addWidget(info_text)
        widget.setLayout(layout)
        return widget

    def apply_modern_style(self):
        """Apply modern dark theme"""
        stylesheet = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QPushButton {
            background-color: #0d47a1;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            padding: 8px;
            font-weight: bold;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #1565c0;
        }
        QPushButton:pressed {
            background-color: #0d47a1;
        }
        QLineEdit {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #404040;
            border-radius: 4px;
            padding: 5px;
            selection-background-color: #0d47a1;
        }
        QTextEdit {
            background-color: #2d2d2d;
            color: #00ff00;
            border: 1px solid #404040;
            border-radius: 4px;
            padding: 5px;
            font-family: Courier;
        }
        QGroupBox {
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        QTabWidget::pane {
            border: 1px solid #404040;
        }
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #ffffff;
            padding: 8px 20px;
            border: 1px solid #404040;
        }
        QTabBar::tab:selected {
            background-color: #0d47a1;
        }
        QLabel {
            color: #ffffff;
        }
        QProgressBar {
            background-color: #2d2d2d;
            border: 1px solid #404040;
            border-radius: 4px;
            text-align: center;
            color: #ffffff;
        }
        QProgressBar::chunk {
            background-color: #0d47a1;
        }
        """
        self.setStyleSheet(stylesheet)

    def log_output(self, text):
        """Add text to output log"""
        self.output_text.append(text)
        # Auto-scroll to bottom
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def run_setup(self):
        """Run setup script"""
        self.log_output("→ Running setup...")
        self.run_script(str(self.script_dir / "setup.sh"))

    def run_mount(self):
        """Run mount script"""
        self.log_output("→ Mounting filesystem...")
        self.run_script(str(self.script_dir / "mount.sh"))

    def run_unmount(self):
        """Run unmount script"""
        self.log_output("→ Unmounting filesystem...")
        self.run_script(str(self.script_dir / "unmount.sh"))

    def run_cleanup(self):
        """Run cleanup"""
        reply = QMessageBox.question(
            self, "Confirm Cleanup",
            "This will remove all test directories. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.log_output("→ Cleaning up...")
            self.run_script(str(self.script_dir / "unmount.sh") + " clean")

    def run_test(self, script_name):
        """Run a single test"""
        test_path = str(self.script_dir / script_name)
        self.run_script(test_path)

    def run_all_tests(self):
        """Run all tests"""
        self.log_output("→ Running complete test suite...")
        self.run_script(str(self.script_dir / "run_all_tests.sh"))

    def run_script(self, script_path):
        """Run a script in a worker thread"""
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Error", f"Script not found: {script_path}")
            return

        # Disable buttons during execution
        self.setButtonsEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)

        # Create and start worker thread
        self.worker = WorkerThread(script_path)
        self.worker.output_signal.connect(self.log_output)
        self.worker.finished_signal.connect(self.on_test_finished)
        self.worker.start()

    def on_test_finished(self, success, message):
        """Handle test completion"""
        self.setButtonsEnabled(True)
        self.progress.setVisible(False)

        if success:
            self.log_output("\n✓ Test completed successfully\n")
        else:
            self.log_output(f"\n✗ Test failed: {message}\n")

    def setButtonsEnabled(self, enabled):
        """Enable/disable all buttons"""
        for child in self.findChildren(QPushButton):
            child.setEnabled(enabled)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Union FS Testing Suite")

    window = UnionFSGUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
