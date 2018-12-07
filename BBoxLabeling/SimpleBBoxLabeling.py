import os
import cv2
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno


FPS = 24
WINDOW_NAME = 'Simple Bounding Box Labeling Tool'
BAR_HEIGHT = 20
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
DEFAULT_COLOR = {'object':(255,0,0)}
SUPPORTED_FORMATS = ['jpg','png','jpeg']  # 定义支持的图像格式


# 上下左右，ESC及删除键对应的cv2.waitKeyEx()函数的返回值，这个值根据操作系统的不同有所不同
KEY_UP = 2490368
KEY_DOWN = 2621440
KEY_LEFT = 2424832
KEY_RIGHT = 2555904
KEY_DELETE = 3014656
# 空键用于默认循环
KEY_EMPTY = 32
KEY_ESC = 27


get_bbox_name = '{}.bbox'.format
"""
实现思路：
1.输入是一个文件夹，下面包含了所有要标注物体框的图片。如果图片中标注了物体，则生成一个相同名称加额外后缀名的文件保存标注信息。
2.标注的方式是按下鼠标左键选择物体框的左上角，松开鼠标左键选择物体框的右下角，鼠标右键删除上一个标注好的物体框。所有待标注物体的类别，和标注框颜色由用户自定义，如果没有定义则默认只标注一种物体，定义该物体名称叫“Object”。
3.方向键的←和→用来遍历图片，↑和↓用来选择当前要标注的物体，Delete键删除一张图片和对应的标注信息。
"""


