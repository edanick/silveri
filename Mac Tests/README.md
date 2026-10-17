# Mac Tests

Snapshot of the macOS workspace's test sources and fixtures. The repository's
original `tests/` directory is preserved unchanged. Generated executables,
build caches and test output files are not included in this snapshot.

Example from the repository root:

```sh
./executables/macos/silveri "Mac Tests/array_swap.sr"
```

All 12 top-level interpreter fixtures passed with output checks using the
Rust-built interpreter. Additional native checks had 12 passes, two excluded
Windows-target CLI cases, and one Linux-specific expectation that failed on
macOS. The spinner demo is not included in this checkout. Copied legacy Python
scripts may still refer to `tests/`, Windows paths or absent external demos;
they are retained as source fixtures, not macOS-compatible test runners.
