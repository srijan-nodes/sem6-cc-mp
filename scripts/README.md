# Union FS Test Scripts

Bash scripts to test all unionfs operations. Each script is standalone and tests a specific functionality.

## Quick Start

### Run all tests automatically:
```bash
bash run_all_tests.sh
```

This will:
1. Setup test directories
2. Mount the filesystem
3. Run all tests
4. Unmount and cleanup
5. Display a summary report

## Individual Scripts

### Setup & Mount
- **`setup.sh`** - Create test directories and initial files in both layers
- **`mount.sh`** - Mount the union filesystem
- **`unmount.sh`** - Unmount the filesystem (optionally cleanup)

### Functional Tests
- **`test_read.sh`** - Read files from both layers
- **`test_cow.sh`** - Test Copy-on-Write (modifying lower layer files)
- **`test_create.sh`** - Create new files
- **`test_mkdir.sh`** - Create directories
- **`test_delete.sh`** - Delete files (creates whiteout markers)
- **`test_rmdir.sh`** - Delete directories
- **`test_truncate.sh`** - Truncate files
- **`test_utimens.sh`** - Update file timestamps
- **`test_large_file.sh`** - Test large file operations

### Verification
- **`verify_layers.sh`** - Verify layer separation and integrity

## Manual Testing Workflow

```bash
# 1. Setup
bash setup.sh

# 2. Mount
bash mount.sh

# 3. Run specific tests
bash test_read.sh
bash test_cow.sh
bash test_create.sh
# ... run other tests ...

# 4. Verify layers
bash verify_layers.sh

# 5. Unmount and cleanup
bash unmount.sh clean
```

## Script Output

Each script provides:
- ✓ for successful operations
- ✗ for failed operations
- Clear before/after state
- Layer separation verification
- File content verification

## Environment

- `BASE_DIR`: `/tmp/unionfs_test`
- `LOWER_DIR`: `/tmp/unionfs_test/lower` (read-only layer)
- `UPPER_DIR`: `/tmp/unionfs_test/upper` (writable layer)
- `MOUNT_DIR`: `/tmp/unionfs_test/mount` (unionfs mount point)

## Testing Matrix

| Operation | Test Script | Expected Behavior |
|-----------|-------------|-------------------|
| Read | test_read.sh | Files from both layers visible |
| CoW | test_cow.sh | Lower layer file copied to upper on write |
| Create | test_create.sh | New file only in upper layer |
| Mkdir | test_mkdir.sh | Directory created in upper layer |
| Delete | test_delete.sh | Whiteout marker created in upper |
| Rmdir | test_rmdir.sh | Whiteout marker for directory |
| Truncate | test_truncate.sh | File copied to upper before truncate |
| Utimens | test_utimens.sh | Timestamps updated in upper layer |
| Large File | test_large_file.sh | Large files handled correctly |
| Verify | verify_layers.sh | Layer separation maintained |

## Requirements

- FUSE library installed (`libfuse-dev`)
- unionfs binary compiled (`make`)
- Bash shell
- Unix utilities: `mount`, `fusermount`, `dd`, `touch`, `chmod`, `find`, `md5sum`

## Troubleshooting

### Filesystem already mounted
```bash
fusermount -u /tmp/unionfs_test/mount
```

### Permission denied
```bash
sudo bash script.sh
```

### Tests keep failing
```bash
# Clean state and start fresh
bash unmount.sh clean
bash run_all_tests.sh
```

## Notes

- All scripts check if the filesystem is mounted before proceeding
- Tests clean up after themselves (files created in tests)
- Whiteout markers are hidden-by-design but verified with `ls -la`
- Layer files are preserved between tests for verification
