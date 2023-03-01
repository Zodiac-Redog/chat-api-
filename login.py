from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.api_key = ""

        self.initUI()

    def initUI(self):
        # 设置对话框标题和大小
        self.setWindowTitle("登录到 OpenAI")
        self.setFixedSize(300, 150)

        # 创建控件
        label = QLabel("请输入您的 OpenAI GPT-3 API Key:")
        self.edit = QLineEdit()
        self.edit.setEchoMode(QLineEdit.Password)
        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")

        # 水平布局
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.ok_btn)
        h_layout.addWidget(self.cancel_btn)

        # 垂直布局
        v_layout = QVBoxLayout()
        v_layout.addWidget(label)
        v_layout.addWidget(self.edit)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

        # 连接信号和槽
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_api_key(self):
        return self.api_key

    def accept(self):
        self.api_key = self.edit.text()
        super().accept()
