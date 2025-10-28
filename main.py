#!/usr/bin/env python3
"""
PC Voice Assist - 主程序
基于大模型的语音控制PC应用
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.speech_recognition_module import SpeechRecognizer
from src.text_to_speech import TextToSpeech
from src.llm_client import LLMClient
from src.task_executor import TaskExecutor
import config


class VoiceAssistant:
    """语音助手主类"""
    
    def __init__(self):
        """初始化语音助手"""
        print("=" * 60)
        print("PC Voice Assist - 语音控制PC应用")
        print("=" * 60)
        
        print("\n正在初始化组件...")
        
        # 初始化各个模块
        self.speech_recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.llm_client = LLMClient()
        self.task_executor = TaskExecutor()
        
        print("✅ 初始化完成!\n")
    
    def run(self):
        """运行主循环"""
        self.tts.speak("你好,我是你的语音助手,有什么可以帮你的吗?")
        
        while True:
            try:
                # 监听用户语音
                user_input = self.speech_recognizer.listen()
                
                if not user_input:
                    continue
                
                # 检查退出命令
                if user_input in ["退出", "再见", "结束", "关闭"]:
                    self.tts.speak("再见!")
                    break
                
                # 检查重置命令
                if user_input in ["重置对话", "清空历史", "重新开始"]:
                    self.llm_client.reset_conversation()
                    self.tts.speak("对话历史已清空")
                    continue
                
                # 发送给大模型处理
                response_text, function_calls = self.llm_client.chat(user_input)
                
                # 如果有函数调用,执行它们
                if function_calls:
                    for func_call in function_calls:
                        # 执行函数
                        result = self.task_executor.execute(
                            func_call["name"],
                            func_call["arguments"]
                        )
                        
                        print(f"✅ 执行结果: {result}")
                        
                        # 将结果返回给大模型
                        final_response = self.llm_client.add_function_result(
                            func_call["id"],
                            func_call["name"],
                            result
                        )
                        
                        # 如果有最终回复,播放给用户
                        if final_response:
                            self.tts.speak(final_response)
                
                # 如果没有函数调用,直接回复
                elif response_text:
                    self.tts.speak(response_text)
                
            except KeyboardInterrupt:
                print("\n\n收到中断信号,正在退出...")
                self.tts.speak("再见!")
                break
            
            except Exception as e:
                error_msg = f"发生错误: {str(e)}"
                print(f"❌ {error_msg}")
                self.tts.speak("抱歉,处理时出现了错误")


def main():
    """主函数"""
    # 检查环境变量
    if not config.OPENAI_API_KEY:
        print("❌ 错误: 未设置OPENAI_API_KEY环境变量")
        print("请设置环境变量后再运行程序")
        sys.exit(1)
    
    try:
        # 创建并运行助手
        assistant = VoiceAssistant()
        assistant.run()
    
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

