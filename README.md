# Silver Interpreter

Run Silver ideas immediately, with no compilation wait.

`silveri` executes Silver source files directly, making it easy to explore the
language, test an idea, run a script, and see the result without first creating
a native executable.

## Credits

- **Author:** Edan M.
- **Version:** 0.7.7.1
- **Copyright:** © 2025 Edan M.

## Quick start

### Put `silveri` on your `PATH`

#### Windows

Pick either a global binaries directory or a per-user one under AppData.

Option 1 - global `C:\bin` (needs admin to create):

```powershell
mkdir C:\bin
setx PATH "$env:PATH;C:\bin"
```

Download or copy `silveri.exe` into `C:\bin`.

Option 2 - per-user `%appdata%\silver\bin` (no admin needed):

```powershell
mkdir "$env:APPDATA\silver\bin"
setx PATH "$env:PATH;$env:APPDATA\silver\bin"
```

Download or copy `silveri.exe` into `%appdata%\silver\bin`.

Reopen the terminal afterwards, then verify with `silveri --version`.

#### Linux and macOS

Both use the same location, `~/.local/bin`:

```bash
test -d ~/.local/bin || mkdir -p ~/.local/bin
```

Copy it from your Downloads folder:

```bash
cp ~/Downloads/silveri ~/.local/bin/silveri
chmod +x ~/.local/bin/silveri
```

Or download it straight there with curl:

```bash
curl -L -o ~/.local/bin/silveri <download-url>
chmod +x ~/.local/bin/silveri
```

Make sure `~/.local/bin` is on your `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add that line to `~/.bashrc` (Linux) or `~/.zshrc` (macOS, the default
shell) so it persists. Most Linux distributions pick up `~/.local/bin`
automatically once it exists (re-login to apply); macOS always needs the
export line above, then `source ~/.zshrc`.

Verify with `silveri --version`.

### Run a Silver program

Place `silveri` on your `PATH`, then run any Silver source file:

```bash
silveri path/to/program.sr
```

Silver files use the `.sr` extension:

```silver
void main() {
    string message = "Hello from Silver";
    printline(message);
}
```

Save the example as `hello.sr` and execute it immediately:

```bash
silveri hello.sr
```

## Command-line usage

```text
Usage: silveri [options] <filename>

Options:
  -i <file>      Input Silver source file
  -o <file>      Output file (ignored in interpreter)
  --help, -h     Show help information
  --version      Show version information
```

Examples:

```bash
# Execute a Silver script directly
silveri script.sr

# Provide the input file explicitly
silveri -i script.sr

# Inspect the available commands
silveri --help

# Show interpreter and language versions
silveri --version
```

The `-o` option is accepted for command compatibility but is ignored because
`silveri` executes source directly instead of producing a compiled output file.

## Why use silveri?

- Execute Silver code immediately
- Experiment without a compilation step
- Iterate quickly while learning the language
- Run scripts and small command-line tools directly
- Explore language features through short source files
- Use the same `.sr` source files with the Silver toolchain

## A small example

```silver
class Greeter {
    public prop string name;

    construct (string name) {
        this.name = name;
    }

    public string greet() {
        return $"Hello, {this.name}!";
    }
}

void main() {
    Greeter greeter = new Greeter("Silver");
    printline(greeter.greet());
}
```

Run it directly:

```bash
silveri greeter.sr
```

## Project layout

| Path | Purpose |
| --- | --- |
| `src/` | Interpreter source modules |
| `silveri.srp` | Silver interpreter project manifest |
| `silveri.exe` | Interpreter executable on Windows |

## License

Edan M. © 2025 All Rights Reserved Proprietary
