# Union Filesystem - Live Demo Instructions

Complete step-by-step guide for demonstrating all features to evaluators.

---

## 📋 Demo Outline

**Total Time:** ~15-20 minutes

1. **Project Overview** (1 min)
2. **Build & Compile** (2 min)
3. **GUI Interface** (1 min)
4. **Layer Stacking Demo** (2 min)
5. **Copy-on-Write (CoW) Demo** (3 min)
6. **Whiteout Marker Demo** (3 min)
7. **POSIX Operations Demo** (3 min)
8. **Test Suite Results** (3 min)
9. **Q&A** (varies)

---

## DEMO 1: Project Overview (1 minute)

### Show Project Structure
```bash
cd ~/cc-mp
tree -L 2 -I '__pycache__'
```

**Expected Output:**
```
cc-mp/
├── src/              ← Source code
├── scripts/          ← Test suite
├── gui.py            ← Modern interface
├── Makefile          ← Build config
├── DESIGN.md         ← Design document
└── TEAM_GUIDE.md     ← Documentation
```

**🎯 Demonstrates:** Project organization and deliverables

---

## DEMO 2: Build & Compile (2 minutes)

### Clean Build
```bash
make clean
make
ls -lh bin/unionfs
```

**Expected Output:**
```
mkdir -p bin
g++ -Wall -std=c++17 -I/usr/include/fuse -D_FILE_OFFSET_BITS=64 \
  -o bin/unionfs src/main.cpp src/path.cpp src/cow.cpp src/whiteout.cpp \
  -lfuse -pthread

bin/unionfs    74K    executable, Linux x86-64
```

**🎯 Demonstrates:** 
- ✅ Compiles successfully
- ✅ Uses C++17 standard
- ✅ Proper FUSE integration
- ✅ Production-quality binary

---

## DEMO 3: GUI Interface (1 minute)

### Launch GUI
```bash
bash run_gui.sh
```

**📸 Show:**
1. **Dark Professional Theme**
   - Modern blue accents
   - Clean layout with grouped sections

2. **Tab Navigation**
   - "Setup & Mount" tab
   - "Operations" tab with all tests
   - "Info" tab with documentation

3. **Button Organization**
   - Setup, Mount, Operations clearly labeled
   - Real-time output area at bottom
   - Status indicators (✓, ✗, →)

**🎯 Demonstrates:**
- ✅ Modern GUI interface (bonus feature)
- ✅ User-friendly design
- ✅ Professional presentation

---

## DEMO 4: Layer Stacking & Merged View (2 minutes)

### Setup Test Environment (Terminal)
```bash
cd ~/cc-mp

# Exit GUI (Alt+Q) if showing GUI demo
# Or open new terminal window

bash scripts/setup.sh
```

**Expected Output:**
```
=== Union FS Setup ===
✓ Directories created
✓ Lower layer files created
✓ Upper layer files created
=== Setup Complete ===
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: Layer Stacking**
- Creates lower_dir (read-only)
- Creates upper_dir (read-write)
- Prepares mount point

### View Individual Layers
```bash
echo "=== LOWER LAYER (read-only) ==="
ls -la /tmp/unionfs_test/lower/

echo "=== UPPER LAYER (read-write) ==="
ls -la /tmp/unionfs_test/upper/
```

**Expected Output:**
```
=== LOWER LAYER (read-only) ===
-rw-r--r-- file1.txt
-rw-r--r-- file2.txt
drwxr-xr-x dir1/

=== UPPER LAYER (read-write) ===
-rw-r--r-- upper_file.txt
```

**🎯 Demonstrates:**
- Different content in each layer
- Ready for mounting

### Mount Union Filesystem
```bash
bash scripts/mount.sh
```

**Expected Output:**
```
Mounting: ./bin/unionfs /tmp/unionfs_test/lower /tmp/unionfs_test/upper /tmp/unionfs_test/mount
✓ Mount successful
unionfs on /tmp/unionfs_test/mount type fuse.unionfs (rw,nosuid,nodev,relatime)
```

### View Merged Result
```bash
echo "=== MERGED VIEW (Mount Point) ==="
ls -la /tmp/unionfs_test/mount/
```

**Expected Output:**
```
=== MERGED VIEW (Mount Point) ===
total 24
-rw-r--r-- file1.txt          ← From lower
-rw-r--r-- file2.txt          ← From lower
drwxr-xr-x dir1/              ← From lower
-rw-r--r-- upper_file.txt     ← From upper
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: Layer Stacking Complete**
- ✓ Lower files visible
- ✓ Upper files visible
- ✓ Unified merged view
- ✓ Merged directories combined

---

