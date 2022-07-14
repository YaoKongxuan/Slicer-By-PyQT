import sys  # 系统参数操作
import PyQt5
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *  # 含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本
import requests
from InformationalUI import InformationalUI


class EnrollUI(QDialog):
    def __init__(self, *args, **kwargs):
        '''
        构造函数，初始化登录对话框的内容
        :param args:
        :param kwargs:
        '''
        super().__init__(*args, **kwargs)
        self.setWindowTitle('注册用户')  # 设置标题
        self.resize(300, 200)  # 设置宽、高
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        # 表单布局
        flo = QFormLayout()
        '''
        定义界面控件设置
        '''
        self.frame = QFrame(self)  # 初始化 Frame对象
        self.verticalLayout = QVBoxLayout(self.frame)  # 设置横向布局
        self.verticalLayout

        self.login_id = QLineEdit()  # 定义用户名输入框
        self.login_id.setPlaceholderText("请输入用户名")  # 设置默认显示的提示语
        self.verticalLayout.addWidget(self.login_id)  # 将该登录账户设置添加到页面控件

        self.passwd = QLineEdit()  # 定义密码输入框
        self.passwd.setPlaceholderText("请输入密码")  # 设置默认显示的提示语
        self.passwd.setEchoMode(QLineEdit.Password)
        self.verticalLayout.addWidget(self.passwd)  # 将该登录密码设置添加到页面控件

        self.again_passwd = QLineEdit()  # 定义密码输入框
        self.again_passwd.setPlaceholderText("请再次输入密码")  # 设置默认显示的提示语
        self.again_passwd.setEchoMode(QLineEdit.Password)
        self.verticalLayout.addWidget(self.again_passwd)  # 将该登录密码设置添加到页面控件

        self.real_name = QLineEdit()  # 定义密码输入框
        self.real_name.setPlaceholderText("请输入姓名")  # 设置默认显示的提示语
        self.verticalLayout.addWidget(self.real_name)  # 将该登录密码设置添加到页面控件

        self.hospital = QLineEdit()  # 定义密码输入框
        self.hospital.setPlaceholderText("请输入所在医院")  # 设置默认显示的提示语
        self.verticalLayout.addWidget(self.hospital)  # 将该登录密码设置添加到页面控件

        self.enroll = QPushButton()  # 定义登录按钮
        self.enroll.setText("注册")  # 按钮显示值为登录
        self.verticalLayout.addWidget(self.enroll)  # 将按钮添加到页面控件

        self.button_quit = QPushButton()  # 定义返回按钮
        self.button_quit.setText("取消")  # 按钮显示值为返回
        self.verticalLayout.addWidget(self.button_quit)  # 将按钮添加到页面控件
        self.button_quit.clicked.connect(self.close)  # 返回按钮绑定到退出

        flo.addRow(self.login_id)
        flo.addRow(self.passwd)
        flo.addRow(self.again_passwd)
        flo.addRow(self.real_name)
        flo.addRow(self.hospital)
        flo.addRow(self.enroll)
        flo.addRow(self.button_quit)
        # 设置窗口的布局
        self.setLayout(flo)

        # 绑定按钮事件
        self.enroll.clicked.connect(self.button_enroll_verify)

    def button_enroll_verify(self):
        if self.passwd.text() == "" or self.login_id.text() == "":
            self.informationalUI = InformationalUI("请正确输入用户名与密码！")
            self.informationalUI.show()
            return
        if self.passwd.text() != self.again_passwd.text():
            self.informationalUI = InformationalUI("两次输入密码不一致！")
            self.informationalUI.show()
        else:
            url = "http://localhost:8080/login/zhuce?username={username}&password={password}&" \
                  "realName={realName}&hospital={hospital}"
            data = {"username": self.login_id.text(), "password": self.passwd.text(),
                    "realName": self.real_name.text(), "hospital": self.hospital.text()}
            try:
                r = requests.get(url.format(**data))
                r = r.json()
                if r["code"] != 200:
                    self.informationalUI = InformationalUI(r["error"]+"！")
                    self.informationalUI.show()
                    return
                self.informationalUI = InformationalUI("注册成功！")
                self.informationalUI.show()
            except Exception as e:
                self.informationalUI = InformationalUI("网络错误！")
                self.informationalUI.show()
