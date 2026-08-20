# computer-use plugin for Claude Code

Control the real Windows desktop through Claude Code with screenshots, mouse, keyboard, drag, scroll, and other computer-use primitives.

The plugin provides:

- a screenshot → vision → action loop
- MCP tools for `screenshot`, `cursor_position`, `mouse_move`, `click`, `mouse_down`, `mouse_up`, `drag`, `scroll`, `type_text`, `key_press`, and `wait`
- a reusable `SKILL.md` describing the operating loop and safety discipline
- a portable Windows launcher that does not require paths from the maintainer's machine

## Requirements

- Windows
- Python 3.10+
- a vision-capable tool/model for reading screenshots

Install Python dependencies in a dedicated environment:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The bundled MCP launcher resolves Python in this order:

1. `COMPUTER_USE_PYTHON` environment variable
2. `.venv\Scripts\python.exe` in the plugin root
3. `python.exe` on `PATH`
4. `py.exe -3`

If you already have a dedicated stable environment, keep using it without editing repository files:

```powershell
[Environment]::SetEnvironmentVariable(
  "COMPUTER_USE_PYTHON",
  "D:\\path\\to\\your\\venv\\Scripts\\python.exe",
  "User"
)
```

## Install as a Claude Code marketplace

Add this repository as a marketplace, then install the `computer-use` plugin from it using Claude Code's plugin manager. The repository includes both `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json`.

After installation, restart Claude Code so the MCP server is loaded.

## Safety model

This plugin controls the **real mouse and keyboard** of the current Windows session.

- Keep the intended target window in the foreground.
- `pyautogui.FAILSAFE` is enabled, so moving the mouse to a screen corner can abort automation.
- Re-screenshot after significant actions instead of blindly repeating clicks.
- Treat destructive or externally consequential actions such as deleting, paying, publishing, submitting, or sending as confirmation-gated operations.
- Store screenshots in an OS/user temporary directory or another path chosen by the caller; no maintainer-specific path is required.

## Development

Validate the repository locally:

```powershell
python -m compileall -q scripts
python -m pip install -r requirements.txt
```

GitHub Actions runs equivalent validation on Windows for pushes and pull requests.

## License

MIT — see [LICENSE](LICENSE).
