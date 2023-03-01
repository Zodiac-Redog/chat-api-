from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QTextCharFormat, QFont
from PyQt5.QtWidgets import QTextEdit


class ChatWindow(QTextEdit):
    def __init__(self, api_key, **kwargs):
        super().__init__(**kwargs)

        # 保存对话历史记录
        self.history = []

        # 保存上下文
        self.context = None

        # API Key
        self.api_key = api_key

        # 设置文本框属性
        self.setReadOnly(True)
        self.setAcceptRichText(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapAnywhere)

        # 设置样式
        self.setStyleSheet(
            """
            ChatWindow {
                background-color: #f5f5f5;
                border: 2px solid #d3d3d3;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-family: Arial, Helvetica, sans-serif;
            }
            """
        )

        # 设置字体
        font = QFont("Arial", 16)
        self.setFont(font)

        # 创建输入框并设置样式
        self.input_box = QTextEdit(self)
        self.input_box.setMaximumHeight(80)
        self.input_box.setStyleSheet(
            """
            QTextEdit {
                background-color: #ffffff;
                border: 2px solid #d3d3d3;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-family: Arial, Helvetica, sans-serif;
            }
            """
        )
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTabChangesFocus(True)

        # 设置字体
        font = QFont("Arial", 16)
        self.input_box.setFont(font)

    def get_input_text(self):
        """
        获取输入框的文本内容
        """
        return self.input_box.toPlainText().strip()

    def clear_input_box(self):
        """
        清空输入框的文本内容
        """
        self.input_box.clear()

    def add_chat_text(self, text, sender="user", color=None):
        """
        将文本添加到聊天框中
        """
        # 获取当前光标位置
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        # 添加发送者信息
        if sender == "chatbot":
            text = "\nChatBot: " + text
        else:
            text = "\nUser: " + text

        # 添加颜色标签
        if color:
            fmt = QTextCharFormat()
            fmt.setForeground(QPalette(color))
            cursor.insertText(text, fmt)
        else:
            cursor.insertText(text)

        # 移动光标到末尾
        self.setTextCursor(cursor)

    def add_chat_history(self, text):
        """
        将聊天历史记录添加到 history 列表中
        """
        self.history.append(text)

    def show_chat_history(self):
        """
        在聊天框中显示历史记录
        """
        # 获取当前光标位置
        cursor = self.input_box.textCursor()
        pos = cursor.position()

        # 获取历史记录
        history = self.get_chat_history()

        # 遍历历史记录，插入到聊天框中
        for item in history:
            text = item['text']
            is_user = item['is_user']
            context = item['context']
            response = item['response']
            color_tag = item['color_tag']

            # 创建新的文本块
            block = QTextBlock()

            # 设置文本块的属性
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignLeft)
            block_format.setLineHeight(150, QTextBlockFormat.FixedHeight)
            block.setBlockFormat(block_format)

            # 插入文本块到文档中
            self.chat_box.document().insertBlock(block)

            # 获取新插入的文本块
            block = self.chat_box.document().findBlockByLineNumber(self.chat_box.document().blockCount() - 1)

            # 创建富文本
            rich_text = QTextCharFormat()

            # 根据用户或chatgpt的不同，设置不同的文本样式
            if is_user:
                rich_text.setForeground(QColor('#0080FF'))
            else:
                rich_text.setForeground(QColor('#666666'))

            # 设置颜色标签
            if color_tag:
                rich_text.setFontUnderline(True)
                if color_tag == 'warning':
                    rich_text.setForeground(QColor('#ff0000'))
                elif color_tag == 'success':
                    rich_text.setForeground(QColor('#008000'))
                elif color_tag == 'info':
                    rich_text.setForeground(QColor('#1E90FF'))

            # 插入文本到文本块中
            block_text = text.replace('\n', '<br>')
            rich_text.setToolTip('上下文：' + context + '\n回复：' + response)
            rich_text.setAnchorHref(response)
            self.chat_box.textCursor().insertHtml(f'<span style="font-size: 14px">{block_text}</span>')
            self.chat_box.setCurrentCharFormat(rich_text)

        # 恢复光标位置
        cursor.setPosition(pos)
        self.input_box.setTextCursor(cursor)
