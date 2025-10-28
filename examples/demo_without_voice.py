#!/usr/bin/env python3
"""
无语音演示脚本
用于在没有麦克风的环境中测试功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_client import LLMClient
from src.task_executor import TaskExecutor
import config


def demo():
    """演示程序"""
    print("=" * 60)
    print("PC Voice Assist - 无语音演示")
    print("=" * 60)
    print()
    
    # 检查API Key
    if not config.OPENAI_API_KEY:
        print("❌ 错误: 未设置OPENAI_API_KEY环境变量")
        return
    
    # 初始化组件
    print("正在初始化...")
    llm_client = LLMClient()
    task_executor = TaskExecutor()
    print("✅ 初始化完成!\n")
    
    # 演示对话
    test_queries = [
        "你好,介绍一下你的功能",
        "帮我在桌面创建一个文件,文件名是demo.txt,内容是'这是一个演示文件'",
        "读取刚才创建的文件",
        "搜索音乐目录中的音乐文件",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"👤 用户: {query}")
        print(f"{'='*60}")
        
        # 发送给大模型
        response_text, function_calls = llm_client.chat(query)
        
        if response_text:
            print(f"🤖 助手: {response_text}")
        
        # 执行函数调用
        if function_calls:
            for func_call in function_calls:
                print(f"\n⚙️ 执行函数: {func_call['name']}")
                print(f"📋 参数: {func_call['arguments']}")
                
                # 执行
                result = task_executor.execute(
                    func_call["name"],
                    func_call["arguments"]
                )
                
                print(f"✅ 执行结果: {result}")
                
                # 返回结果给大模型
                final_response = llm_client.add_function_result(
                    func_call["id"],
                    func_call["name"],
                    result
                )
                
                if final_response:
                    print(f"🤖 助手: {final_response}")
        
        print()
    
    print("=" * 60)
    print("演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n收到中断信号,退出演示")
    except Exception as e:
        print(f"❌ 演示出错: {str(e)}")
        sys.exit(1)

