"""执行器模块：键盘/鼠标输入模拟与热键管理"""

from time import sleep as player_wait  # 延时（秒）

import keyboard
from keyboard import add_hotkey, remove_hotkey, wait
from pydirectinput import (
    click as mouse_click,
    keyDown as keyboard_down,
    keyUp as keyboard_up,
    mouseDown as mouse_down,
    mouseUp as mouse_up,
    moveRel as mouse_move_rel,
    moveTo as mouse_move_to,
    press as keyboard_press,
    rightClick as mouse_right_click,
)

__all__ = [
    "add_hotkey",
    "keyboard_down",
    "keyboard_press",
    "keyboard_up",
    "mouse_click",
    "mouse_down",
    "mouse_move_rel",
    "mouse_move_to",
    "mouse_right_click",
    "mouse_up",
    "player_wait",
    "remove_hotkey",
    "wait",
]
