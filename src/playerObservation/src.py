import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def imgMatch(BaseImg, InImg):
    imgA = BaseImg
    if BaseImg.shape != InImg.shape:
        imgB = cv2.resize(InImg, (imgA.shape[1], imgA.shape[0]))
    else:
        imgB = InImg
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # 计算SSIM（值范围-1到1，1表示完全相同）
    return ssim(grayA, grayB)
