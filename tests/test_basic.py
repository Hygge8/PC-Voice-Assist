"""
基础功能测试
"""

import os
import sys

# isort: skip_file
# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controllers.file_controller import FileController
from src.controllers.music_controller import MusicController
from src.task_executor import TaskExecutor


def test_file_controller():
    """测试文件控制器"""
    print("测试文件控制器...")

    controller = FileController()

    # 测试创建文件
    test_file = os.path.expanduser("~/Desktop/test_voice_assist.txt")
    result = controller.create_file(test_file, "这是一个测试文件")
    print(f"创建文件: {result}")

    # 测试读取文件
    result = controller.read_file(test_file)
    print(f"读取文件: {result}")

    # 测试删除文件
    result = controller.delete_file(test_file)
    print(f"删除文件: {result}")

    print("✅ 文件控制器测试完成\n")


def test_music_controller():
    """测试音乐控制器"""
    print("测试音乐控制器...")

    controller = MusicController()

    # 测试搜索音乐
    result = controller.search_music("test")
    print(f"搜索音乐: {result}")

    # 测试获取状态
    result = controller.get_status()
    print(f"播放状态: {result}")

    print("✅ 音乐控制器测试完成\n")


def test_task_executor():
    """测试任务执行引擎"""
    print("测试任务执行引擎...")

    executor = TaskExecutor()

    # 测试文件操作
    test_file = os.path.expanduser("~/Desktop/test_executor.txt")
    result = executor.execute(
        "file_operation",
        {"operation": "create", "file_path": test_file, "content": "任务执行引擎测试"},
    )
    print(f"执行结果: {result}")

    # 清理
    executor.execute("file_operation", {"operation": "delete", "file_path": test_file})

    print("✅ 任务执行引擎测试完成\n")


if __name__ == "__main__":
    print("=" * 60)
    print("PC Voice Assist - 基础功能测试")
    print("=" * 60)
    print()

    try:
        test_file_controller()
        test_music_controller()
        test_task_executor()

        print("=" * 60)
        print("所有测试完成!")
        print("=" * 60)

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        sys.exit(1)
