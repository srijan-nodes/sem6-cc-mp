#!/bin/bash
# Run all tests in sequence

set -x

BASE_DIR="/tmp/unionfs_test"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔════════════════════════════════════════════════╗"
echo "║     Union FS - Complete Test Suite              ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
FAILED_TESTS=()
PASSED_TESTS=()
run_test() {
    local test_name=$1
    local script=$2
    echo -e "${YELLOW}Running:${NC} $test_name"

    if bash "$script" > /tmp/test_output.log 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}: $test_name"
        PASSED_TESTS+=("$test_name")
    else
        echo -e "${RED}✗ FAILED${NC}: $test_name"
        FAILED_TESTS+=("$test_name")
        echo "  Error details:"
        tail -5 /tmp/test_output.log | sed 's/^/    /'
    fi
    echo ""
}

# Setup
echo "Step 1: Setup"
if bash "$SCRIPTS_DIR/setup.sh" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Setup complete${NC}"
else
    echo -e "${RED}✗ Setup failed${NC}"
    exit 1
fi
echo ""

# Mount
echo "Step 2: Mount"
if bash "$SCRIPTS_DIR/mount.sh" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Mount successful${NC}"
else
    echo -e "${RED}✗ Mount failed${NC}"
    exit 1
fi
echo ""

# Run all tests
echo "Step 3: Running Tests"
echo "════════════════════════════════════════════════"
echo ""

run_test "Reading Files" "$SCRIPTS_DIR/test_read.sh"
run_test "Copy-on-Write" "$SCRIPTS_DIR/test_cow.sh"
run_test "File Creation" "$SCRIPTS_DIR/test_create.sh"
run_test "Directory Creation" "$SCRIPTS_DIR/test_mkdir.sh"
run_test "File Deletion" "$SCRIPTS_DIR/test_delete.sh"
run_test "Directory Deletion" "$SCRIPTS_DIR/test_rmdir.sh"
run_test "Truncate" "$SCRIPTS_DIR/test_truncate.sh"
run_test "Timestamps" "$SCRIPTS_DIR/test_utimens.sh"
run_test "Large Files" "$SCRIPTS_DIR/test_large_file.sh"
run_test "Layer Verification" "$SCRIPTS_DIR/verify_layers.sh"

# Summary
echo "════════════════════════════════════════════════"
echo ""
echo "Step 4: Cleanup"
if bash "$SCRIPTS_DIR/unmount.sh" clean > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Unmount and cleanup complete${NC}"
else
    echo -e "${RED}✗ Unmount failed${NC}"
fi

# Report
echo ""
echo "════════════════════════════════════════════════"
echo "Test Summary"
echo "════════════════════════════════════════════════"
echo -e "${GREEN}Passed: ${#PASSED_TESTS[@]}${NC}"
echo -e "${RED}Failed: ${#FAILED_TESTS[@]}${NC}"

if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
    echo ""
    echo "Failed tests:"
    for test in "${FAILED_TESTS[@]}"; do
        echo -e "${RED}  - $test${NC}"
    done
    exit 1
else
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
fi
