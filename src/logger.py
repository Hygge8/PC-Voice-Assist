"""
日志模块
"""

import logging
import logging.handlers
import os
import sys

import config


def setup_logger():
    """
    配置并返回日志记录器
    """
    logger = logging.getLogger("PCVoiceAssist")
    logger.setLevel(config.LOG_LEVEL)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 1. 控制台处理器
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(config.LOG_LEVEL)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 2. 文件处理器 (每天轮换)
    log_path = os.path.join(config.PROJECT_ROOT.parent, config.LOG_FILE)
    fh = logging.handlers.TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    fh.setLevel(config.LOG_LEVEL)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# 初始化日志记录器
logger = setup_logger()

