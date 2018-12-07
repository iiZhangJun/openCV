import os
from itertools import cycle
import cv2
# 列出frames文件夹下所有的图片
frame = 'E:\\Python\\ImgPracticeData\\hymenoptera_data\\train\\Augment_ants'
filenames = os.listdir(frame)

# 通过itertools生成一个无限循环的迭代器，每次迭代都输出下一张迭代对象
itm_iter = cycle([cv2.imread(os.sep.join([frame,filename])) for filename in filenames])
key = 0

def on_mouse(event, x, y, flags, param):
    # 鼠标左键按下，抬起，双击
    x0 = 0
    y0 = 0
    if event == cv2.EVENT_LBUTTONDOWN:
        x0 = x
        y0 = y
        print('Left button down at ({}, {})'.format(x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        print('Left button up at ({}, {})'.format(x, y))
        cv2.rectangle(img, (x0, y0), (x, y), (0, 255, 0), -1)
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        print('Left button double clicked at ({}, {})'.format(x, y))
    # 鼠标左键按下，抬起，双击
    elif event == cv2.EVENT_RBUTTONDOWN:
        print('Right button down at ({}, {})'.format(x, y))
    elif event == cv2.EVENT_RBUTTONUP:
        print('Right button up at ({}, {})'.format(x, y))
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        print('Right button double clicked at ({}, {})'.format(x, y))
    # 鼠标中/滚轮键（如果有的话）按下，抬起，双击
    elif event == cv2.EVENT_MBUTTONDOWN:
        print('Middle button down at ({}, {})'.format(x, y))
    elif event == cv2.EVENT_MBUTTONUP:
        print('Middle button up at ({}, {})'.format(x, y))
    elif event == cv2.EVENT_MBUTTONDBLCLK:
        print('Middle button double clicked at ({}, {})'.format(x, y))
        # 鼠标移动
    elif event == cv2.EVENT_MOUSEMOVE:
        print('Moving at ({}, {})'.format(x, y))


img = next(itm_iter)
# 为指定的窗口绑定自定义的回调函数
cv2.namedWindow('Honemoon Island')
cv2.setMouseCallback('Honemoon Island', on_mouse)
while key != 27:
    cv2.imshow('Honemoon Island', next(itm_iter))
    key = cv2.waitKeyEx()          # cv2.waitKeyEx()获取full key code
    # 如果获取的键值小于256则作为ASCII嘛输出对应字符，否则直接输出值
    msg = '{} is pressed'.format(key if key < 256 else key)
    print(msg)

# 上：2490368
# 下：2621440
# 左：2424832
# 右：2555904
# ESC: 27
