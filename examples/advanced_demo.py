#!/usr/bin/env python3
"""
高级功能演示脚本
展示复杂任务编排和多步骤操作
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_client import LLMClient
from src.task_executor import TaskExecutor
import config


def demo_complex_tasks():
    """演示复杂任务编排"""
    print("=" * 60)
    print("PC Voice Assist - 高级功能演示")
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
    
    # 复杂任务示例
    complex_queries = [
        {
            "query": "帮我在桌面创建一个文件叫notes.txt,内容是'今天要完成的任务',然后读取这个文件确认内容",
            "description": "多步骤文件操作"
        },
        {
            "query": "搜索音乐目录中的音乐文件,如果找到就播放第一首",
            "description": "条件执行"
        },
        {
            "query": "帮我写一篇短文,主题是科技发展,保存到桌面,文件名是tech.md",
            "description": "AI写作并保存"
        }
    ]
    
    for i, item in enumerate(complex_queries, 1):
        print(f"\n{'='*60}")
        print(f"示例 {i}: {item['description']}")
        print(f"{'='*60}")
        print(f"👤 用户: {item['query']}")
        print(f"{'='*60}")
        
        # 发送给大模型
        response_text, function_calls = llm_client.chat(item['query'])
        
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
        input("按回车继续下一个示例...")
    
    print("=" * 60)
    print("演示完成!")
    print("=" * 60)


def demo_conversation_context():
    """演示对话上下文管理"""
    print("\n" + "=" * 60)
    print("对话上下文演示")
    print("=" * 60)
    print()
    
    llm_client = LLMClient()
    task_executor = TaskExecutor()
    
    # 多轮对话
    conversations = [
        "帮我写一篇关于人工智能的短文",
        "把它保存到桌面",
        "文件名叫做ai_article.md"
    ]
    
    for i, query in enumerate(conversations, 1):
        print(f"\n第 {i} 轮对话:")
        print(f"👤 用户: {query}")
        
        response_text, function_calls = llm_client.chat(query)
        
        if response_text:
            print(f"🤖 助手: {response_text}")
        
        if function_calls:
            for func_call in function_calls:
                result = task_executor.execute(
                    func_call["name"],
                    func_call["arguments"]
                )
                print(f"✅ 执行: {result}")
                
                final_response = llm_client.add_function_result(
                    func_call["id"],
                    func_call["name"],
                    result
                )
                
                if final_response:
                    print(f"🤖 助手: {final_response}")
        
        input("按回车继续...")
    
    print("\n✅ 对话上下文演示完成!")


def demo_error_handling():
    """演示错误处理"""
    print("\n" + "=" * 60)
    print("错误处理演示")
    print("=" * 60)
    print()
    
    task_executor = TaskExecutor()
    
    # 测试各种错误情况
    error_cases = [
        {
            "name": "file_operation",
            "args": {"operation": "read", "file_path": "/nonexistent/file.txt"},
            "description": "读取不存在的文件"
        },
        {
            "name": "play_music",
            "args": {"action": "play", "file_path": "/nonexistent/music.mp3"},
            "description": "播放不存在的音乐"
        },
        {
            "name": "file_operation",
            "args": {"operation": "create", "file_path": "/root/test.txt", "content": "test"},
            "description": "在不安全的目录创建文件"
        }
    ]
    
    for i, case in enumerate(error_cases, 1):
        print(f"\n测试 {i}: {case['description']}")
        print(f"函数: {case['name']}")
        print(f"参数: {case['args']}")
        
        result = task_executor.execute(case['name'], case['args'])
        print(f"结果: {result}")
        
        input("按回车继续...")
    
    print("\n✅ 错误处理演示完成!")


def main():
    """主函数"""
    print("\n选择演示模式:")
    print("1. 复杂任务编排")
    print("2. 对话上下文管理")
    print("3. 错误处理")
    print("4. 全部演示")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    try:
        if choice == "1":
            demo_complex_tasks()
        elif choice == "2":
            demo_conversation_context()
        elif choice == "3":
            demo_error_handling()
        elif choice == "4":
            demo_complex_tasks()
            demo_conversation_context()
            demo_error_handling()
        else:
            print("无效的选项")
    
    except KeyboardInterrupt:
        print("\n\n收到中断信号,退出演示")
    except Exception as e:
        print(f"❌ 演示出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

