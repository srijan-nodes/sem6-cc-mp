#!/bin/bash
# Setup test directories and initial files for unionfs testing

set -e

BASE_DIR="/tmp/unionfs_test"
LOWER_DIR="$BASE_DIR/lower"
UPPER_DIR="$BASE_DIR/upper"
MOUNT_DIR="$BASE_DIR/mount"

echo "=== Union FS Setup ==="
echo "Creating test directories..."

# Clean up if already exists
if [ -d "$BASE_DIR" ]; then
    echo "Cleaning existing test directory..."
    # Try to unmount if mounted
    fusermount -u "$MOUNT_DIR" 2>/dev/null || true
    sleep 1
    rm -rf "$BASE_DIR"
fi

# Create directories
mkdir -p "$LOWER_DIR"
mkdir -p "$UPPER_DIR"
mkdir -p "$MOUNT_DIR"

echo "✓ Directories created"

# Create initial files in lower layer
echo "Creating initial files in lower layer..."
echo "file1 content" > "$LOWER_DIR/file1.txt"
echo "file2 content" > "$LOWER_DIR/file2.txt"
mkdir -p "$LOWER_DIR/dir1"
echo "nested file" > "$LOWER_DIR/dir1/nested.txt"

echo "✓ Lower layer files created"

# Create initial files in upper layer
echo "Creating initial files in upper layer..."
echo "upper file" > "$UPPER_DIR/upper_file.txt"

echo "✓ Upper layer files created"

echo ""
echo "=== Setup Complete ==="
echo "Lower dir: $LOWER_DIR"
echo "Upper dir: $UPPER_DIR"
echo "Mount dir: $MOUNT_DIR"
echo ""
echo "Next: Run mount.sh to mount the filesystem"
