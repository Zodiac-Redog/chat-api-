import sys
import openai
import json
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize ,QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QSizePolicy, QMessageBox, QDesktopWidget, QGridLayout, QInputDialog, QWidget, QTextEdit, QStyle, QFileDialog, QFrame

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_key = None
        self.conversation_history = []

        self.settings = QSettings("ChatGPT", "history")

        self.initUI()

    def initUI(self):
        self.setWindowTitle('与 ChatGPT 对话')
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(800, 600)

        # 创建顶部栏
        top_bar = QFrame(self)
        top_bar.setFrameShape(QFrame.NoFrame)
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("""
            background-color: #222;
            color: white;
        """)
        top_layout = QHBoxLayout(top_bar)

        # 创建logo
        logo = QLabel("ChatGPT", top_bar)
        logo.setFont(QFont("Arial", 20))
        logo.setStyleSheet("""
            font-weight: bold;
            color: #70b2e0;
        """)
        top_layout.addWidget(logo)

        # 创建api key输入框和登录按钮
        self.api_key_input = QLineEdit(top_bar)
        self.api_key_input.setFont(QFont("Arial", 12))
        self.api_key_input.setPlaceholderText("输入您的 API KEY")
        top_layout.addWidget(self.api_key_input)

        login_btn = QPushButton("登录", top_bar)
        login_btn.setFont(QFont("Arial", 12))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #70b2e0;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3c8cbd;
            }
        """)
        login_btn.clicked.connect(self.login)
        top_layout.addWidget(login_btn)

        # 创建中心部分
        central_widget = QWidget(self)
        central_widget.setStyleSheet("""
            background-color: #e5e5e5;
        """)

        # 创建输入框和发送按钮
        self.input_box = QLineEdit(central_widget)
        self.input_box.setFont(QFont("Arial", 16))
        self.input_box.setPlaceholderText("输入消息...")
        self.send_btn = QPushButton("发送", central_widget)
        self.send_btn.setFont(QFont("Arial", 16))
        self.send_btn.setShortcut("Return")

        # 创建聊天文本框
        self.chat_box = QTextEdit(central_widget)
        self.chat_box.setFont(QFont("Arial", 16))
        self.chat_box.setReadOnly(True)
        self.chat_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # 创建垂直布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_box)

        # 创建水平布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.input_box)
        hbox.addWidget(self.send_btn)
        vbox.addLayout(hbox)

        # 设置聊天窗口的布局
        central_widget.setLayout(vbox)

        # 创建底部栏
        bottom_bar = QFrame(self)
        bottom_bar.setFrameShape(QFrame.NoFrame)
        bottom_bar.setFixedHeight(50)
        bottom_bar.setStyleSheet("""
            background-color: #222;
            color: white;
        """)
        bottom_layout = QHBoxLayout(bottom_bar)

        # 创建历史记录按钮
        history_btn = QPushButton("历史记录", bottom_bar)
        history_btn.setFont(QFont("Arial", 12))
        history_btn.setCursor(Qt.PointingHandCursor)
        history_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                color: #70b2e0;
            }
        """)
        history_btn.clicked.connect(self.show_history)
        bottom_layout.addWidget(history_btn)

        # 创建保存聊天记录按钮
        save_btn = QPushButton("保存聊天记录", bottom_bar)
        save_btn.setFont(QFont("Arial", 12))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                color: #70b2e0;
            }
        """)
        save_btn.clicked.connect(self.save_conversation)
        bottom_layout.addWidget(save_btn)

        # 创建导入聊天记录按钮
        import_btn = QPushButton("导入聊天记录", bottom_bar)
        import_btn.setFont(QFont("Arial", 12))
        import_btn.setCursor(Qt.PointingHandCursor)
        import_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                color: #70b2e0;
            }
        """)
        import_btn.clicked.connect(self.import_conversation)
        bottom_layout.addWidget(import_btn)

        # 将各部分添加到主窗口中
        self.setCentralWidget(central_widget)
        self.setMenuWidget(top_bar)
        self.statusBar().addWidget(bottom_bar)


        # 连接发送按钮的点击事件
        self.send_btn.clicked.connect(self.send_message)

    def login(self):

        self.api_key = self.api_key_input.text().strip()
        if not self.api_key:
            QMessageBox.critical(self, '错误', '请输入有效的 API KEY！')
        else:
            # 使用输入的 API Key 创建 OpenAI 对象
            openai.api_key = self.api_key
            QMessageBox.information(self, '登录成功', '您已成功登录 OpenAI！')

    def send_message(self):
        # 获取用户输入的消息
        message = self.input_box.text().strip()

        # 清空输入框
        self.input_box.setText("")

        # 如果消息不为空，则发送给 ChatGPT
        if message:
            try:
                # 发送请求
                response = openai.Completion.create(
                    engine="davinci",
                    #davinci-codex
                    #Davinci-instruct-beta
                    prompt="",
                    max_tokens=2048,
                    temperature=0.7,
                    n = 1,
                    stop=None,
                    prompt_suffix="\n\n",
                    frequency_penalty=0,
                    presence_penalty=0
                )


                # 解析响应并将其添加到聊天框中
                text = response.choices[0].text.strip()
                self.chat_box.append("<font color='blue'><b>您：</b></font>" + message)
                self.chat_box.append("<font color='green'><b>ChatGPT：</b></font>" + text)

            # 将对话记录添加到历史记录中
                self.history.append((message, text))

            except Exception as e:
                # 显示错误消息
                QMessageBox.critical(self, '错误', '无法连接到 ChatGPT 服务器！')

        # 如果消息为空，则不执行任何操作
        else:
            pass

    def show_history(self):
        # 创建历史记录对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("历史记录")
        dialog.setMinimumWidth(400)
        dialog.setMinimumHeight(300)
        layout = QVBoxLayout(dialog)

        # 创建滚动区域
        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget(scroll_area)
        scroll_area.setWidget(scroll_area_widget)
        layout.addWidget(scroll_area)

        # 创建垂直布局
        vbox = QVBoxLayout(scroll_area_widget)

        # 添加历史记录条目
        for message, response in self.history:
            hbox = QHBoxLayout()
            message_label = QLabel("<font color='blue'><b>您：</b></font>" + message)
            response_label = QLabel("<font color='green'><b>ChatGPT：</b></font>" + response)
            hbox.addWidget(message_label)
            hbox.addWidget(response_label)
            vbox.addLayout(hbox)

        # 显示历史记录对话框
        dialog.exec_()

    def save_conversation(self):
        # 弹出保存文件对话框
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存聊天记录", "", "Text Files (*.txt)")

        # 如果用户选择了文件，则将对话记录保存到文件中
        if file_name:
            with open(file_name, 'w') as f:
                for message, response in self.history:
                    f.write("您：" + message + "\n")
                    f.write("ChatGPT：" + response + "\n")
                    f.write("\n")

            QMessageBox.information(self, '保存成功', '聊天记录已成功保存！')

    def import_conversation(self):
        # 弹出打开文件对话框
        file_name, _ = QFileDialog.getOpenFileName(
            self, "导入聊天记录", "", "Text Files (*.txt)")

        # 如果用户选择了文件，则读取文件中的对话记录并添加到历史记录中
        if file_name:
            with open(file_name, 'r') as f:
                lines = f.readlines()
                messages = [line.strip()[2:] for i, line in enumerate(lines) if i % 2 == 0]
                responses = [line.strip()[8:] for i, line in enumerate(lines) if i % 2 == 1]
                self.history.extend(list(zip(messages, responses)))

            QMessageBox.information(self, '导入成功', '聊天记录已成功导入！')
