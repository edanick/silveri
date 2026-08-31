# silveri/std

Standard-library source directory for the silveri interpreter project.

The manifest (`silveri.srp`) declares `sources: ["std", "src"]` so the
project qualifies for the compiler-project carve-out in the std-internal
win32 visibility rule (silverc-rs `src/main.rs`: a `.srp` manifest that
ships a `std` source directory keeps full win32 access across its
manifest sources). This lets interpreter internals (`builtins.sr`,
`cache.sr`, `resource.sr`, `exception_std.sr`, `project.sr`, `gc.sr`,
`mouse.sr`, `keyboard.sr`) import `win32.kernel32`, `win32.msvcrt`,
`win32.user32`, and `win32.ws2_32` directly.

Only `.sr` files under this directory are compiled; this README is a
placeholder and is never collected (see silverc-rs `src/project.rs`
`walk_dir`).
