"""
任务执行引擎
负责解析和执行函数调用
"""

from typing import Any, Dict

from src.controllers.app_controller import AppController
from src.controllers.file_controller import FileController
from src.controllers.music_controller import MusicController
from src.controllers.system_controller import SystemController
from src.controllers.writing_controller import WritingController
from src.logger import logger


class TaskExecutor:
    """任务执行引擎"""

    def __init__(self):
        """初始化执行引擎"""
        self.music_controller = MusicController()
        self.writing_controller = WritingController()
        self.file_controller = FileController()
        self.app_controller = AppController()
        self.system_controller = SystemController()

    def execute(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """
        执行函数调用

        Args:
            function_name: 函数名称
            arguments: 函数参数

        Returns:
            执行结果描述
        """
        try:
            print(f"\n⚙️ 执行函数: {function_name}")
            print(f"📋 参数: {arguments}")

            # 路由到对应的控制器
            if function_name == "play_music":
                return self._handle_play_music(arguments)

            elif function_name == "write_article":
                return self._handle_write_article(arguments)

            elif function_name == "open_application":
                return self._handle_open_application(arguments)

            elif function_name == "file_operation":
                return self._handle_file_operation(arguments)

            elif function_name == "system_control":
                return self._handle_system_control(arguments)

            elif function_name == "search_music":
                return self._handle_search_music(arguments)

            else:
                logger.error(f"未知的函数 - {function_name}")
            return f"错误: 未知的函数 - {function_name}"

        except Exception as e:
            logger.error(f"执行函数 {function_name} 时出错: {str(e)}")
            return f"执行函数时出错: {str(e)}"

    def _handle_play_music(self, args: Dict[str, Any]) -> str:
        """处理音乐播放"""
        action = args.get("action")
        file_path = args.get("file_path")

        if action == "play":
            if not file_path:
                return "错误: 播放音乐需要指定文件路径"
            return self.music_controller.play(file_path)

        elif action == "pause":
            return self.music_controller.pause()

        elif action == "resume":
            return self.music_controller.resume()

        elif action == "stop":
            return self.music_controller.stop()

        else:
            return f"错误: 未知的音乐操作 - {action}"

    def _handle_write_article(self, args: Dict[str, Any]) -> str:
        """处理文章写作"""
        topic = args.get("topic")
        length = args.get("length", "medium")
        save_path = args.get("save_path")

        if not topic:
            return "错误: 写文章需要指定主题"

        return self.writing_controller.write_article(topic, length, save_path)

    def _handle_open_application(self, args: Dict[str, Any]) -> str:
        """处理打开应用"""
        app_name = args.get("app_name")

        if not app_name:
            return "错误: 需要指定应用程序名称"

        return self.app_controller.open_application(app_name)

    def _handle_file_operation(self, args: Dict[str, Any]) -> str:
        """处理文件操作"""
        operation = args.get("operation")
        file_path = args.get("file_path")
        content = args.get("content", "")

        if not file_path:
            return "错误: 需要指定文件路径"

        if operation == "create":
            return self.file_controller.create_file(file_path, content)

        elif operation == "read":
            return self.file_controller.read_file(file_path)

        elif operation == "delete":
            return self.file_controller.delete_file(file_path)

        else:
            return f"错误: 未知的文件操作 - {operation}"

    def _handle_system_control(self, args: Dict[str, Any]) -> str:
        """处理系统控制"""
        action = args.get("action")
        value = args.get("value", 10)

        if action == "volume_up":
            return self.system_controller.volume_up(value)

        elif action == "volume_down":
            return self.system_controller.volume_down(value)

        elif action == "set_volume":
            if value is None:
                return "错误: 设置音量需要指定数值"
            return self.system_controller.set_volume(value)

        elif action == "screenshot":
            return self.system_controller.take_screenshot()

        else:
            return f"错误: 未知的系统操作 - {action}"

    def _handle_search_music(self, args: Dict[str, Any]) -> str:
        """处理音乐搜索"""
        keyword = args.get("keyword")

        if not keyword:
            return "错误: 需要指定搜索关键词"

        return self.music_controller.search_music(keyword)
