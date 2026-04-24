import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def similarity_in_ssim(base_img: np.ndarray, input_img: np.ndarray) -> float:
    """
    计算两张图像的 SSIM（结构相似性）

    Args:
        base_img: 基准图像
        input_img: 待比较图像

    Returns:
        SSIM 值，范围 [-1, 1]，1 表示完全相同

    Raises:
        ValueError: 输入图像为空或尺寸无效
    """
    # 输入校验
    if base_img is None or input_img is None:
        raise ValueError("输入图像不能为 None")
    if base_img.size == 0 or input_img.size == 0:
        raise ValueError("输入图像不能为空")
    if len(base_img.shape) < 2 or len(input_img.shape) < 2:
        raise ValueError("输入图像维度无效")

    # 尺寸对齐
    if base_img.shape != input_img.shape:
        img_b = cv2.resize(input_img, (base_img.shape[1], base_img.shape[0]))
    else:
        img_b = input_img

    # 灰度转换（兼容已为灰度的输入）
    if len(base_img.shape) == 3:
        gray_a = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_a = base_img
    if len(img_b.shape) == 3:
        gray_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    else:
        gray_b = img_b

    # 计算SSIM（值范围-1到1，1表示完全相同）
    return ssim(gray_a, gray_b)
