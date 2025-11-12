"""
应用控制器
负责打开应用程序
"""

import platform
import subprocess

import config
from src.logger import logger


class AppController:
    """应用控制器"""

    def __init__(self):
        """初始化应用控制器"""
        self.system = platform.system()

    def open_application(self, app_name: str) -> str:
        """
        打开应用程序

        Args:
            app_name: 应用程序名称

        Returns:
            执行结果描述
        """
        try:
            # 查找应用程序命令
            app_commands = config.ALLOWED_APPLICATIONS.get(app_name, [])

            if not app_commands:
                # 尝试模糊匹配
                for key in config.ALLOWED_APPLICATIONS.keys():
                    if app_name in key or key in app_name:
                        app_commands = config.ALLOWED_APPLICATIONS[key]
                        app_name = key
                        break

            if not app_commands:
                available_apps = ", ".join(config.ALLOWED_APPLICATIONS.keys())
                return f"错误: 未找到应用程序 '{app_name}'\n可用的应用: {available_apps}"

            # 尝试每个命令
            for cmd in app_commands:
                try:
                    if self.system == "Linux":
                        # Linux系统
                        subprocess.Popen(
                            [cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                        )
                        return f"已打开应用: {app_name}"
                    elif self.system == "Darwin":
                        # macOS系统
                        subprocess.Popen(
                            ["open", "-a", cmd],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        return f"已打开应用: {app_name}"
                    elif self.system == "Windows":
                        # Windows系统
                        subprocess.Popen(
                            ["start", cmd],
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        return f"已打开应用: {app_name}"
                except FileNotFoundError:
                    continue

            return f"错误: 无法打开应用 '{app_name}',可能未安装"

        except Exception as e:
            logger.error(f"打开应用时出错: {str(e)}")
            return f"打开应用时出错: {str(e)}"
