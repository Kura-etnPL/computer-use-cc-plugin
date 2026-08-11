# computer-use plugin for Claude Code

Control the real Windows desktop through Claude Code — screenshots, mouse, keyboard, drag, scroll, and more.

This plugin rebuilds the same idea as Cursor's Computer Use for Claude Code:

- **Screenshot → vision → action loop**: capture the screen, read it with a vision model (`gemini-vision` MCP), then issue mouse/keyboard actions.
- **Action primitives**: `screenshot`, `cursor_position`, `mouse_move`, `click`, `mouse_down`, `mouse_up`, `drag`, `scroll`, `type_text`, `key_press`, `wait`.
- **MCP server included**: all actions are exposed as MCP tools so they appear in Claude Code's tool list.
- **Skill included**: natural-language trigger for the screenshot-driven loop.

## Requirements

- Windows (uses `pyautogui` for desktop automation)
- A dedicated Python venv at `E:\CSoftware\computer-use-venv` with `pyautogui` and `fastmcp` installed.
- `gemini-vision` MCP server for reading screenshots (Claude Code has no native vision).

## Install

```bash
claude plugin install computer-use@<marketplace>
```

After installing, restart Claude Code. The MCP server starts automatically and the tools appear in the tool list.

## Safety notes

- This controls your **real mouse and keyboard**. The target window must be in the foreground.
- Screenshots are written to `E:\Eternal\Auto_Empire\temp\computer_use\`.
- CJK text is pasted via the clipboard (`Ctrl+V`) to avoid encoding issues.
- `Win` key combinations (e.g. `Win+R`) are unreliable through `pyautogui` in this setup; launch applications via shell or other means.

## License

MIT
