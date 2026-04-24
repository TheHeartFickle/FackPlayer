import ctypes
import sys
from os import system


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if __name__ == "__main__":
    if is_admin():
        # 将要运行的代码加到这里
        system(f"{sys.executable} ./src/main.py")
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1
            )
