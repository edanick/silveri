# silveri/std

Standard-library source directory for the silveri interpreter project.

The manifest (`silveri.srp`) declares `sources: ["std", "src"]` so the
project qualifies for the compiler-project carve-out in the std-internal
win32 visibility rule (silverc-rs `src/main.rs`: a `.srp` manifest that
ships a `std` source directory keeps full win32 access across its
manifest sources).

After the UNIFIED_CORE_LIBRARY phase-3 rewires (v2 canonical fold), the
interpreter ships no `_win` backend files at all: `builtins_win.sr`,
`cache_win.sr`, and `resource_win.sr` were folded into their owner modules
(`builtins.sr`, `cache.sr`, `resource.sr`) and deleted, so every raw kernel32/
msvcrt call now lives inline inside an `#on WINDOWS ... #off` region of the
owning function (file-top plain grant for the win32 imports), per
UNIFIED_CORE_LIBRARY.md §4 rule 6. `gc.sr` keeps its runtime-internal
memory backend as-is. The remaining sources (`exception_std.sr`,
`project.sr`, and the rest of `src/`) are win32-free: they route through
the unified std (`fs.getenv`, `file.*`, `folder.*`). The old
`mouse.sr`/`keyboard.sr` mirror files were dead code (never compiled,
never dispatched, as the interpreter implements `mouse`/`keyboard` natively
via the `mouse_module`/`keyboard_module` builtin dispatch) and were
removed.

Only `.sr` files under this directory are compiled; this README is a
placeholder and is never collected (see silverc-rs `src/project.rs`
`walk_dir`).
