# silveri/std

Standard-library source directory for the silveri interpreter project.

The manifest (`silveri.srp`) declares `sources: ["std", "src"]` so the
project qualifies for the compiler-project carve-out in the std-internal
win32 visibility rule (silverc-rs `src/main.rs`: a `.srp` manifest that
ships a `std` source directory keeps full win32 access across its
manifest sources).

After the UNIFIED_CORE_LIBRARY phase-3 rewires, win32 imports in the
interpreter's own sources exist ONLY in the internal Windows backends
(`builtins_win.sr`, `cache_win.sr`, `resource_win.sr`) and in `gc.sr`
(runtime-internal memory backend, kept as-is). `builtins.sr`,
`cache.sr`, `resource.sr`, `exception_std.sr`, and `project.sr` are
win32-free: they route through the unified std (`fs.getenv`, `file.*`,
`folder.*`) or the internal backends. The old `mouse.sr`/`keyboard.sr`
mirror files were dead code (never compiled, never dispatched — the
interpreter implements `mouse`/`keyboard` natively via the
`mouse_module`/`keyboard_module` builtin dispatch) and were removed.

Only `.sr` files under this directory are compiled; this README is a
placeholder and is never collected (see silverc-rs `src/project.rs`
`walk_dir`).
