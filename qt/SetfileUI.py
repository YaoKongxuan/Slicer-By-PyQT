import sys  # 系统参数操作
import os
import PyQt5
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *  # 含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本
import requests
import rarfile
import zipfile
import py7zr
from InformationalUI import InformationalUI
from CloudUI import CloudUI
from VtkUIrealize import VtkUIrealize


class SetfileUI(QTabWidget):
    def __init__(self, *args, **kwargs):
        '''
        构造函数，初始化登录对话框的内容
        :param args:
        :param kwargs:
        '''
        super(SetfileUI, self).__init__()

        self.new_dic_file_path = None
        self.new_dic_file_path_Btn = None
        self.new_dic_file_path_Button = None
        self.input_new_dic_file_path = None
        self.open_file_path = None
        self.open_file_ok_Button = None
        self.open_file_cloud_Button = None
        self.open_file_path_Button = None
        self.input_open_file_path = None
        self.informationalUI = None
        self.new_file_path = None
        self.input_new_file_name = None
        self.input_new_file_path = None
        self.new_file_path_Button = None
        self.new_file_name = None
        self.new_file_cloud_Button = None
        self.new_file_ok_Button = None

        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        self.setWindowTitle("选择项目")

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, 'Tab1')
        self.addTab(self.tab2, 'Tab2')
        self.tab1UI()
        self.tab2UI()

    def tab1UI(self):
        layout = QFormLayout()

        self.input_open_file_path = QLabel(self)

        self.open_file_path_Button = QPushButton()  # 定义登录按钮
        self.open_file_path_Button.setText("选择路径")  # 按钮显示值为新建
        # 绑定按钮事件
        self.open_file_path_Button.clicked.connect(self.button_open_file_path)

        self.open_file_cloud_Button = QPushButton()
        self.open_file_cloud_Button.setText("管理云端项目")
        # 绑定按钮事件
        self.open_file_cloud_Button.clicked.connect(self.button_cloud)

        self.open_file_ok_Button = QPushButton()
        self.open_file_ok_Button.setText("确认打开")
        # 绑定按钮事件
        self.open_file_ok_Button.clicked.connect(self.button_open_file)

        layout.addRow(self.open_file_path_Button, self.input_open_file_path)
        layout.addRow(self.open_file_ok_Button)
        layout.addRow(self.open_file_cloud_Button)
        self.setTabText(0, "打开项目")
        self.tab1.setLayout(layout)

    def tab2UI(self):

        layout = QFormLayout()

        self.new_file_ok_Button = QPushButton()
        self.new_file_ok_Button.setText("确认新建")
        # 绑定按钮事件
        self.new_file_ok_Button.clicked.connect(self.button_new_file)

        self.new_file_cloud_Button = QPushButton()
        self.new_file_cloud_Button.setText("管理云端项目")
        # 绑定按钮事件
        self.new_file_cloud_Button.clicked.connect(self.button_cloud)

        self.new_file_name = QLineEdit()  # 定义用户名输入框

        self.new_file_path_Button = QPushButton()  # 定义登录按钮
        self.new_file_path_Button.setText("选择路径")  # 按钮显示值为新建
        # 绑定按钮事件
        self.new_file_path_Button.clicked.connect(self.button_new_file_path)

        self.input_new_file_path = QLabel(self)
        self.input_new_file_name = QLabel(self)

        self.new_dic_file_path_Btn = QRadioButton("是否添加dic文件")  # 实例化一个选择的按钮
        self.new_dic_file_path_Btn.clicked.connect(self.radioButton_new_dic_file_path_Btn)


        self.new_dic_file_path_Button = QPushButton()  # 定义登录按钮
        self.new_dic_file_path_Button.setText("选择dic压缩包路径")  # 按钮显示值为新建
        # 绑定按钮事件
        self.new_dic_file_path_Button.clicked.connect(self.button_new_dic_file_path)
        self.input_new_dic_file_path = QLabel(self)

        self.input_new_file_name.setText("请输入项目名称")
        layout.addRow(self.input_new_file_name, self.new_file_name)
        layout.addRow(self.new_file_path_Button, self.input_new_file_path)
        layout.addRow(self.new_dic_file_path_Btn)
        layout.addRow(self.new_dic_file_path_Button, self.input_new_dic_file_path)
        layout.addRow(self.new_file_ok_Button)
        layout.addRow(self.new_file_cloud_Button)

        self.setTabText(1, "新建项目")
        self.tab2.setLayout(layout)

    def button_new_file(self):
        if self.new_file_path is None or self.new_file_name.text() is None:
            self.informationalUI = InformationalUI("请输入路径！")
            self.informationalUI.show()
        elif not os.path.isdir(self.new_file_path + "/" + self.new_file_name.text()):
            if self.new_dic_file_path_Btn.isChecked():
                if self.new_dic_file_path is None:
                    self.informationalUI = InformationalUI("没有选择dic文件！")
                    self.informationalUI.show()
                    return
                if self.new_dic_file_path.split(".")[-1] not in ("7z", "rar", 'zip'):
                    self.informationalUI = InformationalUI("选取的dic文件格式必须为zip rar 7z中一种！")
                    self.informationalUI.show()
                    return
            with open("project.txt", "w") as f:
                f.write(self.new_file_path+"/"+self.new_file_name.text()+"/")

            os.makedirs(self.new_file_path + "/" + self.new_file_name.text())
            os.makedirs(self.new_file_path + "/" + self.new_file_name.text() + "/dict")
            with open(self.new_file_path + "/" + self.new_file_name.text() + "/init.txt", "w") as f:
                f.write("ykx")  # 自带文件关闭功能，不需要再写f.close()
            if self.new_dic_file_path_Btn.isChecked():
                geshi = self.new_dic_file_path.split(".")
                if geshi == "zip":
                    zip = zipfile.ZipFile(self.new_dic_file_path)
                    zip.extractall(self.new_file_path + "/" + self.new_file_name.text() + "/dict")
                elif geshi == "rar":
                    rar = rarfile.RarFile(self.new_dic_file_path)
                    # 解压缩到指定目录
                    rar.extractall(self.new_file_path + "/" + self.new_file_name.text() + "/dict")
                else:
                    z = py7zr.SevenZipFile(self.new_dic_file_path, 'r')
                    z.extractall(path=self.new_file_path + "/" + self.new_file_name.text() + "/dict")
                    z.close()
            self.vtkUI = VtkUIrealize()
            self.vtkUI.show()
            self.informationalUI = InformationalUI("项目建立成功！")
            self.informationalUI.show()
        else:
            self.informationalUI = InformationalUI("路径有误请重新输入！")
            self.informationalUI.show()

    def button_open_file(self):
        if self.open_file_path is None:
            self.informationalUI = InformationalUI("请先选择路径！")
            self.informationalUI.show()
            return
        if os.path.isfile(self.open_file_path + "/" + "init.txt"):
            f = open(self.open_file_path + "/" + "init.txt", encoding='utf-8')
            txt = []
            for line in f:
                txt.append(line.strip())
            if txt[0] == "ykx":
                with open("project.txt", "w") as f:
                    f.write(self.open_file_path)
            else:
                self.informationalUI = InformationalUI("选择的路径没有项目！")
                self.informationalUI.show()
                return
            self.vtkUI = VtkUIrealize()
            self.vtkUI.show()
            self.informationalUI = InformationalUI("项目打开成功！")
            self.informationalUI.show()

        else:
            self.informationalUI = InformationalUI("选择的路径没有项目！")
            self.informationalUI.show()

    def button_cloud(self):
        self.cloudUI = CloudUI()
        self.cloudUI.show()

    def button_new_file_path(self):
        m = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹")
        self.input_new_file_path.setText(m)
        self.new_file_path = m

    def button_open_file_path(self):
        m = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹")
        self.input_open_file_path.setText(m)
        self.open_file_path = m

    def button_new_dic_file_path(self):
        m = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, "选取文件")
        self.input_new_dic_file_path.setText(m[0])
        self.new_dic_file_path = m[0]

    def radioButton_new_dic_file_path_Btn(self):
        self.new_dic_file_path_Button.setVisible(not self.new_dic_file_path_Btn.isChecked())
        self.input_new_dic_file_path.setVisible(not self.new_dic_file_path_Btn.isChecked())