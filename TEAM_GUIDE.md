# Union Filesystem - Team Guide

Complete guide for understanding, building, and testing the union filesystem implementation.

---

## 📋 Table of Contents
1. [What is This?](#what-is-this)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [How It Works](#how-it-works)
4. [File Structure](#file-structure)
5. [Building](#building)
6. [Testing](#testing)
7. [GUI Interface](#gui-interface)
8. [Troubleshooting](#troubleshooting)
9. [Key Concepts](#key-concepts)
10. [Contributing](#contributing)

---

## What is This?

This is a **Union Filesystem** built with **FUSE** (Filesystem in Userspace). It combines two directories:
- **Lower Directory** (read-only layer) - Base files
- **Upper Directory** (read-write layer) - Modifications

Users see a **unified view** of both layers merged together.

### Real-World Example
```
Lower Layer: base_files/
  ├── document.txt
  └── image.png

Upper Layer: modifications/
  ├── document.txt (modified version)
  └── new_file.txt

Mount Point: unionfs/
  ├── document.txt (from upper, modified)
  ├── image.png (from lower, original)
  └── new_file.txt (from upper, new)
```

---

## Quick Start (5 minutes)

### Install Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install libfuse-dev g++ make python3-pyqt5
```

### Compile
```bash
cd /path/to/cc-mp
make
```

### Run GUI (Easiest for teammates)
```bash
bash run_gui.sh
```
Then click buttons in order: Setup → Mount → Run Tests → Verify → Cleanup

### Or Run Tests (Command-line)
```bash
bash scripts/setup.sh          # Create test directories
bash scripts/mount.sh          # Mount filesystem
bash scripts/run_all_tests.sh  # Run all tests
bash scripts/unmount.sh clean  # Cleanup
```

**Done!** All tests should pass ✓

---

## How It Works

### 1. Copy-on-Write (CoW)

**What:** When you modify a file from the lower layer, it's copied to the upper layer first.

**Why:** Keeps the original lower layer unchanged.

**Example:**
```bash
# File originally in lower layer
cat /mount/file.txt
# Output: "original content"

# Modify it through the mount point
echo " modified" >> /mount/file.txt

# Check layers:
cat /lower/file.txt         # Still: "original content"
cat /upper/file.txt         # Now: "original content modified"
```

### 2. Whiteout Markers

**What:** Deleting a file from lower layer creates a `.wh.` marker in upper layer.

**Why:** Hide the lower file without actually deleting it.

**Example:**
```bash
# File exists in lower layer
ls /mount/file.txt          # Shows the file

# Delete through mount point
rm /mount/file.txt

# Check what happened:
ls /lower/file.txt          # Still exists (unchanged)
ls /upper/.wh.file.txt      # Whiteout marker created
ls /mount/file.txt          # Hidden (marked as deleted)
```

### 3. Layer Separation

**Reading:**
- First checks upper layer
- If not found, checks lower layer
- Shows whichever exists

**Writing:**
- Always goes to upper layer
- Copies from lower if needed (CoW)

**Deleting:**
- Upper files: deleted directly
- Lower files: whiteout marker created

---

## File Structure

```
cc-mp/
├── src/                      # Source code
│   ├── main.cpp             # FUSE initialization, operations struct
│   ├── path.cpp             # Read, release operations
│   ├── cow.cpp              # Copy-on-Write, file operations
│   ├── whiteout.cpp         # Whiteout markers, delete operations
│   ├── state.h              # Global state (layer paths)
│   ├── path.h               # Path operations declarations
│   ├── cow.h                # CoW declarations
│   └── whiteout.h           # Whiteout declarations
│
├── scripts/                 # Test scripts
│   ├── setup.sh            # Create test directories
│   ├── mount.sh            # Mount filesystem
│   ├── test_read.sh        # Test reading
│   ├── test_cow.sh         # Test Copy-on-Write
│   ├── test_create.sh      # Test file creation
│   ├── test_mkdir.sh       # Test directory creation
│   ├── test_delete.sh      # Test file deletion
│   ├── test_rmdir.sh       # Test directory deletion
│   ├── test_truncate.sh    # Test truncate
│   ├── test_utimens.sh     # Test timestamps
│   ├── test_large_file.sh  # Test 10MB files
│   ├── verify_layers.sh    # Verify separation
│   ├── unmount.sh          # Unmount
│   └── run_all_tests.sh    # Run all tests
│
├── gui.py                  # Modern PyQt5 GUI
├── run_gui.sh              # GUI launcher
├── Makefile                # Build configuration
├── .gitignore              # Git ignore rules
├── README.md               # Project overview
├── GUI.md                  # GUI documentation
├── TESTING.md              # Testing guide
└── TEAM_GUIDE.md           # This file
```

---

## Building

### Prerequisites
```bash
# Check if you have them
which gcc          # C++ compiler
which make         # Build tool
pkg-config --list-all | grep fuse  # FUSE library
```

### Build
```bash
make              # Compile
make clean        # Remove build artifacts
```

### Output
```
bin/unionfs       # Compiled binary (~74KB)
```

---

## Testing

### Option 1: GUI (Recommended for first-time)
```bash
bash run_gui.sh
```
1. Click "Setup Test Directories"
2. Click "Mount Union FS"
3. Click "Run Complete Test Suite"
4. Watch tests pass in real-time
5. Click "Clean & Remove Directories"

### Option 2: Individual Tests
```bash
bash scripts/setup.sh
bash scripts/mount.sh
bash scripts/test_read.sh      # Test reading
bash scripts/test_cow.sh       # Test Copy-on-Write
bash scripts/test_create.sh    # Test creation
bash scripts/test_delete.sh    # Test deletion
bash scripts/verify_layers.sh  # Verify separation
bash scripts/unmount.sh clean
```

### Option 3: All Tests at Once
```bash
bash scripts/run_all_tests.sh
```

### Test Results
```
✓ PASSED: Reading Files
✓ PASSED: Copy-on-Write
✓ PASSED: File Creation
✓ PASSED: Directory Creation
✓ PASSED: File Deletion
✓ PASSED: Directory Deletion
✓ PASSED: Truncate
✓ PASSED: Timestamps
✓ PASSED: Large Files
✓ PASSED: Layer Verification

All tests passed!
```

---

## GUI Interface

### Tabs

#### Setup & Mount
- **Setup Test Directories** - Creates `/tmp/unionfs_test/` with lower, upper, mount dirs
- **Mount Union FS** - Mounts the filesystem
- **Unmount** - Unmounts
- **Clean & Remove** - Deletes all test files

#### Operations
- **Read Files** - Test reading from both layers
- **Copy-on-Write** - Test CoW behavior
- **Create File** - Test file creation
- **Create Directory** - Test directory creation
- **Delete File** - Test deletion with whiteouts
- **Delete Directory** - Test directory deletion
- **Truncate File** - Test truncate operation
- **Timestamps** - Test utimens
- **Large File Test** - 10MB file test
- **Verify Layers** - Check layer separation
- **Run Complete Test Suite** - All tests

#### Info
- Project overview
- Workflow description
- Key features
- Support info

### Output Log
- Real-time test output
- Green text on dark background
- Status symbols (✓, ✗, →)
- Auto-scrolls to show latest

---

## How Each Test Works

### Read Test
**What:** Reads files from both layers
**How:** Opens files on mount point, verifies content
**Pass Condition:** Can read files from lower and upper

### Copy-on-Write Test
**What:** Modifies a lower-layer file
**How:** Appends text to file from mount point
**Pass Condition:** File copied to upper, lower unchanged

### Create Test
**What:** Creates new file through mount point
**How:** Writes file, verifies it appears only in upper
**Pass Condition:** File only in upper layer

### Delete Test
**What:** Deletes lower-layer file
**How:** Removes file, checks for `.wh.` marker
**Pass Condition:** Whiteout marker created, file hidden

### Large File Test
**What:** Copies 10MB file
**How:** Uses `dd` to create large file
**Pass Condition:** File transfers successfully

### Layer Verification
**What:** Checks layer separation
**How:** Lists files in each layer and mount point
**Pass Condition:** Separation maintained, no conflicts

---

## Troubleshooting

### Build Issues

**Error: `libfuse-dev` not found**
```bash
sudo apt-get install libfuse-dev
```

**Error: `g++ command not found`**
```bash
sudo apt-get install build-essential
```

**Error: Cannot compile**
```bash
make clean
make
```

### Runtime Issues

**Error: Mount failed**
```bash
# Check if already mounted
mount | grep unionfs

# Unmount if needed
fusermount -u /tmp/unionfs_test/mount
```

**Error: Permission denied**
```bash
# Run with sudo
sudo bash run_gui.sh
sudo bash scripts/setup.sh
```

**GUI won't start**
```bash
# Check PyQt5
python3 -c "import PyQt5"

# Install if missing
sudo apt-get install python3-pyqt5
```

**Tests fail**
```bash
# Clean up old test files
rm -rf /tmp/unionfs_test

# Try again
bash scripts/run_all_tests.sh
```

---

## Key Concepts

### FUSE (Filesystem in Userspace)
- Allows userspace programs to implement filesystems
- Our program handles all filesystem operations
- Kernel talks to our program when files are accessed

### Union Mount
- Combines multiple directories into one
- Typically: read-only base + read-write overlay
- Common in containers and live systems

### Copy-on-Write
- File copied only when modified
- Saves space (base files not duplicated)
- Base layer always unchanged

### Whiteout
- Special marker for deleted files
- `.wh.filename` convention
- Hides lower files without deleting them
- Used in Docker, overlayfs

### Layers
- **Lower:** Base layer (read-only)
- **Upper:** Modification layer (read-write)
- **Mount:** Combined view (read-write)

---

## Architecture Diagram

```
Application/User
      ↓
Mount Point (/tmp/unionfs_test/mount)
      ↓
FUSE Kernel Module
      ↓
Our unionfs Program
      ├─ fs_read() → check upper, then lower
      ├─ fs_write() → CoW if needed, write to upper
      ├─ fs_unlink() → whiteout if in lower
      └─ fs_getattr() → resolve path correctly
      ↓
Lower Layer (read-only) + Upper Layer (read-write)
      ↓
Filesystem
```

---

## Implementation Details

### Main Components

**main.cpp** - Initialization
- Sets up FUSE operations struct
- Initializes state (lower/upper paths)
- Calls `fuse_main()` to start filesystem

**path.cpp** - Path Resolution
- `resolve_path()` - Finds file in layers
- Checks upper first, then lower
- Returns "" if not found

**cow.cpp** - Copy-on-Write
- `fs_open()` - CoW on write access
- `fs_write()` - Write operations
- `copy_to_upper()` - Copies lower → upper

**whiteout.cpp** - Deletion
- `fs_unlink()` - File deletion
- `create_whiteout()` - Creates `.wh.` marker
- `is_whiteout()` - Checks if whiteout exists

### Key Functions

| Function | Purpose |
|----------|---------|
| `fs_getattr` | Get file attributes (permissions, size, etc) |
| `fs_read` | Read file content |
| `fs_write` | Write file content |
| `fs_open` | Open file (triggers CoW if needed) |
| `fs_release` | Close file |
| `fs_create` | Create new file |
| `fs_mkdir` | Create directory |
| `fs_unlink` | Delete file |
| `fs_rmdir` | Delete directory |
| `fs_truncate` | Truncate file |
| `fs_chmod` | Change permissions |
| `fs_utimens` | Update timestamps |
| `fs_readdir` | List directory |

---

## Contributing

### Adding a New Operation

1. **Implement in appropriate file:**
   - File ops → `cow.cpp` or `path.cpp`
   - Deletion → `whiteout.cpp`
   - Metadata → `path.cpp`

2. **Add to operations struct in `main.cpp`:**
   ```cpp
   ops.my_operation = fs_my_operation;
   ```

3. **Add test in `scripts/test_myop.sh`:**
   ```bash
   #!/bin/bash
   # Test description
   echo "Testing..."
   # Implementation
   ```

4. **Add to test suite in `scripts/run_all_tests.sh`:**
   ```bash
   run_test "My Operation" "scripts/test_myop.sh"
   ```

### Modifying Existing Operations

1. Edit the function in `src/`
2. Rebuild: `make clean && make`
3. Run tests: `bash scripts/run_all_tests.sh`
4. Verify no regressions

### Testing Your Changes

```bash
make                      # Recompile
bash scripts/setup.sh     # Fresh test environment
bash scripts/mount.sh     # Mount
bash scripts/test_*.sh    # Test specific operation
bash scripts/unmount.sh   # Cleanup
```

---

## Common Workflows

### For Code Review
```bash
make
bash scripts/run_all_tests.sh
```
If all tests pass, code is ready.

### For Debugging
```bash
bash scripts/setup.sh
bash scripts/mount.sh
bash scripts/test_specific.sh  # Run failing test
# Check output, make changes
bash scripts/unmount.sh
```

### For Performance Testing
```bash
bash scripts/test_large_file.sh
# Modify test_large_file.sh to increase size
# Re-run and compare times
```

### For Submission
```bash
make clean
make
bash scripts/run_all_tests.sh
git add .
git commit -m "Union FS implementation"
git push
```

---

## Quick Reference

### Mount Test Filesystem
```bash
bash scripts/setup.sh && bash scripts/mount.sh
```

### Run All Tests
```bash
bash scripts/run_all_tests.sh
```

### Check if Mounted
```bash
mount | grep unionfs
```

### Unmount and Clean
```bash
bash scripts/unmount.sh clean
```

### View Test Results
```bash
cat /tmp/test_output.log
```

### Manual Testing
```bash
# After mounting
cat /tmp/unionfs_test/mount/file.txt          # Read
echo "text" >> /tmp/unionfs_test/mount/file.txt  # Write
rm /tmp/unionfs_test/mount/file.txt           # Delete
ls /tmp/unionfs_test/upper/.wh.*              # Check whiteout
```

---

## Resources

- **FUSE Documentation:** https://github.com/libfuse/libfuse
- **Union Mount Concept:** https://en.wikipedia.org/wiki/Union_mount
- **Linux Filesystem:** https://tldp.org/LDP/intro-linux/html/chap03.html

---

## Support

### For Issues
1. Check troubleshooting section above
2. Run individual tests to isolate problem
3. Check FUSE permissions
4. Review source code comments

### For Questions
1. Check GUI Info tab
2. Read source code comments
3. Review test scripts

---

## Summary

**What:** Union filesystem using FUSE
**How:** Combines read-only lower + read-write upper layers
**Why:** Efficient file management with CoW and whiteout
**Testing:** 10 comprehensive tests, all passing
**Interface:** Modern PyQt5 GUI or bash scripts

**To get started:**
```bash
bash run_gui.sh
```

Then follow the GUI buttons!

---

**Last Updated:** 2026-04-22
**Status:** ✅ Fully Functional
**Tests Passing:** 10/10