'''
class MainWindow(QWidget):
    def init(self):
        super().init()
        # 初始化聊天窗口
        self.chat_window = ChatWindow()
        self.chat_window.message_received.connect(self.on_message_received)
        self.chat_window.history_requested.connect(self.show_history)
        self.chat_window.conversation_saved.connect(self.save_conversation)
        self.chat_window.conversation_imported.connect(self.import_conversation)

        # 创建 API KEY 输入框和按钮
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("请输入您的 OpenAI API KEY")
        self.api_key_input.setMinimumWidth(400)
        self.api_key_btn = QPushButton("保存", clicked=self.save_api_key)

        # 创建水平布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.api_key_input)
        hbox.addWidget(self.api_key_btn)

        # 创建垂直布局
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.chat_window)

        # 设置布局
        self.setLayout(vbox)

    def save_api_key(self):
        api_key = self.api_key_input.text().strip()
        if api_key:
            self.chat_window.api_key = api_key
            QMessageBox.information(self, 'API KEY 保存成功', 'API KEY 已成功保存！')
        else:
            QMessageBox.critical(self, '错误', '请输入有效的 API KEY！')

    def on_message_received(self, message, response):
        self.chat_window.add_message(message, response)

    def show_history(self):
        self.chat_window.show_history()

    def save_conversation(self):
        self.chat_window.save_conversation()

    def import_conversation(self):
        self.chat_window.import_conversation()
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ChatWindow()
    main_window.show()
    sys.exit(app.exec_())