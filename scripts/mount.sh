#!/bin/bash
# Mount the unionfs filesystem

set -x

BASE_DIR="/tmp/unionfs_test"
LOWER_DIR="$BASE_DIR/lower"
UPPER_DIR="$BASE_DIR/upper"
MOUNT_DIR="$BASE_DIR/mount"
UNIONFS_BIN="./bin/unionfs"

if [ ! -f "$UNIONFS_BIN" ]; then
    echo "Error: $UNIONFS_BIN not found. Please compile first with 'make'"
    exit 1
fi

echo "=== Mounting Union FS ==="

if ! [ -d "$MOUNT_DIR" ]; then
    echo "Error: Mount directory not found. Run setup.sh first"
    exit 1
fi

# Check if already mounted
if mount | grep -q "$MOUNT_DIR"; then
    echo "Already mounted at $MOUNT_DIR"
    mount | grep "$MOUNT_DIR"
    exit 0
fi

echo "Mounting: $UNIONFS_BIN $LOWER_DIR $UPPER_DIR $MOUNT_DIR"
$UNIONFS_BIN "$LOWER_DIR" "$UPPER_DIR" "$MOUNT_DIR"

sleep 1

if mount | grep -q "$MOUNT_DIR"; then
    echo "✓ Mount successful"
    mount | grep "$MOUNT_DIR"
else
    echo "✗ Mount failed"
    exit 1
fi

echo ""
echo "Mount directory contents:"
ls -la "$MOUNT_DIR"
