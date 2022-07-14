import sys  # 系统参数操作
import PyQt5
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *  # 含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本
import requests
from InformationalUI import InformationalUI
from Enroll_userUI import EnrollUI


class LoginUI(QDialog):
    def __init__(self, *args, **kwargs):
        '''
        构造函数，初始化登录对话框的内容
        :param args:
        :param kwargs:
        '''
        super().__init__(*args, **kwargs)
        self.setWindowTitle('欢迎登录医学影像云软件')  # 设置标题
        self.resize(300, 150)  # 设置宽、高
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 表单布局
        flo = QFormLayout()
        '''
        定义界面控件设置
        '''
        self.frame = QFrame(self)  # 初始化 Frame对象
        self.verticalLayout = QVBoxLayout(self.frame)  # 设置横向布局
        self.verticalLayout

        self.login_id = QLineEdit()  # 定义用户名输入框
        self.login_id.setPlaceholderText("请输入登录账号")  # 设置默认显示的提示语
        self.verticalLayout.addWidget(self.login_id)  # 将该登录账户设置添加到页面控件

        self.passwd = QLineEdit()  # 定义密码输入框
        self.passwd.setPlaceholderText("请输入登录密码")  # 设置默认显示的提示语
        self.passwd.setEchoMode(QLineEdit.Password)
        self.verticalLayout.addWidget(self.passwd)  # 将该登录密码设置添加到页面控件

        self.login = QPushButton()  # 定义登录按钮
        self.login.setText("登录")  # 按钮显示值为登录
        self.verticalLayout.addWidget(self.login)  # 将按钮添加到页面控件

        self.enroll = QPushButton()  # 定义注册按钮
        self.enroll.setText("注册")  # 按钮显示值为注册
        self.verticalLayout.addWidget(self.enroll)  # 将按钮添加到页面控件

        flo.addRow(self.login_id)
        flo.addRow(self.passwd)
        flo.addRow(self.login)
        flo.addRow(self.enroll)
        # 设置窗口的布局
        self.setLayout(flo)

        # 绑定按钮事件
        self.login.clicked.connect(self.button_login_verify)
        # 绑定按钮事件
        self.enroll.clicked.connect(self.button_enroll_verify)

    def button_login_verify(self):
        url = "http://localhost:8080/login/tologin?username={username}&password={password}"
        data = {"username": self.login_id.text(), "password": self.passwd.text()}
        if self.login_id.text() == "" or self.passwd.text() == "":
            self.informationalUI = InformationalUI("请正确输入用户名和密码！")
            self.informationalUI.show()
            return
        try:
            r = requests.get(url.format(**data))
            r = r.json()
            if r["code"] != 200:
                self.informationalUI = InformationalUI(r["error"]+"！")
                self.informationalUI.show()
                return
            with open("user.txt", "w") as f:
                f.write(r["user"]["username"])  # 自带文件关闭功能，不需要再写f.close()
            self.accept()
        except Exception as e:
            self.informationalUI = InformationalUI("网络错误！")
            self.informationalUI.show()

    def button_enroll_verify(self):
        self.enrollUI = EnrollUI()
        self.enrollUI.show()
