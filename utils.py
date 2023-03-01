from datetime import datetime

# 定义颜色
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#7C7C7C"
DARK_GRAY = "#3C3F41"
BLUE = "#2F80ED"

# 日期格式化
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def format_datetime(dt):
    """
    格式化日期时间为字符串

    Args:
        dt: datetime.datetime 对象

    Returns:
        格式化后的字符串
    """
    return dt.strftime(DATETIME_FORMAT)
