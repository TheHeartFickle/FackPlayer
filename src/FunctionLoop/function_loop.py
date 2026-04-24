import logging
import multiprocessing
import time
import keyboard

logger = logging.getLogger(__name__)


def _command_worker(command_queue, stop_flag, pause_flag, function_name):
    """命令处理进程：阻塞监听队列命令，控制暂停状态"""
    while not stop_flag.is_set():
        try:
            cmd = command_queue.get(timeout=0.2)
            if cmd == "start":
                pause_flag.clear()
                logger.info("[%s] started/resumed", function_name)
            elif cmd == "pause":
                pause_flag.set()
                logger.info("[%s] paused", function_name)
        except Exception:
            continue


def _function_worker(stop_flag, pause_flag, function, function_name, max_retries=5):
    """函数执行进程：循环执行目标函数，支持暂停和异常上限"""
    retry_count = 0
    while not stop_flag.is_set():
        if pause_flag.is_set():
            time.sleep(0.2)
            continue
        try:
            function()
            retry_count = 0  # 成功后重置计数
        except Exception as e:
            retry_count += 1
            logger.error("Error in %s (retry %d/%d): %s",
                         function_name, retry_count, max_retries, e)
            if retry_count >= max_retries:
                logger.critical(
                    "%s 连续失败 %d 次，停止执行", function_name, max_retries
                )
                break


class LoopFunction:
    def __init__(self):
        self._command_queue = multiprocessing.Queue()
        self._stop_flag = multiprocessing.Event()
        self._pause_flag = multiprocessing.Event()
        self._pause_flag.set()  # 初始设为暂停状态
        self._function = None
        self._function_name = ""
        self._process = None          # 函数执行进程
        self._command_process = None  # 命令处理进程
        self._hotkey_removers = []    # 热键注销回调列表

    def start_key(self, key):
        remover = keyboard.add_hotkey(key, lambda: self._command_queue.put("start"))
        self._hotkey_removers.append(remover)
        return self

    def pause_key(self, key):
        remover = keyboard.add_hotkey(key, self.pause)
        self._hotkey_removers.append(remover)
        return self

    def loop_function(self, func):
        self._function = func
        self._function_name = func.__name__
        return self

    def build(self, max_retries: int = 5):
        if self._function is None:
            raise ValueError("loop_function must be set before calling build()")

        self._stop_flag.clear()

        # 命令处理进程
        self._command_process = multiprocessing.Process(
            target=_command_worker,
            args=(self._command_queue, self._stop_flag, self._pause_flag, self._function_name),
            daemon=True,
        )
        self._command_process.start()

        # 函数执行进程
        self._process = multiprocessing.Process(
            target=_function_worker,
            args=(self._stop_flag, self._pause_flag, self._function, self._function_name),
            kwargs={"max_retries": max_retries},
            daemon=True,
        )
        self._process.start()

        print(f"{self._function_name} worker built and started")
        return self

    def start(self):
        self._command_queue.put("start")

    def pause(self):
        self._command_queue.put("pause")

    def stop(self):
        """请求停止，等待进程退出（超时后强制终止）"""
        self._stop_flag.set()
        self._join_processes()

    def release(self):
        """释放所有资源：终止进程 + 注销热键"""
        self.stop()
        self._release_hotkeys()

    # ── 内部辅助 ──────────────────────────────────

    def _join_processes(self, timeout=2):
        processes = [p for p in (self._command_process, self._process) if p is not None]
        if not processes:
            return

        # 先等待优雅退出
        for p in processes:
            if p.is_alive():
                p.join(timeout=timeout)

        # 强制终止仍未退出的进程
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=1)

    def _release_hotkeys(self):
        for remover in self._hotkey_removers:
            try:
                remover()
            except Exception:
                logger.exception("Failed to remove hotkey")
        self._hotkey_removers.clear()
