testing scripts
# Run everything automatically
bash scripts/run_all_tests.sh

# Or manually:
bash scripts/setup.sh
bash scripts/mount.sh
bash scripts/test_cow.sh          # Run individual tests
bash scripts/verify_layers.sh
bash scripts/unmount.sh clean



# Union Filesystem Testing Guide

This document contains commands to test the unionfs implementation.

## Setup

### 1. Create test directories

```bash
# Create temporary directories for testing
mkdir -p /tmp/unionfs_test/lower
mkdir -p /tmp/unionfs_test/upper
mkdir -p /tmp/unionfs_test/mount

# Create initial files in lower layer (read-only)
echo "file1 content" > /tmp/unionfs_test/lower/file1.txt
echo "file2 content" > /tmp/unionfs_test/lower/file2.txt
mkdir -p /tmp/unionfs_test/lower/dir1
echo "nested file" > /tmp/unionfs_test/lower/dir1/nested.txt

# Create initial files in upper layer (writable)
echo "upper file" > /tmp/unionfs_test/upper/upper_file.txt
```

### 2. Mount the filesystem

```bash
# From the cc-mp directory, mount the union filesystem
./bin/unionfs /tmp/unionfs_test/lower /tmp/unionfs_test/upper /tmp/unionfs_test/mount

# Verify mount succeeded
mount | grep unionfs
```

## Basic Operations Tests

### 3. Test reading files

```bash
# List files in mount point (should see from both layers)
ls -la /tmp/unionfs_test/mount/

# Read file from lower layer
cat /tmp/unionfs_test/mount/file1.txt

# Read file from upper layer
cat /tmp/unionfs_test/mount/upper_file.txt

# Read nested file from lower layer
cat /tmp/unionfs_test/mount/dir1/nested.txt
```

### 4. Test writing to files (Copy-on-Write)

```bash
# Modify a file from lower layer - should copy to upper layer first
echo "modified content" >> /tmp/unionfs_test/mount/file1.txt

# Verify the file was modified
cat /tmp/unionfs_test/mount/file1.txt

# Verify it was copied to upper layer
cat /tmp/unionfs_test/upper/file1.txt

# Verify original lower layer file is unchanged
cat /tmp/unionfs_test/lower/file1.txt
```

### 5. Test file creation

```bash
# Create a new file in mount point (goes to upper layer)
echo "new file content" > /tmp/unionfs_test/mount/newfile.txt

# Verify file is readable from mount point
cat /tmp/unionfs_test/mount/newfile.txt

# Verify file exists in upper layer
cat /tmp/unionfs_test/upper/newfile.txt

# Verify file does not exist in lower layer
ls /tmp/unionfs_test/lower/newfile.txt 2>&1  # Should show "No such file"
```

### 6. Test directory operations

```bash
# Create a new directory
mkdir -p /tmp/unionfs_test/mount/newdir

# Verify it exists in upper layer
ls -la /tmp/unionfs_test/upper/newdir

# Create files in the new directory
echo "file in new dir" > /tmp/unionfs_test/mount/newdir/file.txt
cat /tmp/unionfs_test/mount/newdir/file.txt
```

### 7. Test file deletion with whiteout markers

```bash
# Delete a file from lower layer - creates whiteout marker
rm /tmp/unionfs_test/mount/file1.txt

# Verify file is no longer visible
ls /tmp/unionfs_test/mount/file1.txt 2>&1  # Should show "No such file"

# Verify whiteout marker exists in upper layer
ls -la /tmp/unionfs_test/upper/ | grep "\.wh\.file1"

# Verify original file still exists in lower layer
cat /tmp/unionfs_test/lower/file1.txt
```

### 8. Test directory deletion

```bash
# Delete a directory from lower layer
rmdir /tmp/unionfs_test/mount/dir1  # Will fail if not empty

# First delete nested file
rm /tmp/unionfs_test/mount/dir1/nested.txt

# Then delete directory
rmdir /tmp/unionfs_test/mount/dir1

# Verify it's no longer visible
ls /tmp/unionfs_test/mount/dir1 2>&1  # Should show "No such file"

# Verify whiteout marker exists
ls -la /tmp/unionfs_test/upper/ | grep "\.wh\.dir1"
```

### 9. Test truncate operation

```bash
# Create a test file
echo "This is a longer file content" > /tmp/unionfs_test/mount/truncate_test.txt

# Truncate the file to 5 bytes
truncate -s 5 /tmp/unionfs_test/mount/truncate_test.txt

# Verify the truncation
cat /tmp/unionfs_test/mount/truncate_test.txt

# Verify file was copied to upper layer
ls -la /tmp/unionfs_test/upper/truncate_test.txt
```

