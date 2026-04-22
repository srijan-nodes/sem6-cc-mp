#!/bin/bash
# Verify layer separation and integrity

set -x

BASE_DIR="/tmp/unionfs_test"
LOWER_DIR="$BASE_DIR/lower"
UPPER_DIR="$BASE_DIR/upper"
MOUNT_DIR="$BASE_DIR/mount"

echo "=== Verify Layer Separation ==="

if ! mount | grep -q "$MOUNT_DIR"; then
    echo "✗ Filesystem not mounted. Run mount.sh first"
    exit 1
fi

echo ""
echo "1. Files in lower layer:"
find "$LOWER_DIR" -type f 2>/dev/null | sort
LOWER_COUNT=$(find "$LOWER_DIR" -type f 2>/dev/null | wc -l)
echo "   Total: $LOWER_COUNT files"

echo ""
echo "2. Files in upper layer:"
find "$UPPER_DIR" -type f 2>/dev/null | sort
UPPER_COUNT=$(find "$UPPER_DIR" -type f 2>/dev/null | wc -l)
echo "   Total: $UPPER_COUNT files"

echo ""
echo "3. Files on mount point:"
find "$MOUNT_DIR" -type f 2>/dev/null | sort
MOUNT_COUNT=$(find "$MOUNT_DIR" -type f 2>/dev/null | wc -l)
echo "   Total: $MOUNT_COUNT files"

echo ""
echo "4. Checking for whiteout markers in upper:"
WHITEOUT_COUNT=$(find "$UPPER_DIR" -name ".wh.*" -type f 2>/dev/null | wc -l)
if [ $WHITEOUT_COUNT -gt 0 ]; then
    echo "   Found $WHITEOUT_COUNT whiteout markers:"
    find "$UPPER_DIR" -name ".wh.*" -type f 2>/dev/null | sort
else
    echo "   No whiteout markers"
fi

echo ""
echo "5. Layer statistics:"
echo "   Lower size: $(du -sh $LOWER_DIR 2>/dev/null | cut -f1)"
echo "   Upper size: $(du -sh $UPPER_DIR 2>/dev/null | cut -f1)"
echo "   Mount visible size: $(du -sh $MOUNT_DIR 2>/dev/null | cut -f1)"

echo ""
echo "6. Overlapping files (should be in both):"
for f in $(find "$LOWER_DIR" -type f 2>/dev/null); do
    rel_path=$(echo "$f" | sed "s|$LOWER_DIR||")
    if [ -f "$UPPER_DIR$rel_path" ]; then
        echo "   $rel_path (in both layers)"
    fi
done

echo ""
echo "7. Layer-specific files:"
echo "   Only in lower:"
for f in $(find "$LOWER_DIR" -type f 2>/dev/null); do
    rel_path=$(echo "$f" | sed "s|$LOWER_DIR||")
    if [ ! -f "$UPPER_DIR$rel_path" ]; then
        echo "   $rel_path"
    fi
done

echo ""
echo "   Only in upper:"
for f in $(find "$UPPER_DIR" -type f 2>/dev/null); do
    if [[ ! "$f" =~ \.wh\. ]]; then
        rel_path=$(echo "$f" | sed "s|$UPPER_DIR||")
        if [ ! -f "$LOWER_DIR$rel_path" ]; then
            echo "   $rel_path"
        fi
    fi
done

echo ""
echo "✓ Layer verification complete"