## DEMO 5: Copy-on-Write (CoW) - 3 Minutes

### **PART A: Verify File Before Modification**

```bash
echo "=== BEFORE CoW ==="
echo "Lower layer:"
cat /tmp/unionfs_test/lower/file1.txt

echo "Upper layer:"
[ -f /tmp/unionfs_test/upper/file1.txt ] && \
  cat /tmp/unionfs_test/upper/file1.txt || \
  echo "file1.txt NOT in upper (as expected)"
```

**Expected Output:**
```
=== BEFORE CoW ===
Lower layer:
file1 content

Upper layer:
file1.txt NOT in upper (as expected)
```

**🎯 Demonstrates:**
- File exists only in lower layer
- Upper layer doesn't have a copy yet

### **PART B: Modify File Through Mount Point**

```bash
echo "=== TRIGGERING CoW ==="
echo "Appending to file through mount point..."
echo "modified content" >> /tmp/unionfs_test/mount/file1.txt
echo "✓ File modified through mount"
```

**Expected Output:**
```
=== TRIGGERING CoW ===
Appending to file through mount point...
✓ File modified through mount
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: Copy-on-Write Triggered**
- Write operation detected
- CoW mechanism activated

### **PART C: Verify File Copied to Upper**

```bash
echo "=== AFTER CoW ==="
echo "Lower layer (should be UNCHANGED):"
cat /tmp/unionfs_test/lower/file1.txt

echo ""
echo "Upper layer (should now have COPY with modification):"
cat /tmp/unionfs_test/upper/file1.txt

echo ""
echo "Mount point (should show modified version):"
cat /tmp/unionfs_test/mount/file1.txt
```

**Expected Output:**
```
=== AFTER CoW ===
Lower layer (should be UNCHANGED):
file1 content

Upper layer (should now have COPY with modification):
file1 content
modified content

Mount point (should show modified version):
file1 content
modified content
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: Copy-on-Write Complete**
- ✓ File copied to upper layer
- ✓ Modification applied to upper copy
- ✓ Lower layer completely unchanged
- ✓ Modified version visible on mount

---

## DEMO 6: Whiteout Markers (Deletions) - 3 Minutes

### **PART A: Verify File Before Deletion**

```bash
echo "=== BEFORE DELETION ==="
echo "File visible on mount:"
ls -la /tmp/unionfs_test/mount/file2.txt

echo ""
echo "Original in lower layer:"
ls -la /tmp/unionfs_test/lower/file2.txt

echo ""
echo "Whiteout markers in upper:"
ls -la /tmp/unionfs_test/upper/.wh.* 2>/dev/null || echo "None yet"
```

**Expected Output:**
```
=== BEFORE DELETION ===
File visible on mount:
-rw-r--r-- file2.txt

Original in lower layer:
-rw-r--r-- file2.txt

Whiteout markers in upper:
None yet
```

**🎯 Demonstrates:**
- File exists in lower layer
- File visible on mount
- No whiteout markers yet

### **PART B: Delete File Through Mount Point**

```bash
echo "=== DELETING FILE ==="
echo "Removing file through mount point..."
rm /tmp/unionfs_test/mount/file2.txt
echo "✓ File deleted via mount"
```

**Expected Output:**
```
=== DELETING FILE ===
Removing file through mount point...
✓ File deleted via mount
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: Whiteout Mechanism Triggered**
- Delete operation detected
- Whiteout mechanism activated

### **PART C: Verify Whiteout Marker Created**

```bash
echo "=== AFTER DELETION ==="
echo "File hidden from mount point:"
ls /tmp/unionfs_test/mount/file2.txt 2>&1 | grep "No such file"

echo ""
echo "Original STILL in lower layer (unchanged):"
ls -la /tmp/unionfs_test/lower/file2.txt

echo ""
echo "Whiteout marker CREATED in upper layer:"
ls -la /tmp/unionfs_test/upper/.wh.file2.txt

echo ""
echo "Verify marker is empty:"
stat /tmp/unionfs_test/upper/.wh.file2.txt | grep Size
```

**Expected Output:**
```
=== AFTER DELETION ===
File hidden from mount point:
No such file or directory

Original STILL in lower layer (unchanged):
-rw-r--r-- file2.txt

Whiteout marker CREATED in upper layer:
-rw-r--r-- .wh.file2.txt

Verify marker is empty:
Size: 0
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: Whiteout Complete**
- ✓ File hidden from mount (deletion visible)
- ✓ Original preserved in lower layer
- ✓ Whiteout marker (.wh.) created in upper
- ✓ Marker is empty (0 bytes) as designed

---

## DEMO 7: POSIX Operations (3 minutes)

