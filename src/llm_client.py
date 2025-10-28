"""
大模型客户端模块
负责与OpenAI API交互,实现Function Calling
"""
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
import config


class LLMClient:
    """大模型客户端"""
    
    def __init__(self):
        """初始化客户端"""
        self.client = OpenAI()  # API key已在环境变量中配置
        self.model = config.OPENAI_MODEL
        self.conversation_history: List[Dict[str, Any]] = []
        self.system_prompt = config.SYSTEM_PROMPT
        
        # 初始化系统消息
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def get_available_functions(self) -> List[Dict[str, Any]]:
        """获取可用的函数定义"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "play_music",
                    "description": "播放、暂停或停止音乐",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["play", "pause", "stop", "resume"],
                                "description": "播放动作: play(播放), pause(暂停), stop(停止), resume(继续)"
                            },
                            "file_path": {
                                "type": "string",
                                "description": "音乐文件路径(仅play时需要)"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_article",
                    "description": "使用AI写一篇文章并保存",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "文章主题"
                            },
                            "length": {
                                "type": "string",
                                "enum": ["short", "medium", "long"],
                                "description": "文章长度: short(短), medium(中), long(长)"
                            },
                            "save_path": {
                                "type": "string",
                                "description": "保存路径,如果不指定则保存到默认文档目录"
                            }
                        },
                        "required": ["topic"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "打开应用程序",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {
                                "type": "string",
                                "description": "应用程序名称,如:浏览器、记事本、文件管理器、终端等"
                            }
                        },
                        "required": ["app_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "file_operation",
                    "description": "文件操作(创建、读取、删除)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["create", "read", "delete"],
                                "description": "操作类型"
                            },
                            "file_path": {
                                "type": "string",
                                "description": "文件路径"
                            },
                            "content": {
                                "type": "string",
                                "description": "文件内容(仅create时需要)"
                            }
                        },
                        "required": ["operation", "file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "system_control",
                    "description": "系统控制操作",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["volume_up", "volume_down", "set_volume", "screenshot"],
                                "description": "系统操作类型"
                            },
                            "value": {
                                "type": "integer",
                                "description": "操作值(如音量百分比0-100)"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_music",
                    "description": "在音乐目录中搜索音乐文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "搜索关键词"
                            }
                        },
                        "required": ["keyword"]
                    }
                }
            }
        ]
    
    def chat(self, user_message: str) -> tuple[Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        发送消息并获取响应
        
        Args:
            user_message: 用户消息
            
        Returns:
            (回复文本, 函数调用列表) 的元组
        """
        # 添加用户消息到历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # 限制历史长度
        if len(self.conversation_history) > config.MAX_CONVERSATION_HISTORY * 2 + 1:
            # 保留系统消息和最近的对话
            self.conversation_history = [self.conversation_history[0]] + \
                                       self.conversation_history[-(config.MAX_CONVERSATION_HISTORY * 2):]
        
        try:
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.get_available_functions(),
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # 添加助手响应到历史
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls
            })
            
            # 检查是否有函数调用
            if message.tool_calls:
                function_calls = []
                for tool_call in message.tool_calls:
                    function_calls.append({
                        "id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })
                return message.content, function_calls
            else:
                return message.content, None
                
        except Exception as e:
            error_msg = f"调用大模型时出错: {str(e)}"
            print(error_msg)
            return error_msg, None
    
    def add_function_result(self, tool_call_id: str, function_name: str, result: str) -> Optional[str]:
        """
        添加函数执行结果并获取后续响应
        
        Args:
            tool_call_id: 工具调用ID
            function_name: 函数名称
            result: 执行结果
            
        Returns:
            助手的回复文本
        """
        # 添加函数结果到历史
        self.conversation_history.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": function_name,
            "content": result
        })
        
        try:
            # 再次调用API获取基于函数结果的响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.get_available_functions(),
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # 添加助手响应到历史
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls
            })
            
            # 如果还有函数调用,返回None表示需要继续处理
            if message.tool_calls:
                return None
            
            return message.content
            
        except Exception as e:
            error_msg = f"处理函数结果时出错: {str(e)}"
            print(error_msg)
            return error_msg
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]

