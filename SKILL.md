---
name: computer-use
description: Control the real Windows desktop — move the mouse, click, drag, scroll, type, press keys, and take screenshots — in a screenshot-driven loop. Use when the user asks to operate a desktop app, click through a UI, fill a form, navigate a non-browser program, take a screenshot, or use/control the computer. Requires a vision-capable tool/model to interpret screenshots.
tools: Bash, mcp__gemini-vision__analyze_image
---

# Computer Use (desktop automation)

Drive the real Windows desktop through a **screenshot → vision → action → verify** loop.

The plugin exposes its actions through the bundled `computer-use` MCP server. Prefer those MCP tools directly. Use the CLI in `scripts/computer_use.py` only for diagnostics or when explicitly operating outside the MCP host.

## 1. Core loop

1. Capture the current screen with the `screenshot` MCP tool. Save it to an OS/user temporary directory or another caller-selected path.
2. Inspect the screenshot with the available vision tool/model and identify the exact target and pixel coordinates.
3. Perform one deliberate action.
4. Re-screenshot after a significant state change or whenever the result is uncertain.
5. Continue until the requested task is complete. If progress is blocked, report the exact blocker instead of repeatedly clicking.

## 2. Action primitives

The MCP server exposes:

- `screenshot(out_path)`
- `cursor_position()`
- `mouse_move(x, y)`
- `click(x, y, button="left", count=1)`
- `mouse_down(button="left")`
- `mouse_up(button="left")`
- `drag(x1, y1, x2, y2, duration=0.5)`
- `scroll(clicks, x=None, y=None)`
- `type_text(text)`
- `key_press(keys)`
- `wait(ms)`

Coordinates use screen pixels with `(0,0)` at the top-left.

## 3. Safety and reliability discipline

- Confirm the intended target window is visible and in the foreground before acting.
- `pyautogui.FAILSAFE` is enabled. The user can move the mouse to a screen corner to abort automation.
- Make one state-changing action at a time when the outcome is uncertain, then verify with a fresh screenshot.
- Never compensate for uncertain coordinates by rapid repeated clicking.
- For destructive or externally consequential actions — deleting, submitting, paying, publishing, sending, purchasing, changing permissions, or equivalent — obtain explicit user confirmation immediately before the action and verify the visible target.
- CJK and other non-ASCII text is pasted through the clipboard for reliability.
- Do not assume a maintainer-specific drive, username, venv, or screenshot directory.

## 4. Python resolution

The MCP launcher resolves Python in this order:

1. `COMPUTER_USE_PYTHON`
2. plugin-local `.venv\\Scripts\\python.exe`
3. `python.exe` on `PATH`
4. `py.exe -3`

This preserves stable dedicated environments while keeping the repository portable.

## 5. Diagnostic CLI

When MCP startup itself is being debugged, invoke the script with a known interpreter:

```powershell
$env:COMPUTER_USE_PYTHON = "D:\\path\\to\\venv\\Scripts\\python.exe"
& $env:COMPUTER_USE_PYTHON .\scripts\computer_use.py position
```

Do not hard-code personal machine paths into committed files.
