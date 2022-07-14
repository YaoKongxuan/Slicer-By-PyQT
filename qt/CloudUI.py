import os
import sys  # 系统参数操作
import PyQt5
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *  # 含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本
import requests
from InformationalUI import InformationalUI
from hdfs import *

class CloudUI(QTabWidget):
    def __init__(self, *args, **kwargs):
        '''
        构造函数，初始化登录对话框的内容
        :param args:
        :param kwargs:
        '''
        super(CloudUI, self).__init__()
        self.new_flag = False
        self.new_local_file_path = None
        self.dow_save_file_path = None
        self.up_local_file_path = None
        self.up_flag = False
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        self.setWindowTitle("云端数据管理")

        try:
            url = "http://localhost:8080/user/getdatas?username={username}"
            f = open("user.txt", encoding='gbk')
            txt = []
            for line in f:
                txt.append(line.strip())
            f.close()
            data = {"username": txt[0]}
            r = requests.get(url.format(**data))
            self.dow_datas = r.json()["data"]
        except Exception as e:
            self.informationalUI = InformationalUI("网络错误！")
            self.informationalUI.show()
        print(self.dow_datas)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.addTab(self.tab1, 'Tab1')
        self.addTab(self.tab2, 'Tab2')
        self.addTab(self.tab3, 'Tab3')
        self.addTab(self.tab4, 'Tab4')
        self.addTab(self.tab5, 'Tab5')
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()

    # 下载
    def tab1UI(self):
        layout = QFormLayout()

        self.dow_bingren_username = QLabel(self)
        self.dow_bingren_username.setText("病人用户名")
        # 下拉框
        self.dow_bingren_comboBox = QComboBox(self)
        self.dow_bingren_comboBox.addItems(list(self.dow_datas.keys()))

        self.dow_bingren_comboBox.currentIndexChanged[int].connect(self.comboBox_dow_bingren)

        self.dow_bingren_name_label = QLabel(self)
        self.dow_bingren_name_label.setText("病人姓名")
        self.dow_bingren_name = QLabel(self)

        self.dow_bingren_hospital_label = QLabel(self)
        self.dow_bingren_hospital_label.setText("医院")
        self.dow_bingren_hospital = QLabel(self)

        self.dow_bingren_other_label = QLabel(self)
        self.dow_bingren_other_label.setText("病人简介")
        self.dow_bingren_other = QLabel(self)


        self.dow_file_name = QLabel(self)
        self.dow_file_name.setText("项目名称")
        self.dow_file_comboBox = QComboBox(self)

        self.dow_file_comboBox.currentIndexChanged[int].connect(self.comboBox_dow_project)

        self.dow_project_other_label = QLabel(self)
        self.dow_project_other_label.setText("项目简介")
        self.dow_project_other = QLabel(self)

        self.dow_choice_path_Button = QPushButton()
        self.dow_choice_path_Button.setText("选择保存路径")
        # 绑定按钮事件
        self.dow_choice_path_Button.clicked.connect(self.button_dow_file_path)

        self.dow_save_path = QLabel(self)

        self.dow_ok_Button = QPushButton()
        self.dow_ok_Button.setText("确认下载")
        # 绑定按钮事件
        self.dow_ok_Button.clicked.connect(self.button_dow_file_ok)

        # 载入进度条控件
        self.dow_pgb = QProgressBar(self)
        # 配置一个值表示进度条的当前进度
        self.dow_pv = 0
        # 设置进度条的范围
        self.dow_pgb.setMinimum(0)
        self.dow_pgb.setMaximum(100)
        self.dow_pgb.setValue(self.dow_pv)
        self.dow_pgb.setVisible(False)
        # 申明一个时钟控件
        self.dow_timer = QTimer()
        self.dow_timer.start(1000)  # 设置定时器的定时间隔时间，为1000ms，即1秒
        self.dow_timer.timeout.connect(self.dow_timerEvent)
        self.dow_timer.stop()

        self.dow_jindu = QLabel(self)

        layout.addRow(self.dow_bingren_username, self.dow_bingren_comboBox)
        layout.addRow(self.dow_bingren_name_label,self.dow_bingren_name)
        layout.addRow(self.dow_bingren_hospital_label, self.dow_bingren_hospital)
        layout.addRow(self.dow_bingren_other_label, self.dow_bingren_other)
        layout.addRow(self.dow_file_name, self.dow_file_comboBox)
        layout.addRow(self.dow_project_other_label, self.dow_project_other)
        layout.addRow(self.dow_choice_path_Button, self.dow_save_path)
        layout.addRow(self.dow_ok_Button)
        layout.addRow(self.dow_pgb)
        layout.addWidget(self.dow_jindu)
        self.setTabText(0, "下载数据")
        self.tab1.setLayout(layout)

    # 上传
    def tab2UI(self):
        layout = QFormLayout()

        self.up_bingren_username = QLabel(self)
        self.up_bingren_username.setText("病人用户名")
        self.up_bingren_comboBox = QComboBox(self)
        self.up_bingren_comboBox.addItems(list(self.dow_datas.keys()))

        self.up_bingren_comboBox.currentIndexChanged[int].connect(self.comboBox_up_bingren)
        self.up_bingren_name_label = QLabel(self)
        self.up_bingren_name_label.setText("病人姓名")
        self.up_bingren_name = QLabel(self)

        self.up_bingren_hospital_label = QLabel(self)
        self.up_bingren_hospital_label.setText("医院")
        self.up_bingren_hospital = QLabel(self)

        self.up_bingren_other_label = QLabel(self)
        self.up_bingren_other_label.setText("病人简介")
        self.up_bingren_other = QLabel(self)
        
        self.up_bingren_master = QRadioButton('上传至病人master文件', self)
        self.up_bingren_master.clicked.connect(self.radioButton_up_bingren_master)

        self.up_choice_path_Button = QPushButton()
        self.up_choice_path_Button.setText("选择上传文件")
        # 绑定按钮事件
        self.up_choice_path_Button.clicked.connect(self.button_up_file_path)

        self.up_local_path = QLabel(self)

        self.up_file_name = QLineEdit()  # 定义用户名输入框
        self.up_file_name.setPlaceholderText("请输入项目名称")  # 设置默认显示的提示语
        
        self.up_file_other = QLineEdit()  # 定义用户名输入框
        self.up_file_other.setPlaceholderText("请输入项目简介")  # 设置默认显示的提示语
        
        self.up_ok_Button = QPushButton()
        self.up_ok_Button.setText("确认上传")
        # 绑定按钮事件
        self.up_ok_Button.clicked.connect(self.button_up_file_ok)

        # 载入进度条控件
        self.up_pgb = QProgressBar(self)
        # 配置一个值表示进度条的当前进度
        self.up_pv = 0
        # 设置进度条的范围
        self.up_pgb.setMinimum(0)
        self.up_pgb.setMaximum(100)
        self.up_pgb.setValue(self.up_pv)
        self.up_pgb.setVisible(False)
        # 申明一个时钟控件
        self.up_timer = QTimer()
        self.up_timer.start(1000)  # 设置定时器的定时间隔时间，为1000ms，即1秒
        self.up_timer.timeout.connect(self.up_timerEvent)
        self.up_timer.stop()

        self.up_jindu = QLabel(self)

        layout.addRow(self.up_bingren_username, self.up_bingren_comboBox)
        layout.addRow(self.up_bingren_name_label,self.up_bingren_name)
        layout.addRow(self.up_bingren_hospital_label, self.up_bingren_hospital)
        layout.addRow(self.up_bingren_other_label, self.up_bingren_other)
        layout.addRow(self.up_bingren_master)
        layout.addRow(self.up_choice_path_Button,self.up_local_path)
        layout.addRow(self.up_file_name)
        layout.addRow(self.up_file_other)
        layout.addRow(self.up_ok_Button)
        layout.addRow(self.up_pgb)
        layout.addWidget(self.up_jindu)
        self.setTabText(1, "上传文件")
        self.tab2.setLayout(layout)

    # 删除
    def tab3UI(self):
        layout = QFormLayout()

        self.del_bingren_username = QLabel(self)
        self.del_bingren_username.setText("病人用户名")
        # 下拉框
        self.del_bingren_comboBox = QComboBox(self)
        self.del_bingren_comboBox.addItems(list(self.dow_datas.keys()))

        self.del_bingren_comboBox.currentIndexChanged[int].connect(self.comboBox_del_bingren)

        self.del_bingren_name_label = QLabel(self)
        self.del_bingren_name_label.setText("病人姓名")
        self.del_bingren_name = QLabel(self)

        self.del_bingren_hospital_label = QLabel(self)
        self.del_bingren_hospital_label.setText("医院")
        self.del_bingren_hospital = QLabel(self)

        self.del_bingren_other_label = QLabel(self)
        self.del_bingren_other_label.setText("病人简介")
        self.del_bingren_other = QLabel(self)

        self.del_file_name = QLabel(self)
        self.del_file_name.setText("项目名称")
        self.del_file_comboBox = QComboBox(self)

        self.del_file_comboBox.currentIndexChanged[int].connect(self.comboBox_del_project)

        self.del_project_other_label = QLabel(self)
        self.del_project_other_label.setText("项目简介")
        self.del_project_other = QLabel(self)


        self.del_ok_Button = QPushButton()
        self.del_ok_Button.setText("确认删除")
        # 绑定按钮事件
        self.del_ok_Button.clicked.connect(self.button_del_file_ok)


        layout.addRow(self.del_bingren_username, self.del_bingren_comboBox)
        layout.addRow(self.del_bingren_name_label, self.del_bingren_name)
        layout.addRow(self.del_bingren_hospital_label, self.del_bingren_hospital)
        layout.addRow(self.del_bingren_other_label, self.del_bingren_other)
        layout.addRow(self.del_file_name, self.del_file_comboBox)
        layout.addRow(self.del_project_other_label, self.del_project_other)
        layout.addRow(self.del_ok_Button)
        self.setTabText(2, "删除文件")
        self.tab3.setLayout(layout)

    # 注册病人
    def tab4UI(self):
        layout = QFormLayout()


        self.new_bingren_username = QLineEdit()  # 定义用户名输入框
        self.new_bingren_username.setPlaceholderText("请输入病人用户名")  # 设置默认显示的提示语

        self.new_bingren_name = QLineEdit()  # 定义用户名输入框
        self.new_bingren_name.setPlaceholderText("请输入病人姓名")  # 设置默认显示的提示语

        self.new_bingren_hospital = QLineEdit()  # 定义用户名输入框
        self.new_bingren_hospital.setPlaceholderText("请输入病人医院")  # 设置默认显示的提示语

        self.new_bingren_other = QLineEdit()  # 定义用户名输入框
        self.new_bingren_other.setPlaceholderText("请输入病人简介")  # 设置默认显示的提示语
        
        self.new_choice_path_Button = QPushButton()
        self.new_choice_path_Button.setText("选择上传文件")
        # 绑定按钮事件
        self.new_choice_path_Button.clicked.connect(self.button_new_file_path)

        self.new_local_path = QLabel(self)

        self.new_ok_Button = QPushButton()
        self.new_ok_Button.setText("确认新建")
        # 绑定按钮事件
        self.new_ok_Button.clicked.connect(self.button_new_file_ok)

        # 载入进度条控件
        self.new_pgb = QProgressBar(self)
        # 配置一个值表示进度条的当前进度
        self.new_pv = 0
        # 设置进度条的范围
        self.new_pgb.setMinimum(0)
        self.new_pgb.setMaximum(100)
        self.new_pgb.setValue(self.new_pv)
        self.new_pgb.setVisible(False)
        # 申明一个时钟控件
        self.new_timer = QTimer()
        self.new_timer.start(1000)  # 设置定时器的定时间隔时间，为1000ms，即1秒
        self.new_timer.timeout.connect(self.new_timerEvent)
        self.new_timer.stop()

        self.new_jindu = QLabel(self)

        layout.addRow(self.new_bingren_username)
        layout.addRow(self.new_bingren_name)
        layout.addRow(self.new_bingren_hospital)
        layout.addRow(self.new_bingren_other)
        layout.addRow(self.new_choice_path_Button, self.new_local_path)
        layout.addRow(self.new_ok_Button)
        layout.addRow(self.new_pgb)
        layout.addWidget(self.new_jindu)
        self.setTabText(3, "新建病人")
        self.tab4.setLayout(layout)

    # 添加权限
    def tab5UI(self):
        layout = QFormLayout()

        self.change_bingren_username = QLabel(self)
        self.change_bingren_username.setText("病人用户名")
        self.change_bingren_comboBox = QComboBox(self)
        self.change_bingren_comboBox.addItems(list(self.dow_datas.keys()))

        self.change_bingren_comboBox.currentIndexChanged[int].connect(self.comboBox_change_bingren)
        
        self.change_bingren_name_label = QLabel(self)
        self.change_bingren_name_label.setText("病人姓名")
        self.change_bingren_name = QLabel(self)

        self.change_bingren_hospital_label = QLabel(self)
        self.change_bingren_hospital_label.setText("医院")
        self.change_bingren_hospital = QLabel(self)

        self.change_bingren_other_label = QLabel(self)
        self.change_bingren_other_label.setText("病人简介")
        self.change_bingren_other = QLabel(self)

        self.change_user_name = QLineEdit()  # 定义用户名输入框
        self.change_user_name.setPlaceholderText("请输入要添加的医生用户名")  # 设置默认显示的提示语

        self.change_ok_Button = QPushButton()
        self.change_ok_Button.setText("确认添加")
        # 绑定按钮事件
        self.change_ok_Button.clicked.connect(self.button_change_file_ok)

        layout.addRow(self.change_bingren_username,self.change_bingren_comboBox)
        layout.addRow(self.change_bingren_name_label,self.change_bingren_name)
        layout.addRow(self.change_bingren_hospital_label,self.change_bingren_hospital)
        layout.addRow(self.change_bingren_other_label,self.change_bingren_other)
        layout.addRow(self.change_user_name)
        layout.addRow(self.change_ok_Button)
        self.setTabText(4, "添加权限")
        self.tab5.setLayout(layout)

    def button_dow_file_path(self):
        m = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹")
        self.dow_save_path.setText(m)
        self.dow_save_file_path = m

    def button_dow_file_ok(self):
        if self.dow_save_file_path is None or self.dow_save_file_path == "":
            self.informationalUI = InformationalUI("请选择保存路径！")
            self.informationalUI.show()
            return
        if self.dow_timer.isActive():
            self.dow_timer.stop()
            self.dow_ok_Button.setText("开始下载")
            # 停止下载线程
        else:
            try:
                url = "http://ip-api.com/json/"
                r = requests.get(url)
                r = r.json()
                url = "http://localhost:8080/user/getdowweb?userLat="+str(r["lat"])+"&userLon="+str(r["lon"])
                r = requests.get(url)
                r = r.json()
                # 开始下载线程
                HDFSConn = Client(r["web"]+":50070")
                self.dow_pgb.setVisible(True)
                self.dow_timer.start(1000)
                self.dow_ok_Button.setText("停止下载")
                f = open("user.txt", encoding='gbk')
                txt = []
                for line in f:
                    txt.append(line.strip())
                f.close()
                if not os.path.exists(self.dow_save_file_path+"/temp_"+ self.dow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText()+".txt", encoding='gbk'):
                    length = HDFSConn.content("/dicoms/"+self.dow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText()+"zip")
                    with open(self.dow_save_file_path+"/temp_"+ self.dow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText()+".txt", encoding='gbk') as f:
                        f.write("0")
                        f.write(length["length"])
                    for i in range(int(int(length["length"])/1024) + 1):
                        with HDFSConn.read("/dicoms/"+self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText()+"zip",offset = i*1024,length=1024) as reader:
                            f = open(self.dow_save_file_path+"/temp_"+ self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText(), "a", encoding="utf-8")
                            f.write(reader.read())
                            f.close()
                        with open(self.dow_save_file_path + "/temp_" + self.ow_bingren_comboBox.currentText() + "_" + txt[
                            0] + "_" + self.dow_file_comboBox.currentText() + ".txt", encoding='gbk') as f:
                            f.write(str(1024*i))
                            f.write(length["length"])
                else:
                    f = open(self.dow_save_file_path+"/temp_"+ self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText()+".txt", encoding='gbk')
                    txt = []
                    for line in f:
                        txt.append(line.strip())
                    f.close()
                    for i in range(int(int(txt[0])/1024),int(int(txt[1]) / 1024) + 1):
                        with HDFSConn.read("/dicoms/"+self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText()+"zip",offset = i*1024,length=1024) as reader:
                            f = open(self.dow_save_file_path+"/temp_"+ self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.dow_file_comboBox.currentText(), "a", encoding="utf-8")
                            f.write(reader.read())
                            f.close()
            except Exception as e:
                self.informationalUI = InformationalUI("网络错误！")
                self.informationalUI.show()

    def dow_timerEvent(self):
        if self.dow_pv == 100:
            self.dow_timer.stop()
            self.dow_ok_Button.setText("下载完成")
            self.informationalUI = InformationalUI("下载完成！")
            self.informationalUI.show()
        else:
            # 从下载文件夹处读取下载进度
            self.dow_pv += 1
            self.dow_pgb.setValue(self.dow_pv)
            self.dow_jindu.setText(str(self.dow_pv)+"%")

    def comboBox_dow_bingren(self, index):
        self.dow_bingren_name.setText(self.dow_datas[self.dow_bingren_comboBox.currentText()]["realname"])
        self.dow_bingren_hospital.setText(self.dow_datas[self.dow_bingren_comboBox.currentText()]["hospital"])
        self.dow_bingren_other.setText(self.dow_datas[self.dow_bingren_comboBox.currentText()]["patientother"])
        self.dow_file_comboBox.clear()
        self.dow_file_comboBox.addItems(self.dow_datas[self.dow_bingren_comboBox.currentText()]["projects"].keys())

    def comboBox_dow_project(self, index):
        try:
            self.dow_project_other.setText(self.dow_datas[self.dow_bingren_comboBox.currentText()]["projects"][self.dow_file_comboBox.currentText()])
        except Exception as e:
            pass


    def comboBox_up_bingren(self, index):
        self.up_bingren_name.setText(self.dow_datas[self.up_bingren_comboBox.currentText()]["realname"])
        self.up_bingren_hospital.setText(self.dow_datas[self.up_bingren_comboBox.currentText()]["hospital"])
        self.up_bingren_other.setText(self.dow_datas[self.up_bingren_comboBox.currentText()]["patientother"])
        if self.dow_datas[self.up_bingren_comboBox.currentText()]["root"] == "yes":
            self.up_bingren_master.setVisible(True)
        else:
            self.up_bingren_master.setVisible(False)
        self.up_file_name.setVisible(True)
        self.up_file_other.setVisible(True)

    def button_up_file_path(self):
        m = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, "选取文件")
        self.up_local_path.setText(m[0])
        self.up_local_file_path = m[0]

    def button_up_file_ok(self):
        if self.up_local_file_path is None or self.up_local_file_path == "":
            self.informationalUI = InformationalUI("请选择上传文件！")
            self.informationalUI.show()
            return
        if self.up_local_file_path.split(".")[-1] != "zip":
            self.informationalUI = InformationalUI("请使用zip格式压缩包上传文件！")
            self.informationalUI.show()
            return
        if not self.up_bingren_master.isChecked() and self.up_file_name.text() == "":
            self.informationalUI = InformationalUI("非上传master项目请输入上传项目名称！")
            self.informationalUI.show()
            return
        if self.up_file_name.text() in self.dow_datas[self.up_bingren_comboBox.currentText()]["projects"].keys():
            self.informationalUI = InformationalUI("项目名重复！")
            self.informationalUI.show()
            return
        if self.up_timer.isActive():
            self.up_timer.stop()
            self.up_ok_Button.setText("开始上传")
            # 停止上传线程
        else:
            try:
                if not self.up_bingren_master.isChecked() or self.up_flag:
                    self.up_flag = True
                    url = "http://localhost:8080/user/newproject?username={username}&patientname={patientname}&projectname={projectname}&other={other}"
                    f = open("user.txt", encoding='gbk')
                    txt = []
                    for line in f:
                        txt.append(line.strip())
                    f.close()
                    data = {"username": txt[0], "patientname": self.up_bingren_comboBox.currentText(),
                            "projectname": self.up_file_name.text(),
                            "other": self.up_file_other.text()}
                    r = requests.get(url.format(**data))
                url = "http://ip-api.com/json/"
                r = requests.get(url)
                r = r.json()
                url = "http://localhost:8080/user/getdowweb?userLat="+str(r["lat"])+"&userLon="+str(r["lon"])
                r = requests.get(url)
                r = r.json()

                self.up_pgb.setVisible(True)
                self.up_timer.start(1000)
                # 开始上传线程
                HDFSConn = Client(r["web"]+":50070")
                f = open("user.txt", encoding='gbk')
                txt = []
                for line in f:
                    txt.append(line.strip())
                f.close()
                if not os.path.exists("temp_"+ self.up_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.up_file_name.text()+".txt", encoding='gbk'):
                    length = os.path.getsize(self.up_local_file_path)
                    with open("temp_"+ self.up_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.up_file_name.text()+".txt", encoding='gbk') as f:
                        f.write("0")
                        f.write(str(length))
                    with open(self.up_local_file_path) as f:
                        for i in range(int(int(length)/1024) + 1):
                            reads = f.read(1024)
                            HDFSConn.upload("/dicoms/"+self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.up_file_name.text()+".zip",reads)
                            with open("temp_" + self.up_bingren_comboBox.currentText() + "_" + txt[
                                0] + "_" + self.up_file_name.text() + ".txt", encoding='gbk') as f:
                                f.write(str(1024*i))
                                f.write(str(length))
                            f.seek(1024, 1)
                else:
                    f = open("temp_"+ self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.up_file_name.text()+".txt", encoding='gbk')
                    txt = []
                    for line in f:
                        txt.append(line.strip())
                    f.close()
                    with open(self.up_local_file_path) as f:
                        length = os.path.getsize(self.up_local_file_path)
                        for i in range(int(int(txt[0]) / 1024), int(int(txt[1]) / 1024) + 1):
                            reads = f.read(1024)
                            HDFSConn.upload("/dicoms/"+self.ow_bingren_comboBox.currentText()+"_"+txt[0]+"_"+self.up_file_name.text()+".zip",reads)
                            with open("temp_" + self.up_bingren_comboBox.currentText() + "_" + txt[
                                0] + "_" + self.up_file_name.text() + ".txt", encoding='gbk') as f:
                                f.write(str(1024*i))
                                f.write(str(length))
                            f.seek(1024, 1)

                self.up_ok_Button.setText("停止上传")
            except Exception as e:
                self.informationalUI = InformationalUI("网络错误！")
                self.informationalUI.show()

    def up_timerEvent(self):
        if self.up_pv == 100:
            self.up_timer.stop()
            self.up_ok_Button.setText("上传完成")
            self.informationalUI = InformationalUI("上传完成！")
            self.informationalUI.show()
        else:
            # 从上传文件夹处读取下载进度
            self.up_pv += 1
            self.up_pgb.setValue(self.up_pv)
            self.up_jindu.setText(str(self.up_pv)+"%")
            
    def radioButton_up_bingren_master(self):
        self.up_file_name.setVisible(not self.up_bingren_master.isChecked())
        self.up_file_other.setVisible(not self.up_bingren_master.isChecked())
        
    def comboBox_del_bingren(self, index):
        self.del_bingren_name.setText(self.dow_datas[self.del_bingren_comboBox.currentText()]["realname"])
        self.del_bingren_hospital.setText(self.dow_datas[self.del_bingren_comboBox.currentText()]["hospital"])
        self.del_bingren_other.setText(self.dow_datas[self.del_bingren_comboBox.currentText()]["patientother"])
        self.del_file_comboBox.clear()
        self.del_file_comboBox.addItems(self.dow_datas[self.del_bingren_comboBox.currentText()]["projects"].keys())

    def comboBox_del_project(self, index):
        try:
            self.del_project_other.setText(self.dow_datas[self.del_bingren_comboBox.currentText()]["projects"][self.del_file_comboBox.currentText()])
        except Exception as e:
            pass

    def button_del_file_ok(self):
        if self.del_file_comboBox.currentText() == "":
            self.informationalUI = InformationalUI("请选择要删除的项目！")
            self.informationalUI.show()
            return
        if self.del_file_comboBox.currentText() == "master":
            self.informationalUI = InformationalUI("master项目无法删除！")
            self.informationalUI.show()
            return
        try:
            url = "http://localhost:8080/user/delproject?username={username}&patientname={patientname}&projectname={projectname}"
            f = open("user.txt", encoding='gbk')
            txt = []
            for line in f:
                txt.append(line.strip())
            f.close()
            data = {"username": txt[0],"patientname":self.del_bingren_comboBox.currentText(),"projectname":self.del_file_comboBox.currentText()}
            r = requests.get(url.format(**data))
            if r.json()["code"] != 200:
                self.informationalUI = InformationalUI("服务器错误，请稍后重试！")
                self.informationalUI.show()
                return
            self.informationalUI = InformationalUI("删除成功！")
            self.informationalUI.show()
        except Exception as e:
            self.informationalUI = InformationalUI("网络错误！")
            self.informationalUI.show()
        
    def button_new_file_path(self):
        m = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, "选取文件")
        self.new_local_path.setText(m[0])
        self.new_local_file_path = m[0]

    def button_new_file_ok(self):
        if self.new_bingren_name.text() == "" or self.new_bingren_username.text() == "":
            self.informationalUI = InformationalUI("请输入新建病人用户名和真实姓名！")
            self.informationalUI.show()
            return
        if self.new_local_file_path is None or self.new_local_file_path == "":
            self.informationalUI = InformationalUI("请选择上传文件！")
            self.informationalUI.show()
            return
        if self.new_local_file_path.split(".")[-1] != "zip":
            self.informationalUI = InformationalUI("请使用zip格式压缩包上传文件！")
            self.informationalUI.show()
            return
        if self.new_timer.isActive():
            self.new_timer.stop()
            self.new_ok_Button.setText("开始上传")
            # 停止上传线程
        else:
            try:
                self.new_flag = True
                url = "http://localhost:8080/user/newpatientt?username={username}&patientname={patientname}&" \
                      "hospital={hospital}&other={other}&realname={realname}"
                f = open("user.txt", encoding='gbk')
                txt = []
                for line in f:
                    txt.append(line.strip())
                f.close()
                data = {"username": txt[0], "patientname": self.new_bingren_username.text(),
                        "hospital": self.new_bingren_hospital.text(),
                        "other": self.new_bingren_other.text(),
                        "realname": self.new_bingren_name.text()}
                r = requests.get(url.format(**data))
                if r.json()["code"] != 200:
                    self.informationalUI = InformationalUI(r.json()["error"])
                    self.informationalUI.show()
                else:
                    url = "http://ip-api.com/json/"
                    r = requests.get(url)
                    r = r.json()
                    url = "http://localhost:8080/user/getdowweb?userLat="+str(r["lat"])+"&userLon="+str(r["lon"])
                    r = requests.get(url)
                    r = r.json()

                    self.new_pgb.setVisible(True)
                    self.new_timer.start(1000)
                    # 开始上传线程
                    self.new_ok_Button.setText("停止上传")
            except Exception as e:
                self.informationalUI = InformationalUI("网络错误！")
                self.informationalUI.show()
                
    def new_timerEvent(self):
        if self.new_pv == 100:
            self.new_timer.stop()
            self.new_ok_Button.setText("上传完成")
            self.informationalUI = InformationalUI("上传完成！")
            self.informationalUI.show()
        else:
            # 从上传文件夹处读取下载进度
            self.new_pv += 1
            self.new_pgb.setValue(self.new_pv)
            self.new_jindu.setText(str(self.new_pv)+"%")
            
    def comboBox_change_bingren(self, index):
        self.change_bingren_name.setText(self.dow_datas[self.change_bingren_comboBox.currentText()]["realname"])
        self.change_bingren_hospital.setText(self.dow_datas[self.change_bingren_comboBox.currentText()]["hospital"])
        self.change_bingren_other.setText(self.dow_datas[self.change_bingren_comboBox.currentText()]["patientother"])
        if self.dow_datas[self.change_bingren_comboBox.currentText()]["root"] == "yes":
            self.change_ok_Button.setEnabled(True)
        else:
            self.change_ok_Button.setEnabled(False)

    def button_change_file_ok(self):
        if self.change_user_name.text() == "":
            self.informationalUI = InformationalUI("请输入要添加权限的用户名！")
            self.informationalUI.show()
            return
        try:
            url = "http://localhost:8080/user/addrelationship?username={username}&patientname={patientname}"
            data = {"username": self.change_user_name.text(), "patientname": self.change_bingren_comboBox.currentText()}
            r = requests.get(url.format(**data))
            if r.json()["code"] != 200:
                self.informationalUI = InformationalUI(r.json()["error"])
                self.informationalUI.show()
            else:
                self.informationalUI = InformationalUI("添加成功！")
                self.informationalUI.show()
        except Exception as e:
            self.informationalUI = InformationalUI("网络错误！")
            self.informationalUI.show()

    # 获取HDFS连接
    def getHDFSConn(self,str):
        client = None
        try:
            client = Client(str+":50070", root='/')
        except Exception as e:
            print(e)
        return client
