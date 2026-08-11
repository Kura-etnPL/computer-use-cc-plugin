#!/usr/bin/env python
"""computer_use MCP server — exposes the desktop automation actions as MCP tools.

Serves the same action primitives as scripts/computer_use.py (mouse, keyboard,
screenshot) as standard MCP tools so they appear in Claude Code's tool list.
Reuses computer_use.py as the single source of truth.

Run as a stdio MCP server via the plugin's .mcp.json:
    E:\\CSoftware\\computer-use-venv\\Scripts\\python.exe scripts/mcp_server.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP  # noqa: E402

import computer_use as cu  # noqa: E402

mcp = FastMCP("computer-use")


def _run(fn, *args, **kwargs) -> str:
    """Call a computer_use action, capture its stdout, return a result string."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = fn(*args, **kwargs)
        detail = buf.getvalue().strip()
        return f"ok ({detail})" if rc == 0 else f"error(rc={rc}): {detail}"
    except Exception as e:  # noqa: BLE001 — surface any pyautogui/system error
        return f"error: {type(e).__name__}: {e}"


@mcp.tool()
def screenshot(out_path: str) -> str:
    """Capture the full screen to a PNG file at out_path. Use the result for the vision loop."""
    return _run(cu.screenshot, out_path)


@mcp.tool()
def cursor_position() -> str:
    """Return the current mouse cursor position as 'x,y' (top-left origin)."""
    return _run(cu.position)


@mcp.tool()
def mouse_move(x: int, y: int) -> str:
    """Move the mouse to screen pixel (x, y)."""
    return _run(cu.mouse_move, x, y)


@mcp.tool()
def click(x: int, y: int, button: str = "left", count: int = 1) -> str:
    """Click at screen pixel (x, y). button: left|right|middle. count: 1 (single) or 2 (double)."""
    return _run(cu.click, x, y, button, count)


@mcp.tool()
def mouse_down(button: str = "left") -> str:
    """Press and hold a mouse button (left|right|middle) at the current position."""
    return _run(cu.mouse_down, button)


@mcp.tool()
def mouse_up(button: str = "left") -> str:
    """Release a previously held mouse button (left|right|middle)."""
    return _run(cu.mouse_up, button)


@mcp.tool()
def drag(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5) -> str:
    """Drag with the left button from (x1,y1) to (x2,y2) over `duration` seconds."""
    return _run(cu.drag, x1, y1, x2, y2, duration)


@mcp.tool()
def scroll(clicks: int, x: int | None = None, y: int | None = None) -> str:
    """Scroll `clicks` notches (positive = up) at (x,y) or the current cursor."""
    return _run(cu.scroll, clicks, x, y)


@mcp.tool()
def type_text(text: str) -> str:
    """Type `text` into the focused field. ASCII goes via keystrokes; CJK via clipboard paste."""
    return _run(cu.type_text, text)


@mcp.tool()
def key_press(keys: list[str]) -> str:
    """Press key(s). One key (e.g. ['enter']) or a combo (e.g. ['ctrl','l'] = Ctrl+L)."""
    return _run(cu.key, keys)


@mcp.tool()
def wait(ms: int) -> str:
    """Wait `ms` milliseconds before the next action."""
    return _run(cu.wait, ms)


if __name__ == "__main__":
    mcp.run()
