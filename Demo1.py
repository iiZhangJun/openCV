import numpy as np
import cv2
import matplotlib.pyplot as  plt
# 在python中图像都是用Numpy的array表示的
"""
img = np.array([
    [[255,0,0],[0,255,0],[0,0,255]],
    [[255,255,0],[255,0,255],[0,255,255]],
    [[255,255,255],[128,128,128],[0,0,0]]
],dtype=np.uint8)
# 用matplotlib存储
plt.imsave('img_pyplot.jpg', img)
# 用OpenCV存储
cv2.imwrite('img_cv2.jpg', img)
"""

# 读取一张500*333分辨率的图像
color_img = cv2.imread('faceImg.jpg')
print(color_img)
# 直接读取单通道
gray_img = cv2.imread('faceImg.jpg', cv2.IMREAD_GRAYSCALE)
print(gray_img)
# 把单通道图片保存后，再读取仍是3通道，相当于把单通道复制到3个通道保存
cv2.imwrite('gray_scale.jpg',gray_img)

reload_grayscale = cv2.imread('gray_scale.jpg')
print(reload_grayscale.shape)
# cv2.IMWRITE_JPEG_QUALITY指定jpg质量，范围为0~100，默认为95，越高画质越好，文件越大
cv2.imwrite('faceImg_imwrite.jpg',color_img,(cv2.IMWRITE_JPEG_QUALITY,80))

# CV2.IMWRITE_PNG_COMPRESSION指定png质量，范围为0~9，默认3，越高文件越小，画质越差
cv2.imwrite('faceImg_imwrite.png',color_img,(cv2.IMWRITE_PNG_COMPRESSION,5))

