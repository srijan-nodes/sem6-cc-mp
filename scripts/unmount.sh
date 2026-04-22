#!/bin/bash
# Unmount the unionfs and optionally cleanup

set -x

BASE_DIR="/tmp/unionfs_test"
MOUNT_DIR="$BASE_DIR/mount"

CLEANUP=false

if [ "$1" = "clean" ]; then
    CLEANUP=true
fi

echo "=== Unmounting Union FS ==="

if ! mount | grep -q "$MOUNT_DIR"; then
    echo "Filesystem not mounted"
else
    echo "Unmounting $MOUNT_DIR..."
    fusermount -u "$MOUNT_DIR"

    sleep 1

    if mount | grep -q "$MOUNT_DIR"; then
        echo "✗ Unmount failed"
        exit 1
    else
        echo "✓ Unmount successful"
    fi
fi

if [ "$CLEANUP" = true ]; then
    echo ""
    echo "Cleaning up test directories..."
    rm -rf "$BASE_DIR"
    echo "✓ Test directories removed"
else
    echo ""
    echo "Test directories preserved at: $BASE_DIR"
    echo "To clean up later, run: $0 clean"
fi

echo ""
echo "Done"
