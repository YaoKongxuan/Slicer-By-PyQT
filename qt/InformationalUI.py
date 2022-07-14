import sys  # 系统参数操作
import PyQt5
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *  # 含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本


class InformationalUI(QDialog):

    def __init__(self, str):
        super(InformationalUI, self).__init__()
        self.frame = QFrame(self)  # 初始化 Frame对象
        self.verticalLayout = QVBoxLayout(self.frame)  # 设置横向布局
        self.verticalLayout

        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        self.resize(200, 100)
        self.setWindowTitle("提示")
        self.label = PyQt5.QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(str)
        self.button_quit = QPushButton()  # 定义返回按钮
        self.button_quit.setText("确定")  # 按钮显示值为返回
        self.verticalLayout.addWidget(self.button_quit)  # 将按钮添加到页面控件
        self.button_quit.clicked.connect(self.close)  # 返回按钮绑定到退出
        # 表单布局
        flo = QFormLayout()
        flo.addRow(self.label)
        flo.addRow(self.button_quit)
        # 设置窗口的布局
        self.setLayout(flo)