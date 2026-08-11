#!/usr/bin/env python
"""computer_use.py — pyautogui-based desktop automation engine for Claude Code.

Implements the action primitives of Cursor's `computer_use_tool_pb` (mouse_move,
click, mouse_down/up, drag, scroll, type, key, wait, screenshot, position) so
Claude Code can drive the real Windows desktop in a screenshot -> vision ->
action loop.

Usage (always via the dedicated venv python):
    E:\\CSoftware\\computer-use-venv\\Scripts\\python.exe computer_use.py <action> [args...]

Exit code 0 on success, 1 on error (message printed to stderr).
Coordinates are in screen pixels; (0,0) is the top-left corner.
"""

import argparse
import sys
import time

import pyautogui

# Fail-fast rather than fling the mouse around when a coordinate is out of range.
pyautogui.FAILSAFE = True

# A short pause between synthetic events so the OS/target app keeps up.
pyautogui.PAUSE = 0.05


def err(msg: str) -> int:
    print(f"[computer_use] error: {msg}", file=sys.stderr)
    return 1


def screenshot(path: str) -> int:
    img = pyautogui.screenshot()
    img.save(path)
    print(f"saved screenshot ({img.width}x{img.height}) -> {path}")
    return 0


def position() -> int:
    x, y = pyautogui.position()
    print(f"{x},{y}")
    return 0


def mouse_move(x: int, y: int, duration: float = 0.15) -> int:
    pyautogui.moveTo(x, y, duration=duration)
    return 0


def parse_button(button: str):
    mapping = {"left": "left", "right": "right", "middle": "middle"}
    if button not in mapping:
        raise ValueError(f"unknown button '{button}' (expected left|right|middle)")
    return mapping[button]


def click(x: int, y: int, button: str = "left", count: int = 1, duration: float = 0.1) -> int:
    btn = parse_button(button)
    pyautogui.click(x=x, y=y, button=btn, clicks=count, interval=0.05, duration=duration)
    return 0


def mouse_down(button: str = "left") -> int:
    pyautogui.mouseDown(button=parse_button(button))
    return 0


def mouse_up(button: str = "left") -> int:
    pyautogui.mouseUp(button=parse_button(button))
    return 0


def drag(x1: int, y1: int, x2: int, y2: int, duration: float = 0.5) -> int:
    pyautogui.moveTo(x1, y1, duration=duration / 2)
    pyautogui.dragTo(x2, y2, duration=duration / 2, button="left")
    return 0


def scroll(clicks: int, x: int | None = None, y: int | None = None) -> int:
    if x is not None and y is not None:
        pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.scroll(clicks)
    return 0


def type_text(text: str) -> int:
    """Type text. ASCII goes through pyautogui keystrokes; anything non-ASCII
    (e.g. Chinese) is pasted via the clipboard to avoid encoding issues."""
    try:
        text.encode("ascii")
        pyautogui.write(text, interval=0.01)
        return 0
    except UnicodeEncodeError:
        # Non-ASCII: copy to clipboard and paste (Ctrl+V) — robust for CJK.
        pyautogui.hotkey("ctrl", "c")  # no-op safety; cleared below anyway
        import pyperclip  # pyautogui bundles pyperclip

        pyperclip.copy(text)
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "v")
        return 0


def key(keys) -> int:
    """Press one key or a hotkey combo. Each CLI arg is a key; combined args
    become a chord (e.g. `key ctrl l` -> Ctrl+L)."""
    keys = [k.lower() for k in keys]
    if len(keys) == 1:
        pyautogui.press(keys[0])
    else:
        pyautogui.hotkey(*keys)
    return 0


def wait(ms: int) -> int:
    time.sleep(ms / 1000.0)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="computer_use.py", description="pyautogui desktop automation")
    sub = p.add_subparsers(dest="action", required=True)

    sub.add_parser("screenshot").add_argument("out_path", help="output PNG path")
    sub.add_parser("position")

    m = sub.add_parser("mouse_move")
    m.add_argument("x", type=int)
    m.add_argument("y", type=int)

    c = sub.add_parser("click")
    c.add_argument("x", type=int)
    c.add_argument("y", type=int)
    c.add_argument("--button", default="left", choices=["left", "right", "middle"])
    c.add_argument("--count", type=int, default=1)

    d = sub.add_parser("mouse_down")
    d.add_argument("--button", default="left", choices=["left", "right", "middle"])
    u = sub.add_parser("mouse_up")
    u.add_argument("--button", default="left", choices=["left", "right", "middle"])

    g = sub.add_parser("drag")
    g.add_argument("x1", type=int)
    g.add_argument("y1", type=int)
    g.add_argument("x2", type=int)
    g.add_argument("y2", type=int)
    g.add_argument("--duration", type=float, default=0.5)

    s = sub.add_parser("scroll")
    s.add_argument("clicks", type=int)
    s.add_argument("--x", type=int, default=None)
    s.add_argument("--y", type=int, default=None)

    t = sub.add_parser("type")
    t.add_argument("text")

    k = sub.add_parser("key")
    k.add_argument("keys", nargs="+")

    w = sub.add_parser("wait")
    w.add_argument("ms", type=int)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.action == "screenshot":
            return screenshot(args.out_path)
        if args.action == "position":
            return position()
        if args.action == "mouse_move":
            return mouse_move(args.x, args.y)
        if args.action == "click":
            return click(args.x, args.y, args.button, args.count)
        if args.action == "mouse_down":
            return mouse_down(args.button)
        if args.action == "mouse_up":
            return mouse_up(args.button)
        if args.action == "drag":
            return drag(args.x1, args.y1, args.x2, args.y2, args.duration)
        if args.action == "scroll":
            return scroll(args.clicks, args.x, args.y)
        if args.action == "type":
            return type_text(args.text)
        if args.action == "key":
            return key(args.keys)
        if args.action == "wait":
            return wait(args.ms)
    except KeyboardInterrupt:
        return err("interrupted")
    except Exception as e:  # noqa: BLE001 — surface any pyautogui/system error clearly
        return err(f"{type(e).__name__}: {e}")
    return err(f"unknown action '{args.action}'")


if __name__ == "__main__":
    sys.exit(main())