class SimpleBBoxLabeling():
    def __init__(self,data_dir,window_name=None):

        self.window_name = window_name if window_name else WINDOW_NAME
        self._data_dir = data_dir
        self._pt1 = None
        self._pt2 = None
        self._drawing = False
        self._bbox = []      # 当前图像对应的所有已标注框
        self._cur_label = None      # 当前标注物体的名称

        # 若有用户自定义的标注信息则读取，否则用默认的物体和颜色
        label_path = '{}.labels'.format(self._data_dir)
        self.label_colors = DEFAULT_COLOR if not os.path.exists(label_path) else self.load_labels(label_path)

        # 获取已经标注的文件列表和还未标注的文件列表
        imagefiles = [x for x in os.listdir(self._data_dir) if x[x.rfind('.') + 1:].lower() in SUPPORTED_FORMATS]
        labeled = [x for x in imagefiles if os.path.exists(get_bbox_name(x))]
        to_be_labeled = [x for x in imagefiles if x not in labeled]

        # 每次打开一个文件夹，都自动从还未标注的第一张开始
        self._filelist = labeled + to_be_labeled        # 所有文件的列表  已标 + 未标
        self._index = len(labeled)                      # 使_index指向未标框的第一幅图片
        if self._index >len(self._filelist) - 1:        # 若index超出文件长度，使其指向最后一个文件
            self._index = len(self._filelist) - 1

    @staticmethod
    def load_labels(filepath):
        label_colors = {}
        with open(filepath,'r') as f:
            line = f.readline().rstrip()
            while line:
                label, color = eval(line)
                label_colors[label] = color
                line = f.readline().rstrip()
        return label_colors

    # 读取图像文件和对应标注框信息（如果有的话）
    @staticmethod
    def load_sample(filepath):
        img = cv2.imread(filepath)
        bbox_filepath = get_bbox_name(filepath)
        bboxes = []
        if os.path.exists(bbox_filepath):
            bboxes = SimpleBBoxLabeling.load_bbox(bbox_filepath)
        return img,bboxes


    # 利用eval函数读取物体及对应颜色信息到数据
    @staticmethod
    def load_bbox(filepath):
        bboxes = []
        with open(filepath,'r') as f:
            line = f.readline().rstrip()
            while line:
                bboxes.append(eval(line))
                line = f.readline().rstrip()
        return bboxes

    #利用repr()函数导出标注框数据到文件
    @staticmethod
    def export_bbox(filepath,bboxes):
        if bboxes:
            with open(filepath,'w') as f:
                for bbox in bboxes:
                    line = repr(bbox) + '\n'
                    f.write(line)
        elif os.path.exists(filepath):
            os.remove(filepath)

    # 定义鼠标回调事件
    def _on_mouse(self,event,x,y,flags,param):
        # 按下左键时，坐标为左上角，同时表明开始画框，改变drawing标记为True
        if event == cv2.EVENT_LBUTTONDOWN:
            self._drawing = True
            self._pt1 = (x,y)
        # 松开左键，表明当前框画完了，坐标记下为右下角并保存，同时改变drawing标记为False
        elif event == cv2.EVENT_LBUTTONUP:
            self._pt2 = (x,y)
            self._bbox.append((self._cur_label, (self._pt1,self._pt2)))
            self._drawing = False
        # 实时更新右下角坐标方便画框
        elif event == cv2.EVENT_MOUSEMOVE:
            self._pt2 = (x,y)
        # 按下鼠标右键删除最近画好的框
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self._bbox:
                self._bbox.pop()

    # 画标注框和当前信息
    def _draw_bbox(self,img):
        h, w = img.shape[:2]
        # 在图像下方多出BAR_HEIGHT这么多像素的区域，用于显示文件名和当前标注物体等信息
        canvas = cv2.copyMakeBorder(img,0, BAR_HEIGHT,0,0,cv2.BORDER_CONSTANT,value=COLOR_WHITE)
        # 正在标注的物体信息，如果鼠标左键已按下，则显示两个点坐标，否则显示当前待标注物体的名称
        label_msg = '{}:{},{}'.format(self._cur_label, self._pt1,self._pt2) if self._drawing else 'Current label:{}'.format(self._cur_label)
        # 显示当前文件名，文件个数信息
        msg = '{}/{}: {} | {}'.format(self._index + 1, len(self._filelist), self._filelist[self._index], label_msg)
        cv2.putText(canvas,msg,(1,h+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)
        # 画出已经标好的框和对应名字
        for label,(bpt1,bpt2) in self._bbox:
            label_color = self.label_colors[label] if label in self.label_colors else COLOR_BLACK
            cv2.rectangle(canvas,bpt1,bpt2,label_color,thickness=2)
            cv2.putText(canvas,label,(bpt1[0]+3,bpt1[1]+15),cv2.FONT_HERSHEY_SIMPLEX,0.5,label_color,2)
        # 画出正在标注的框和对应的名字
        if self._drawing:
            label_color = self.label_colors[self._cur_label] if self._cur_label in self.label_colors else COLOR_BLACK
            if self._pt2[0] >= self._pt1[0] and self._pt2[1] >= self._pt1[1]:
                cv2.rectangle(canvas,self._pt1,self._pt2,label_color,thickness=2)
                cv2.putText(canvas,self._cur_label,(self._pt1[0]+3, self._pt1[1]+15),cv2.FONT_HERSHEY_SIMPLEX,0.5,label_color,2)
        return canvas

    # 导出当前标注框信息并清空
    def _export_n_clean_bbox(self):
        bbox_filepath = os.sep.join([self._data_dir,get_bbox_name(self._filelist[self._index])])
        self.export_bbox(bbox_filepath,self._bbox)
        self._clean_bbox()

    # 清除所有标注框和当前状态
    def _clean_bbox(self):
        self.pt1 = None
        self.pt2 = None
        self.bbox = []
        self.drawing = False

    # 删除当前样本和对应的标注框信息
    def _delete_current_sample(self):
        filename = self._filelist[self._index]
        filepath = os.sep.join([self._data_dir,filename])
        if os.path.exists(filepath):
            os.remove(filepath)
        filepath = get_bbox_name(filepath)
        if os.path.exists(filepath):
            os.remove(filepath)
        self._filelist.pop(self._index)
        print('{} is delete!'.format(filename))


    # 开始OpenCV窗口循环的方法，定义了程序的主逻辑
    def start(self):
        last_filename = ''

        label_index = 0         # 标注物体在列表中的下标

        labels = list(self.label_colors.keys())              # 所有标注物体名称的列表

        #待标注物体的种类数
        n_labels = len(labels)

        # 定义窗口和鼠标回调
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name,self._on_mouse)
        key = KEY_EMPTY
        # 定义每次循环的持续时间
        delay = int(1000/FPS)
        # 只要没有按下ESC键，就持续循环
        while key != KEY_ESC:
            # 上下方向键用于选择当前标注物体
            if key == KEY_UP:
                if label_index == 0:
                    pass
                else:
                    label_index -= 1
            elif key == KEY_DOWN:
                if label_index == n_labels-1:
                    label_index = n_labels-1
                else:
                    label_index += 1
            # 左右方向键用于切换当前标注的图片
            elif key == KEY_LEFT:
                # 已经到了第一张图片的话就不需要清空上一张
                if self._index > 0:
                    self._export_n_clean_bbox()
                self._index -= 1
                if self._index < 0:
                    self._index = 0
            elif key == KEY_RIGHT:
                # 已经到了最后一张图片的话就不需要清空上一张
                if self._index < len(self._filelist)-1:
                    self._export_n_clean_bbox()
                self._index += 1
                if self._index > len(self._filelist)-1:
                    self._index = len(self._filelist)-1
            elif key == KEY_DELETE:
                if askyesno('Delete Sample','Are you sure？'):
                    self._delete_current_sample()
                    key = KEY_EMPTY
                    continue

            # 如果键盘执行了换图片，则重新读取，更新图片
            filename = self._filelist[self._index]
            if filename != last_filename:
                filepath = os.sep.join([self._data_dir,filename])
                img, self._bbox = self.load_sample(filepath)
            # 更新当前标注物体名称
            self._cur_label = labels[label_index]
            # 把标注和相关的信息画在图片上并显示指定的时间
            canvas = self._draw_bbox(img)
            cv2.imshow(self.window_name,canvas)
            key = cv2.waitKeyEx(delay)
            # 当前文件名就是下次循环的老文件名
            last_filename = filename
        print('Finished!')
        cv2.destroyAllWindows()
        # 若退出需要对当前文件进行保存
        self.export_bbox(os.sep.join([self._data_dir,get_bbox_name(filename)]),self._bbox)
        print('Labels updated')


if __name__ == '__main__':
    dir_with_images = askdirectory(title = 'where are the images?')
    labeling_task = SimpleBBoxLabeling(dir_with_images)
    labeling_task.start()









