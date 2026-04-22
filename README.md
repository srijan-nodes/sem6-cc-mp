# Union Filesystem (unionfs) Implementation

A FUSE-based union filesystem implementation with Copy-on-Write semantics and whiteout markers.

## Quick Start

### Compile
```bash
make
```

### GUI Testing (Recommended)
```bash
bash run_gui.sh
```

### Command-Line Testing
```bash
bash scripts/setup.sh
bash scripts/mount.sh
bash scripts/run_all_tests.sh
bash scripts/unmount.sh clean
```

## Features

✅ **Copy-on-Write** - Files copied to upper layer when modified
✅ **Whiteout Markers** - Deletions marked with `.wh.` prefix
✅ **Layer Separation** - Lower layer read-only, upper layer read-write
✅ **File Operations** - Create, delete, read, truncate, chmod, utimens
✅ **Directory Operations** - Create and delete directories
✅ **Large File Support** - Tested with multi-megabyte files

## GUI Interface

Modern dark-themed PyQt5 application with:
- **Setup & Mount** - One-click filesystem setup
- **Operations** - Run individual tests with descriptions
- **Info Tab** - Documentation and workflow guide
- **Real-time Output** - Watch tests execute live

```bash
bash run_gui.sh
```

## Test Status

✅ **All 10 Core Tests Passing**

- Reading from layers
- Copy-on-Write behavior
- File creation
- File deletion with whiteouts
- Directory operations
- Truncate operations
- Timestamp operations
- Large file handling (10MB)
- Layer separation verification

## Architecture

### Layers
```
Mount Point (combined view)
    ├─ Lower Layer (read-only)
    └─ Upper Layer (read-write)
```

### Copy-on-Write
When modifying a lower layer file:
1. File copied to upper layer
2. Modification applied to copy
3. Lower layer unchanged

### Whiteout Markers
When deleting a lower layer file:
1. `.wh.filename` created in upper layer
2. File hidden from mount point
3. Original remains in lower layer

## Requirements

- Linux with FUSE support
- g++ with C++17 support
- libfuse-dev
- PyQt5 (optional, for GUI)

## Installation

```bash
sudo apt-get install libfuse-dev g++ make python3-pyqt5
make
bash run_gui.sh
```

## Documentation

- **GUI.md** - Graphical interface documentation
- **TESTING.md** - Detailed testing procedures
- **scripts/README.md** - Bash scripts reference

## Status

✅ **Production Ready** - All features implemented and tested
