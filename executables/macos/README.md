# macOS executable

`silveri` is the x86_64 macOS interpreter built directly by the Rust compiler.
Apple silicon requires Rosetta 2. From the repository root:

```sh
./executables/macos/silveri --version
./executables/macos/silveri "Mac Tests/array_swap.sr"
```

All 12 main interpreter fixtures passed, including output checks. See
[`Mac Tests`](../../Mac%20Tests/) for fixtures and additional platform-specific
test limitations. This executable is not notarized.