### **Create New File** ✅ REQUIREMENT: create

```bash
echo "=== CREATE OPERATION ==="
echo "Creating new file through mount..."
echo "new file content" > /tmp/unionfs_test/mount/new_file.txt

echo "File visible on mount:"
cat /tmp/unionfs_test/mount/new_file.txt

echo ""
echo "File in upper layer:"
cat /tmp/unionfs_test/upper/new_file.txt

echo ""
echo "NOT in lower layer:"
[ ! -f /tmp/unionfs_test/lower/new_file.txt ] && echo "✓ Confirmed: not in lower"
```

**Expected Output:**
```
=== CREATE OPERATION ===
Creating new file through mount...
new file content

File visible on mount:
new file content

File in upper layer:
new file content

NOT in lower layer:
✓ Confirmed: not in lower
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: create**
- New files created in upper layer only
- Visible on mount point

### **Create Directory** ✅ REQUIREMENT: mkdir

```bash
echo "=== MKDIR OPERATION ==="
echo "Creating directory through mount..."
mkdir -p /tmp/unionfs_test/mount/newdir

echo "Directory visible on mount:"
ls -ld /tmp/unionfs_test/mount/newdir

echo ""
echo "Directory in upper layer:"
ls -ld /tmp/unionfs_test/upper/newdir
```

**Expected Output:**
```
=== MKDIR OPERATION ===
Creating directory through mount...
drwxr-xr-x newdir

Directory visible on mount:
drwxr-xr-x newdir

Directory in upper layer:
drwxr-xr-x newdir
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: mkdir**
- Directories created in upper layer
- Visible on mount

### **File Permissions** ✅ REQUIREMENT: getattr + chmod

```bash
echo "=== GETATTR & CHMOD OPERATIONS ==="
echo "Get attributes:"
stat /tmp/unionfs_test/mount/new_file.txt | grep Access

echo ""
echo "Change permissions:"
chmod 644 /tmp/unionfs_test/mount/new_file.txt
stat /tmp/unionfs_test/mount/new_file.txt | grep Access
```

**Expected Output:**
```
=== GETATTR & CHMOD OPERATIONS ===
Get attributes:
Access: (0644/-rw-r--r--)

Change permissions:
Access: (0644/-rw-r--r--)
```

**🎯 Demonstrates:** ✅ **REQUIREMENTS: getattr, chmod**
- Attributes readable
- Permissions modifiable

### **Directory Listing** ✅ REQUIREMENT: readdir

```bash
echo "=== READDIR OPERATION ==="
echo "List mount directory (merged view):"
ls -la /tmp/unionfs_test/mount/ | head -15
```

**Expected Output:**
```
=== READDIR OPERATION ===
List mount directory (merged view):
total 24
drwxr-xr-x . (current)
drwxr-xr-x .. (parent)
-rw-r--r-- file1.txt     ← from lower (modified)
-rw-r--r-- upper_file.txt ← from upper (original)
drwxr-xr-x dir1/         ← from lower
drwxr-xr-x newdir        ← from upper (new)
-rw-r--r-- new_file.txt  ← from upper (new)
```

**🎯 Demonstrates:** ✅ **REQUIREMENT: readdir**
- Merged directory listing
- Files from both layers visible
- Deleted files hidden

---

## DEMO 8: Complete Test Suite (3 minutes)

### Run All Tests
```bash
bash scripts/run_all_tests.sh 2>&1 | tail -40
```

**Expected Output:**
```
╔════════════════════════════════════════════════╗
║     Union FS - Complete Test Suite              ║
╚════════════════════════════════════════════════╝

Step 1: Setup
✓ Setup complete

Step 2: Mount
✓ Mount successful

Step 3: Running Tests
════════════════════════════════════════════════

Running: Reading Files
✓ PASSED: Reading Files

Running: Copy-on-Write
✓ PASSED: Copy-on-Write

Running: File Creation
✓ PASSED: File Creation

Running: Directory Creation
✓ PASSED: Directory Creation

Running: File Deletion
✓ PASSED: File Deletion

Running: Directory Deletion
✓ PASSED: Directory Deletion

Running: Truncate
✓ PASSED: Truncate

Running: Timestamps
✓ PASSED: Timestamps

Running: Large Files
✓ PASSED: Large Files

Running: Layer Verification
✓ PASSED: Layer Verification

════════════════════════════════════════════════

Test Summary
════════════════════════════════════════════════
Passed: 10
Failed: 0

All tests passed!
```

**🎯 Demonstrates:** ✅ **ALL REQUIREMENTS VERIFIED**
- ✓ 10/10 tests passing
- ✓ Copy-on-Write verified
- ✓ Whiteout mechanism verified
- ✓ Layer separation verified
- ✓ POSIX operations verified
- ✓ Large file handling verified

