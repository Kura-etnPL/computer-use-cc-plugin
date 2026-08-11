---
name: computer-use
description: Control the real Windows desktop — move the mouse, click, drag, scroll, type, press keys, and take screenshots — in a screenshot-driven loop. Use when the user asks to operate a desktop app, click through a UI, fill a form, navigate a non-browser program, take a screenshot, or "use the computer / control the screen / click that button / type into that app". Requires the gemini-vision MCP to read screenshots (Claude has no native vision).
tools: Bash, mcp__gemini-vision__analyze_image
---

# Computer Use (desktop automation)

Drive the real Windows desktop through a **screenshot → vision → action** loop, mirroring Cursor's Computer Use. All actions go through the bundled pyautogui engine at `scripts/computer_use.py`, run by the dedicated venv Python.

## 0. Always use the venv interpreter

```bash
PY=E:/CSoftware/computer-use-venv/Scripts/python.exe
SC=~/.claude/skills/computer-use/scripts/computer_use.py
```

Replace `~` with the real path (`C:/Users/Eternal/.claude/skills/computer-use/scripts/computer_use.py`). Use `$PY "$SC" ...` for every call.

## 1. The loop

1. **Screenshot** the current screen:
   ```bash
   mkdir -p E:/Eternal/Auto_Empire/temp/computer_use
   $PY "$SC" screenshot E:/Eternal/Auto_Empire/temp/computer_use/screen.png
   ```
2. **Read** it with gemini-vision (Claude cannot see images natively):
   `mcp__gemini-vision__analyze_image` on that path. Ask for the layout, the UI elements you need, and their **pixel coordinates**.
3. **Decide** the next action and run it (action table below). One action per step, verify assumptions rather than guessing.
4. **Re-screenshot + re-analyze** whenever the result is uncertain or after a significant step, then continue.
5. Stop when the task is done, or when you cannot make progress — report where you are instead of flailing.

## 2. Action primitives

All coordinates are screen pixels; `(0,0)` is the top-left corner. `(x,y)` from gemini-vision are image pixels = screen pixels at 100% scale.

| Action | Command |
|--------|---------|
| Screenshot | `$PY "$SC" screenshot <out.png>` |
| Cursor position | `$PY "$SC" position` → prints `x,y` |
| Move mouse | `$PY "$SC" mouse_move <x> <y>` |
| Click | `$PY "$SC" click <x> <y> [--button left\|right\|middle] [--count 1\|2]` |
| Mouse down | `$PY "$SC" mouse_down --button <btn>` |
| Mouse up | `$PY "$SC" mouse_up --button <btn>` |
| Drag | `$PY "$SC" drag <x1> <y1> <x2> <y2> [--duration 0.5]` |
| Scroll | `$PY "$SC" scroll <clicks> [--x <x> --y <y>]` (positive = up) |
| Type text | `$PY "$SC" type "<text>"` (Chinese auto-pastes via clipboard) |
| Press key / hotkey | `$PY "$SC" key <key...>` (e.g. `key enter`, `key ctrl l`, `key ctrl c`) |
| Wait | `$PY "$SC" wait <ms>` |

`key` accepts one key or a combo: `key ctrl l` → Ctrl+L; `key enter`, `key tab`, `key escape`, `key ctrl v`, `key ctrl a` are common.

## 3. Safety & discipline

- **Foreground window**: the target app must be visible and in front — you are moving the user's real mouse. Before acting, confirm the active window matches the target (screenshot first).
- **Failsafe**: pyautogui has a fail-safe — moving the mouse hard to a screen corner aborts, in case the user needs to stop you.
- **Screenshots** go to `E:/Eternal/Auto_Empire/temp/computer_use/` (never C:).
- **Irreversible actions** (deleting, submitting, paying, publishing, sending) — **ask the user first**, then verify the screen shows the exact target before clicking.
- **One hypothesis at a time**: make one change, re-screenshot, confirm. If an action didn't take effect, re-check coordinates rather than clicking repeatedly.
- **Chinese text** goes through the clipboard (Ctrl+V) — do not type CJK as raw keys.
