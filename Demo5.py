import cv2
import numpy as np
# 读取一张照片
img = cv2.imread('faceImg.jpg')
# 沿着横纵轴放大1.6倍，然后平移（-150，-240），最后沿原图大小截取，等效于剪裁并放大
M_crop_face = np.array([
    [1.6,0,-150],
    [0,1.6,-200]
],dtype=np.float32)
img_face = cv2.warpAffine(img,M_crop_face,(500,333))
cv2.imwrite('face.jpg',img_face)

# 顺时针旋转，角度15°
theta=1
M_rotate = np.array([
    [np.cos(theta), -np.sin(theta),0],
    [np.sin(theta), np.cos(theta),0]
],dtype=np.float32)
img_rotated = cv2.warpAffine(img,M_rotate,(500,333))
cv2.imwrite('face_rotated.jpg',img_rotated)
# 某种变换，具体几何意义可以通过SVD分解理解
M = np.array([
    [1, 1.5, -400],
    [0.5, 2, -100]
],dtype=np.float32)
img_transformed = cv2.warpAffine(img,M,(500,333))
cv2.imwrite('face_transformed.jpg',img_transformed)