---

## DEMO 9: Design & Documentation (Optional - 2 minutes)

### Show Design Document
```bash
cat DESIGN.md | head -50
```

**📸 Show:**
1. System architecture diagram
2. Path resolution algorithm
3. CoW implementation details
4. Whiteout mechanism explanation
5. Edge case handling

**🎯 Demonstrates:**
- ✅ Comprehensive design documentation
- ✅ Technical depth and understanding
- ✅ Professional engineering approach

---

## DEMO 10: Show Project Files

### Source Code Structure
```bash
echo "=== SOURCE FILES ==="
wc -l src/*.cpp src/*.h | tail -1
echo ""
echo "=== KEY FILES ==="
ls -lh src/ | grep -E '\.(cpp|h)$'
```

**Expected Output:**
```
=== SOURCE FILES ===
    600 total lines of code

=== KEY FILES ===
main.cpp       (60 lines)   - FUSE initialization
path.cpp       (150 lines)  - Path resolution & read
cow.cpp        (120 lines)  - Copy-on-Write
whiteout.cpp   (110 lines)  - Deletion/whiteout
state.h        (20 lines)   - Global state
[other headers]
```

**🎯 Demonstrates:**
- ✅ Well-organized codebase
- ✅ Appropriate complexity
- ✅ Clean separation of concerns

---

## 📋 Quick Reference: Requirements Checklist

Print this or display during demo:

```
CORE REQUIREMENTS DEMONSTRATION
================================

✅ 1. LAYER STACKING
   - Demo Point: Shows merged view combining lower + upper
   - Location: DEMO 4

✅ 2. COPY-ON-WRITE
   - Demo Point: Modifies lower file, copies to upper
   - Location: DEMO 5 (Parts A, B, C)

✅ 3. WHITEOUT MECHANISM  
   - Demo Point: Deletes lower file, creates .wh. marker
   - Location: DEMO 6 (Parts A, B, C)

✅ 4. POSIX OPERATIONS
   - getattr: DEMO 7
   - readdir: DEMO 7
   - read: DEMO 5 (cat command)
   - write: DEMO 5 (echo >>)
   - create: DEMO 7
   - unlink: DEMO 6
   - mkdir: DEMO 7
   - rmdir: Test suite

✅ 5. BUILD & DELIVERABLES
   - Makefile: DEMO 2
   - Design Document: DEMO 9
   - Source Code: DEMO 10
```

---

## 🎬 Pro Tips for Live Demo

### Before Demo
```bash
# Test everything works
bash scripts/run_all_tests.sh
# Clean up for fresh start
bash scripts/unmount.sh clean 2>/dev/null || true
```

### During Demo
1. **Type slowly** - Show what you're doing
2. **Explain each output** - Connect to requirements
3. **Use full paths** - Avoid confusion
4. **Point and highlight** - Use echo or visual markers
5. **Keep terminal large** - Easy to read for audience

### If Something Goes Wrong
```bash
# Quick recovery
fusermount -u /tmp/unionfs_test/mount 2>/dev/null
rm -rf /tmp/unionfs_test
bash scripts/setup.sh
bash scripts/mount.sh
# Continue from appropriate demo point
```

### Preparation Checklist
- [ ] Compile: `make clean && make`
- [ ] Test: `bash scripts/run_all_tests.sh`
- [ ] Cleanup: `bash scripts/unmount.sh clean`
- [ ] Verify GUI works: `bash run_gui.sh` (if showing)
- [ ] Review design document
- [ ] Have print-out of requirements checklist

---

## 📊 Time Breakdown

| Demo | Duration | Key Points |
|------|----------|-----------|
| Overview | 1 min | Structure & organization |
| Build | 2 min | Compilation & FUSE integration |
| GUI | 1 min | Modern interface |
| Layer Stacking | 2 min | Merged view |
| CoW | 3 min | File copying on write |
| Whiteout | 3 min | Deletion with markers |
| POSIX Ops | 3 min | File operations |
| Tests | 3 min | All validations |
| Docs | 2 min | Design & documentation |
| **Total** | **20 min** | Complete coverage |

---

## ✅ Success Criteria

By end of demo, evaluators should see:
- ✅ Layer merging working
- ✅ CoW in action (file copied to upper)
- ✅ Whiteout markers created (.wh. files)
- ✅ File operations functional
- ✅ All tests passing
- ✅ Professional documentation
- ✅ Clean, well-organized code

---

**Demo Status: Ready to Present!** 🎉

All features demonstrated, all requirements covered, all tests passing.