### 10. Test file permissions (chmod)

```bash
# Create a test file
echo "test" > /tmp/unionfs_test/mount/chmod_test.txt

# Change permissions
chmod 644 /tmp/unionfs_test/mount/chmod_test.txt

# Verify permissions on mounted file
ls -l /tmp/unionfs_test/mount/chmod_test.txt

# Change to read-only
chmod 444 /tmp/unionfs_test/mount/chmod_test.txt

# Try to modify (should fail)
echo "change" >> /tmp/unionfs_test/mount/chmod_test.txt 2>&1

# Restore permissions
chmod 644 /tmp/unionfs_test/mount/chmod_test.txt
```

### 11. Test timestamp operations (utimens)

```bash
# Create a test file
echo "test" > /tmp/unionfs_test/mount/utime_test.txt

# Change access and modification time
touch -t 202301010000 /tmp/unionfs_test/mount/utime_test.txt

# Verify the timestamp
ls -l /tmp/unionfs_test/mount/utime_test.txt

# Set current time
touch /tmp/unionfs_test/mount/utime_test.txt
ls -l /tmp/unionfs_test/mount/utime_test.txt
```

### 12. Test large file operations

```bash
# Create a large file (10MB) in mount point
dd if=/dev/zero of=/tmp/unionfs_test/mount/largefile.bin bs=1M count=10

# Verify file size
ls -lh /tmp/unionfs_test/mount/largefile.bin

# Verify it's in upper layer
ls -lh /tmp/unionfs_test/upper/largefile.bin
```

### 13. Verify layer separation

```bash
# Check what's in each layer
echo "=== Lower layer ==="
find /tmp/unionfs_test/lower -type f | sort

echo "=== Upper layer ==="
find /tmp/unionfs_test/upper -type f | sort

echo "=== Mount point ==="
find /tmp/unionfs_test/mount -type f | sort
```

## Cleanup

### 14. Unmount the filesystem

```bash
# Unmount the unionfs
fusermount -u /tmp/unionfs_test/mount

# Verify unmount succeeded
mount | grep unionfs  # Should show nothing

# Remove test directories
rm -rf /tmp/unionfs_test
```

## Debugging

### Check FUSE status

```bash
# List all mounted FUSE filesystems
mount -t fuse.unionfs

# Check FUSE debug info
cat /proc/fs/fuse/connections
```

### Enable verbose output

```bash
# Mount with verbose FUSE options
./bin/unionfs /tmp/unionfs_test/lower /tmp/unionfs_test/upper /tmp/unionfs_test/mount -d -f

# Press Ctrl+C to unmount
```

### Check file descriptors

```bash
# While filesystem is mounted, check open files
lsof | grep unionfs

# Or check process info
ps aux | grep unionfs
```

## Advanced Tests

### Test concurrent access

```bash
# Terminal 1: Mount filesystem
./bin/unionfs /tmp/unionfs_test/lower /tmp/unionfs_test/upper /tmp/unionfs_test/mount

# Terminal 2: Create files while reading
for i in {1..10}; do
  echo "File $i" > /tmp/unionfs_test/mount/file_$i.txt &
done

# Terminal 2: Read files concurrently
for i in {1..10}; do
  cat /tmp/unionfs_test/mount/file_$i.txt &
done

wait
```

### Test error conditions

```bash
# Try to write to read-only file
chmod 444 /tmp/unionfs_test/mount/file.txt
echo "test" >> /tmp/unionfs_test/mount/file.txt 2>&1  # Should fail

# Try to access non-existent file
cat /tmp/unionfs_test/mount/nonexistent.txt 2>&1  # Should fail

# Try to delete non-existent file
rm /tmp/unionfs_test/mount/nonexistent.txt 2>&1  # Should fail
```

## Expected Behavior Summary

| Operation | Expected Result |
|-----------|-----------------|
| Read from lower | File is read directly from lower layer |
| Read from upper | File is read directly from upper layer |
| Write to lower | File copied to upper, then modified |
| Create file | File created in upper layer only |
| Delete from lower | Whiteout marker created in upper layer |
| Delete from upper | File deleted from upper layer |
| Directory ops | Operations work on upper layer |
| Concurrent access | Multiple operations work simultaneously |
| Layer separation | Changes in upper don't affect lower |

