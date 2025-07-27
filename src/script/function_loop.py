from threading import Thread, Event
from keyboard import add_hotkey
import time


class LoopFunction(object):
    def __init__(self, _key_start, _key_pause, _loop_function):
        self.start_key = _key_start
        self.pause_key = _key_pause
        self.loop_function = _loop_function

        self.event = Event()
        self.thread = Thread(target=self.loop, args=(self.loop_function, self.event))
        add_hotkey(_key_start, self.start)
        add_hotkey(_key_pause, self.pause)

    def loop(self, loop_func, event):
        func = loop_func
        func_name = loop_func.__name__
        while 1:
            if event.is_set():
                func()
                print(f"{func_name} run {time.time()}")
        print(f"{func_name} is exit {time.time()}")

    def start(self):
        print("thread start")
        if not self.thread.is_alive():
            self.thread.start()
        self.event.set()

    def pause(self):
        print("thread pause")
        self.event.clear()
