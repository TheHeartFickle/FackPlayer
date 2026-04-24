import logging
import time

import keyboard
from Executor import keyboard_down, keyboard_up, player_wait
from FunctionLoop import LoopFunction
from Observer import ImgDisplay, ScreenCapture
from PatternMatcher import PatternMatcher

DEBUG = 0


def test_fun():
    print("test")
    time.sleep(1)


def single_e():
    keyboard_down("e")
    player_wait(0.35)
    keyboard_up("e")
    player_wait(0.16)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if DEBUG:
        screen = ScreenCapture().cool_down(0.5)
        pm = PatternMatcher().set_vision_observer(screen.get)
        # dis = ImgDisplay().zoom(0.7)
        # dis.Show(screen.get())
    else:
        print("start")
        loop = (
            LoopFunction().start_key("g").pause_key("v").loop_function(single_e).build()
        )
        # loop.start()
        # time.sleep(5)
        # loop.pause()
        print("按 p 键退出...")
        keyboard.wait("p")
        loop.release()
        print("程序已退出")
