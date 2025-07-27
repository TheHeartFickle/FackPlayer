import pydirectinput

# 鼠标部分
mouseClick = pydirectinput.click
mouseRightClick = pydirectinput.rightClick
mouseMoveTo = pydirectinput.moveTo
mouseMoveRel = pydirectinput.moveRel

mouseDown = pydirectinput.mouseDown
mouseUp = pydirectinput.mouseUp


# 键盘部分
import keyboard  # noqa: E402

wait = keyboard.wait
add_hotkey = keyboard.add_hotkey
remove_hotkey = keyboard.remove_hotkey

# ===================================

import pyautogui  # noqa: E402

keyboardPress = pyautogui.press
keyboardDown = pyautogui.keyDown
keyboardUp = pyautogui.keyUp

import time

playerWait = time.sleep
