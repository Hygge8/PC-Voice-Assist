"""
系统控制器
负责系统级操作
"""

import platform
import subprocess
from datetime import datetime
from pathlib import Path
from src.logger import logger


class SystemController:
    """系统控制器"""

    def __init__(self):
        """初始化系统控制器"""
        self.system = platform.system()

    def set_volume(self, value: int) -> str:
        """
        设置音量

        Args:
            value: 音量值 (0-100)

        Returns:
            执行结果描述
        """
        try:
            # 限制范围
            value = max(0, min(100, value))

            if self.system == "Linux":
                # Linux使用amixer或pactl
                try:
                    subprocess.run(
                        ["amixer", "set", "Master", f"{value}%"],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return f"音量已设置为 {value}%"
                except FileNotFoundError:
                    try:
                        subprocess.run(
                            ["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{value}%"],
                            check=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        return f"音量已设置为 {value}%"
                    except FileNotFoundError:
                        return "错误: 未找到音量控制工具(amixer或pactl)"

            elif self.system == "Darwin":
                # macOS使用osascript
                subprocess.run(
                    ["osascript", "-e", f"set volume output volume {value}"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return f"音量已设置为 {value}%"

            elif self.system == "Windows":
                # Windows需要使用nircmd或其他工具
                return "Windows系统音量控制需要额外工具支持"

            return "不支持的操作系统"

        except Exception as e:
            logger.error(f"设置音量时出错: {str(e)}")
            return f"设置音量时出错: {str(e)}"

    def volume_up(self, step: int = 10) -> str:
        """
        增加音量

        Args:
            step: 增加的步长

        Returns:
            执行结果描述
        """
        try:
            if self.system == "Linux":
                subprocess.run(
                    ["amixer", "set", "Master", f"{step}%+"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return f"音量已增加 {step}%"
            else:
                return "此功能仅支持Linux系统"
        except Exception as e:
            logger.error(f"增加音量时出错: {str(e)}")
            return f"增加音量时出错: {str(e)}"

    def volume_down(self, step: int = 10) -> str:
        """
        降低音量

        Args:
            step: 降低的步长

        Returns:
            执行结果描述
        """
        try:
            if self.system == "Linux":
                subprocess.run(
                    ["amixer", "set", "Master", f"{step}%-"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return f"音量已降低 {step}%"
            else:
                return "此功能仅支持Linux系统"
        except Exception as e:
            logger.error(f"降低音量时出错: {str(e)}")
            return f"降低音量时出错: {str(e)}"

    def take_screenshot(self, save_path: str = None) -> str:
        """
        截图

        Args:
            save_path: 保存路径

        Returns:
            执行结果描述
        """
        try:
            # 生成默认文件名
            if not save_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = str(Path.home() / "Pictures" / f"screenshot_{timestamp}.png")

            # 确保目录存在
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)

            if self.system == "Linux":
                # Linux使用gnome-screenshot或scrot
                try:
                    subprocess.run(
                        ["gnome-screenshot", "-f", save_path],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return f"截图已保存到: {save_path}"
                except FileNotFoundError:
                    try:
                        subprocess.run(
                            ["scrot", save_path],
                            check=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        return f"截图已保存到: {save_path}"
                    except FileNotFoundError:
                        return "错误: 未找到截图工具(gnome-screenshot或scrot)"

            elif self.system == "Darwin":
                # macOS使用screencapture
                subprocess.run(
                    ["screencapture", save_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return f"截图已保存到: {save_path}"

            elif self.system == "Windows":
                # Windows可以使用PIL
                try:
                    from PIL import ImageGrab

                    screenshot = ImageGrab.grab()
                    screenshot.save(save_path)
                    return f"截图已保存到: {save_path}"
                except ImportError:
                    return "错误: 需要安装pillow库"

            return "不支持的操作系统"

        except Exception as e:
            logger.error(f"截图时出错: {str(e)}")
            return f"截图时出错: {str(e)}"
