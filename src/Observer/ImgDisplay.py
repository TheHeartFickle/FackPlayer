import logging
import time
from typing import Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class ImgDisplay:
    def __init__(self) -> None:
        self.imgName = f"imgDisplay_{time.time()}"
        self.size: Optional[Tuple[int, int]] = None
        self.zoom: Optional[float] = None
        self.type = "zoom"

    def name(self, name_str: str) -> "ImgDisplay":
        self.imgName = name_str
        return self

    def size(self, width: int, height: int) -> "ImgDisplay":
        """调整图像显示窗口大小"""
        self.size = (width, height)
        self.type = "resize"
        return self

    def zoom(self, zoom_factor: float) -> "ImgDisplay":
        self.zoom = zoom_factor
        self.type = "zoom"
        return self

    def Show(self, img: np.ndarray) -> None:
        """显示图像"""
        cv2.namedWindow(self.imgName)
        if self.type == "resize":
            img = cv2.resize(img, self.size)
        elif self.type == "zoom" and self.zoom is not None:
            img = cv2.resize(
                img,
                (
                    int(img.shape[1] * self.zoom),
                    int(img.shape[0] * self.zoom),
                ),
            )
        cv2.imshow(self.imgName, img)
        cv2.waitKey(0)
        try:
            cv2.destroyWindow(self.imgName)
        except Exception:
            logger.exception("Failed to destroy window: %s", self.imgName)

    @staticmethod
    def close_all_windows() -> None:
        """关闭所有OpenCV窗口"""
        cv2.destroyAllWindows()
