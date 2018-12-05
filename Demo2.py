import cv2

#读取一张人脸照片500,333
img = cv2.imread('faceImg.jpg')
# 缩放成200x200的方形图像
img_200x200 = cv2.resize(img,(200, 200))
cv2.imwrite('resized_200x200.jpg',img_200x200)
#不直接指定缩放后大小，通过fx和fy指定缩放比例，0.5则长宽都为原来一半
# 等效于 img_200*300 = cv2.resize(img,(300,200)),注意指定大小的格式是（宽度、高度）
# 插值方法默认是从cv2.INTER_LINEAR，这里指定为最近邻插值
img_250x168 = cv2.resize(img,(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
cv2.imwrite('resized_250x168.jpg',img_250x168)
# 在原始图片的基础上，上下各贴50像素的黑边，生成250x268的图像
img_500x433 = cv2.copyMakeBorder(img, 50, 50, 0, 0, cv2.BORDER_CONSTANT)
cv2.imwrite('resized_500x433.jpg',img_500x433)
#对照片中人脸进行剪裁
patch_face = img[20:150,-180:-50]
cv2.imwrite('cropped_face.jpg', patch_face)