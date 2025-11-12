"""
文件控制器
负责文件操作
"""

import os
from pathlib import Path


import config
from src.logger import logger


class FileController:
    """文件控制器"""

    def __init__(self):
        """初始化文件控制器"""
        pass

    def _is_safe_path(self, file_path: str) -> bool:
        """
        检查路径是否安全

        Args:
            file_path: 文件路径

        Returns:
            是否安全
        """
        try:
            # 转换为绝对路径
            abs_path = os.path.abspath(file_path)

            # 检查是否在安全目录内
            for safe_dir in config.SAFE_DIRECTORIES:
                if abs_path.startswith(os.path.abspath(safe_dir)):
                    return True

            return False
        except Exception:
            return False

    def create_file(self, file_path: str, content: str = "") -> str:
        """
        创建文件

        Args:
            file_path: 文件路径
            content: 文件内容

        Returns:
            执行结果描述
        """
        try:
            # 安全检查
            if not self._is_safe_path(file_path):
                return f"错误: 不允许在此路径创建文件 - {file_path}\n仅允许在以下目录: {', '.join(config.SAFE_DIRECTORIES)}"

            # 确保目录存在
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            # 创建文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"文件已创建: {file_path}"

        except Exception as e:
            logger.error(f"创建文件时出错: {str(e)}")
            return f"创建文件时出错: {str(e)}"

    def read_file(self, file_path: str) -> str:
        """
        读取文件

        Args:
            file_path: 文件路径

        Returns:
            文件内容或错误信息
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return f"错误: 文件不存在 - {file_path}"

            # 安全检查
            if not self._is_safe_path(file_path):
                return f"错误: 不允许读取此路径的文件 - {file_path}"

            # 读取文件
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 限制返回内容长度
            if len(content) > 1000:
                content = content[:1000] + "\n... (内容过长,已截断)"

            return f"文件内容 ({file_path}):\n{content}"

        except Exception as e:
            logger.error(f"读取文件时出错: {str(e)}")
            return f"读取文件时出错: {str(e)}"

    def delete_file(self, file_path: str) -> str:
        """
        删除文件

        Args:
            file_path: 文件路径

        Returns:
            执行结果描述
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return f"错误: 文件不存在 - {file_path}"

            # 安全检查
            if not self._is_safe_path(file_path):
                return f"错误: 不允许删除此路径的文件 - {file_path}"

            # 删除文件
            os.remove(file_path)

            return f"文件已删除: {file_path}"

        except Exception as e:
            logger.error(f"删除文件时出错: {str(e)}")
            return f"删除文件时出错: {str(e)}"
