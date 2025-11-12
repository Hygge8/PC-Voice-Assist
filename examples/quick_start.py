#!/usr/bin/env python3
"""
快速开始脚本
用于快速测试基本功能
"""
import os
import sys

# isort: skip_file
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.llm_client import LLMClient
# from src.task_executor import TaskExecutor # 仅用于测试,此处无需使用


def quick_test():
    """快速测试基本功能"""
    print("=" * 60)
    print("PC Voice Assist - 快速测试")
    print("=" * 60)
    print()

    # 检查配置
    if not config.OPENAI_API_KEY:
        print("❌ 错误: 未设置OPENAI_API_KEY环境变量")
        print("\n请先设置环境变量:")
        print("  export OPENAI_API_KEY='your-api-key'")
        return

    print("✅ API Key 已配置")
    print(f"✅ 使用模型: {config.OPENAI_MODEL}")
    print()

    # 初始化
    print("正在初始化组件...")
    try:
        llm_client = LLMClient()
        # task_executor = TaskExecutor() # 仅用于测试,此处无需使用
        print("✅ 初始化成功!\n")
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        return

    # 简单测试
    test_query = "你好,介绍一下你的功能"

    print(f"👤 测试查询: {test_query}")
    print("⏳ 正在处理...\n")

    try:
        response_text, function_calls = llm_client.chat(test_query)

        if response_text:
            print(f"🤖 助手回复:\n{response_text}\n")

        if function_calls:
            print(f"📞 函数调用: {len(function_calls)} 个")
        else:
            print("✅ 基本对话功能正常!")

        print("\n" + "=" * 60)
        print("快速测试完成!")
        print("=" * 60)
        print("\n💡 提示:")
        print("  - 运行 'python main.py' 启动完整的语音助手")
        print("  - 运行 'python examples/demo_without_voice.py' 进行无语音演示")
        print("  - 运行 'python examples/advanced_demo.py' 查看高级功能")
        print("  - 运行 'python tests/test_basic.py' 执行测试")

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    quick_test()
