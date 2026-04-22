// Author: Suhani Singh
// Description: Initializes FUSE filesystem and maps operations
#include "state.h"
#include "path.h"
#include "cow.h"
#include "whiteout.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <sys/stat.h>

static struct fuse_operations ops;

static void init_fuse_ops() {
    memset(&ops, 0, sizeof(ops));
    ops.getattr  = fs_getattr;
    ops.mkdir    = fs_mkdir;
    ops.unlink   = fs_unlink;
    ops.rmdir    = fs_rmdir;
    ops.truncate = fs_truncate;
    ops.open     = fs_open;
    ops.read     = fs_read;
    ops.write    = fs_write;
    ops.release  = fs_release;
    ops.readdir  = fs_readdir;
    ops.create   = fs_create;
    ops.utimens  = fs_utimens;
    ops.chmod    = fs_chmod;
}

static void usage(const char* prog) {
    fprintf(stderr, "Usage: %s <lowerdir> <upperdir> <mountpoint> [FUSE options]\n", prog);
}
// Validate command line arguments
int main(int argc, char* argv[]) {
    if (argc < 4) {
        usage(argv[0]);
        return 1;
    }

    init_fuse_ops();

    State* state = new State();
    state->lower_dir = argv[1];
    state->upper_dir = argv[2];

    // Validate that both directories exist.
    struct stat st;
    for (const auto& dir : {state->lower_dir, state->upper_dir}) {
        if (stat(dir.c_str(), &st) == -1 || !S_ISDIR(st.st_mode)) {
            fprintf(stderr, "Error: '%s' is not a valid directory\n", dir.c_str());
            delete state;
            return 1;
        }
    }

    // Build FUSE argv: strip lowerdir and upperdir, keep mountpoint + any FUSE flags.
    int fuse_argc = argc - 2;
    char** fuse_argv = new char*[fuse_argc];
    fuse_argv[0] = argv[0];
    for (int i = 1; i < fuse_argc; i++)
        fuse_argv[i] = argv[i + 2];

    int ret = fuse_main(fuse_argc, fuse_argv, &ops, state);
    delete[] fuse_argv;
    delete state;
    return ret;
}
