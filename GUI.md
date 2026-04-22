# Union FS GUI - Modern Testing Interface

A modern PyQt5-based graphical interface for testing the union filesystem implementation.

## Features

- **Modern Dark Theme** - Professional dark UI with smooth animations
- **Intuitive Layout** - Organized tabs for different operations
- **Real-time Output** - Live test execution logs with color coding
- **Non-blocking** - Tests run in background threads without freezing UI
- **Easy Workflow** - One-click setup, mount, test, and cleanup

## Installation

### Requirements
- Python 3.6+
- PyQt5
- FUSE library
- unionfs binary compiled

### Install PyQt5
```bash
pip install PyQt5
```

Or:
```bash
sudo apt-get install python3-pyqt5
```

## Usage

### Launch the GUI
```bash
bash run_gui.sh
```

Or directly:
```bash
python3 gui.py
```

## Interface Overview

### Setup & Mount Tab
- **Setup Test Directories** - Create lower, upper, and mount directories
- **Mount Union FS** - Mount the filesystem
- **Unmount** - Unmount the filesystem
- **Clean & Remove** - Remove all test files

### Operations Tab
#### File Operations
- **Read Files** - Read from both layers
- **Copy-on-Write** - Modify files to test CoW
- **Create File** - Create new files
- **Delete File** - Delete with whiteout markers
- **Truncate File** - Test truncate operation

#### Directory Operations
- **Create Directory** - Create directories
- **Delete Directory** - Delete directories

#### Advanced
- **Large File Test** - 10MB file operations
- **Verify Layers** - Check layer separation

#### Complete Suite
- **Run Complete Test Suite** - Run all tests automatically

### Info Tab
- Overview of union filesystem
- Workflow description
- Feature documentation
- Support information

## Workflow Example

1. **Setup** - Click "Setup Test Directories"
   - Creates `/tmp/unionfs_test/lower`, `/upper`, `/mount`
   - Populates with initial test files

2. **Mount** - Click "Mount Union FS"
   - Mounts the filesystem
   - Ready for testing

3. **Test** - Click individual tests or "Run Complete Test Suite"
   - Watch real-time output in the log area
   - Tests run without blocking the UI

4. **Verify** - Click "Verify Layers"
   - Check that layer separation is maintained

5. **Cleanup** - Click "Clean & Remove Directories"
   - Unmounts and removes all test files

## Output Log

The output area at the bottom shows:
- ✓ Successful operations
- ✗ Failures
- Real-time test progress
- Detailed error messages

Output is color-coded:
- `→` Starting a test
- `✓` Test passed
- `✗` Test failed

## Configuration

Paths are automatically set to:
- Lower Dir: `/tmp/unionfs_test/lower`
- Upper Dir: `/tmp/unionfs_test/upper`
- Mount Point: `/tmp/unionfs_test/mount`

These can be modified by editing the `gui.py` file:
```python
self.base_dir = "/tmp/unionfs_test"
```

## Keyboard Shortcuts

- `Alt+Q` - Quit
- `Alt+Tab` - Switch tabs
- `Ctrl+L` - Clear log (not implemented yet)

## Troubleshooting

### GUI won't start
```bash
python3 -c "import PyQt5"  # Check if PyQt5 is installed
pip install PyQt5           # Install if missing
```

### Permission denied
```bash
sudo bash run_gui.sh  # Run with elevated permissions if needed
```

### Tests not running
- Ensure unionfs binary is compiled: `make`
- Check that test scripts exist in `scripts/` directory
- Verify FUSE library is installed: `libfuse-dev`

## Advantages over CLI

- **Visual Feedback** - See all operations and results at once
- **No Script Knowledge** - Click buttons instead of remembering commands
- **Error Handling** - Clear error messages for any failures
- **Progress Tracking** - Watch tests complete in real-time
- **Professional Appearance** - Modern dark theme

## Technical Details

- Built with **PyQt5** - Cross-platform GUI framework
- Uses **QThread** - Non-blocking test execution
- Real-time Output - Signal/slot mechanism for log updates
- Error Handling - Try/catch with user-friendly messages

## Files

- `gui.py` - Main GUI application
- `run_gui.sh` - Launcher script with dependency check

## Future Enhancements

- [ ] Custom path configuration
- [ ] Test result export (PDF/JSON)
- [ ] Performance metrics display
- [ ] Filesystem browser
- [ ] Live layer synchronization viewer
- [ ] Keyboard shortcuts help dialog
