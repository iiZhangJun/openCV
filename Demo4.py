from mpl_toolkits.mplot3d import Axes3D
import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('faceImg.jpg')
"""
如果直方图中的成分过于靠近0或255，可能会出现暗部细节不足或者亮部细节丢失的情况
"""
# 分通道计算每个通道的直方图
hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([img],[1],None,[256],[0,256])
hist_r = cv2.calcHist([img],[2],None,[256],[0,256])

#定义Gamma矫正的函数
def gamma_trans(img,gamma):
    # 具体做法是先归一化到1，然后gamma作为指数值求出新的像素再还原
    gamma_table = [np.power(x/255.0, gamma)*255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # 实现映射用的是Opencv的查表函数
    return cv2.LUT(img, gamma_table)

#执行Gamma矫正，小于1的值让暗部细节大量提升，同时亮部细节少量提升
img_corrected = gamma_trans(img,0.5)
cv2.imwrite('gamma_corrected.jpg', img_corrected)
# 分通道计算Gamma矫正后的直方图
hist_b_corrected = cv2.calcHist([img_corrected],[0],None,[256],[0,256])
hist_g_corrected = cv2.calcHist([img_corrected],[1],None,[256],[0,256])
hist_r_corrected = cv2.calcHist([img_corrected],[2],None,[256],[0,256])
# 将直方图进行可视化
fig = plt.figure()
pix_hist = [
    [hist_b,hist_g,hist_r],
    [hist_b_corrected,hist_g_corrected,hist_r_corrected]
]
pix_vals = range(256)
for sub_plt, pix_hist in zip([121,122],pix_hist):
    ax = fig.add_subplot(sub_plt, projection='3d')
    for c,z,channel_hist in zip(['b','g','r'],[20,10,0],pix_hist):
        cs = [c] * 256
        ax.bar(pix_vals,channel_hist,zs=z, zdir='y',color=cs,alpha=0.168, edgecolor='none',lw=0)
#     ax.set_xlabel('pixel Values')
#     ax.set_xlim([0,256])
#     ax.set_ylabel('Counts')
#     ax.set_zlabel("Channels")
# plt.show()




