import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import cv2


def capture_screen_to_cv():
    # 获取桌面窗口句柄
    hwnd = win32gui.GetDesktopWindow()

    # 获取屏幕尺寸
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # 创建设备上下文
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    try:
        # 将位图选入设备上下文
        saveDC.SelectObject(saveBitMap)

        # 执行截图操作
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

        # 获取位图信息
        bmp_info = saveBitMap.GetInfo()
        bmp_str = saveBitMap.GetBitmapBits(True)

        # 转换为OpenCV格式 (高度, 宽度, 通道)
        img = np.frombuffer(bmp_str, dtype=np.uint8)
        img = img.reshape((bmp_info["bmHeight"], bmp_info["bmWidth"], 4))

        # 转换颜色空间 BGRA to BGR (去掉alpha通道)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        return img

    finally:
        # 资源释放
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)


def show_img(image_name, image, resize=1.0):
    img = cv2.resize(
        image,
        (int(image.shape[1] * resize), int(image.shape[0] * resize)),
        interpolation=cv2.INTER_AREA,
    )
    cv2.imshow(image_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 获取截图
    screenshot = capture_screen_to_cv()
    # 在OpenCV中使用
    show_img("name", screenshot, 0.5)

    # 可进行其他OpenCV处理
    # gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
