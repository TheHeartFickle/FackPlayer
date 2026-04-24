import logging
import time
from typing import Optional

import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

logger = logging.getLogger(__name__)


class ScreenCapture:
    def __init__(self) -> None:
        self.hwnd = win32gui.GetDesktopWindow()
        self.lastTimeStamp: float = -1.0
        self.lastImage: Optional[np.ndarray] = None
        self.interval: Optional[float] = None
        self.refresh()

    def cool_down(self, interval: float) -> "ScreenCapture":
        """
        设置截图间隔（秒）

        :param interval: 间隔时间（秒）
        """
        self.interval = interval
        return self

    def refresh(self) -> None:
        """
        初始化资源，可重复调用以应对分辨率变化
        """
        self.width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # 清理旧资源
        self.release()

        # 创建新资源
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.width, self.height)

    def get(self) -> np.ndarray:
        if (self.interval is not None) and (
            time.time() - self.lastTimeStamp < self.interval
        ):
            return self.lastImage
        # 检查分辨率变化
        current_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        current_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        if current_width != self.width or current_height != self.height:
            self.refresh()

        # 执行截图
        self.saveDC.SelectObject(self.saveBitMap)
        self.saveDC.BitBlt(
            (0, 0), (self.width, self.height), self.mfcDC, (0, 0), win32con.SRCCOPY
        )

        # 获取位图数据（True = 自底向上位图顺序）
        bmp_info = self.saveBitMap.GetInfo()
        bmp_str = self.saveBitMap.GetBitmapBits(True)

        # 转换为numpy数组
        img = np.frombuffer(bmp_str, dtype=np.uint8)
        img = img.reshape((bmp_info["bmHeight"], bmp_info["bmWidth"], 4))

        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 缓存图片
        self.lastTimeStamp = time.time()
        self.lastImage = img
        return img

    def release(self) -> None:
        """显式释放资源"""
        if hasattr(self, "saveBitMap") and self.saveBitMap:
            try:
                win32gui.DeleteObject(self.saveBitMap.GetHandle())
            except Exception:
                logger.exception("Failed to delete saveBitMap")
            self.saveBitMap = None

        if hasattr(self, "saveDC") and self.saveDC:
            try:
                self.saveDC.DeleteDC()
            except Exception:
                logger.exception("Failed to delete saveDC")
            self.saveDC = None

        if hasattr(self, "mfcDC") and self.mfcDC:
            try:
                self.mfcDC.DeleteDC()
            except Exception:
                logger.exception("Failed to delete mfcDC")
            self.mfcDC = None

        if hasattr(self, "hwndDC") and self.hwndDC:
            try:
                win32gui.ReleaseDC(self.hwnd, self.hwndDC)
            except Exception:
                logger.exception("Failed to release hwndDC")
            self.hwndDC = None

    def __enter__(self) -> "ScreenCapture":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


# 使用示例
if __name__ == "__main__":
    # 创建捕获器（一次性初始化所有资源）
    capture = ScreenCapture()

    # 多次调用capture方法，重用缓存的对象
    img1 = capture.get()
    print(f"截图1尺寸: {img1.shape}")

    img2 = capture.get()
    print(f"截图2尺寸: {img2.shape}")

    # 销毁对象时自动清理资源
    del capture
