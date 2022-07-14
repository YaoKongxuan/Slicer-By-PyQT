from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QLabel


class DrewQlabel(QLabel):
    def __init__(self, parent):
        super(DrewQlabel, self).__init__(parent)
        canvas = QPixmap(256, 192)
        canvas.fill(QColor(0, 0, 0, 100))
        self.setPixmap(canvas)
        self.color = None
        self.data = []
        self.drew_flag = False
        self.data_init = {}

    def paintEvent(self, event):
        if len(self.data_init.keys()) != 0:
            for color, indexdata in self.data_init.items():
                painter = QPainter()
                painter.begin(self)
                colors = color.split("_")
                pen = QPen(QColor(int(colors[0]), int(colors[1]), int(colors[2])), 1, Qt.SolidLine)
                painter.setPen(pen)
                if len(indexdata) > 1:
                    point_start = indexdata[0]
                    for pos_tmp in indexdata:
                        point_end = pos_tmp
                        if point_end == (-1, -1):
                            point_start = (-1, -1)
                            continue
                        if point_start == (-1, -1):
                            point_start = point_end
                            continue
                        painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                        point_start = point_end
                painter.end()
        if self.drew_flag:
            painter = QPainter()
            painter.begin(self)
            pen = QPen(self.color, 1, Qt.SolidLine)
            painter.setPen(pen)
            '''
                首先判断pos_xy列表中是不是至少有两个点了
                然后将pos_xy中第一个点赋值给point_start
                利用中间变量pos_tmp遍历整个pos_xy列表
                    point_end = pos_tmp

                    判断point_end是否是断点，如果是
                        point_start赋值为断点
                        continue
                    判断point_start是否是断点，如果是
                        point_start赋值为point_end
                        continue

                    画point_start到point_end之间的线
                    point_start = point_end
                这样，不断地将相邻两个点之间画线，就能留下鼠标移动轨迹了
            '''
            if len(self.data) > 1:
                point_start = self.data[0]
                for pos_tmp in self.data:
                    point_end = pos_tmp
                    if point_end == (-1, -1):
                        point_start = (-1, -1)
                        continue
                    if point_start == (-1, -1):
                        point_start = point_end
                        continue
                    painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                    point_start = point_end
            painter.end()

    def mouseMoveEvent(self, event):
        '''
            按住鼠标移动事件：将当前点添加到pos_xy列表中
            调用update()函数在这里相当于调用paintEvent()函数
            每次update()时，之前调用的paintEvent()留下的痕迹都会清空
        '''
        self.update()
        if self.drew_flag:
            # 中间变量pos_tmp提取当前点
            pos_tmp = (event.pos().x(), event.pos().y())
            # pos_tmp添加到self.pos_xy中
            self.data.append(pos_tmp)
            self.update()

    def mouseReleaseEvent(self, event):
        '''
            重写鼠标按住后松开的事件
            在每次松开后向pos_xy列表中添加一个断点(-1, -1)
            然后在绘画时判断一下是不是断点就行了
            是断点的话就跳过去，不与之前的连续
        '''
        if self.drew_flag:
            pos_test = (-1, -1)
            self.data.append(pos_test)
            self.update()