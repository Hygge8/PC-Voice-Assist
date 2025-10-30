# 开发文档

## 项目架构详解

PC Voice Assist 采用分层模块化架构,从底层到顶层依次为功能控制层、任务执行层、智能决策层和语音交互层。这种设计使得各个模块职责清晰,易于维护和扩展。

### 语音交互层

语音交互层负责与用户进行语音交互,包含语音识别和语音合成两个核心模块。

**语音识别模块** (`speech_recognition_module.py`) 使用 Google Speech Recognition API 将用户的语音输入转换为文本。该模块在初始化时会进行环境噪音校准,以提高识别准确率。识别过程中设置了合理的超时时间,避免长时间等待。

**语音合成模块** (`text_to_speech.py`) 使用 pyttsx3 引擎将文本转换为语音输出。该引擎支持离线运行,不依赖网络服务。模块会自动尝试选择中文语音,并允许通过配置文件调整语速和音量。

### 智能决策层

智能决策层的核心是 **LLM 客户端** (`llm_client.py`),负责与 OpenAI API 交互,实现智能理解和决策。

该模块维护了完整的对话历史,支持多轮对话。为了避免上下文过长影响性能和成本,系统会自动限制历史长度,只保留最近的对话记录。

Function Calling 是该层的关键技术。系统定义了一组标准函数接口,每个函数都有详细的参数定义和描述。大模型根据用户输入分析意图后,会返回需要调用的函数及其参数。这种机制使得系统能够将自然语言指令转换为结构化的函数调用。

### 任务执行层

**任务执行引擎** (`task_executor.py`) 是任务执行层的核心,负责解析大模型返回的函数调用,并路由到相应的控制器执行。

该模块采用策略模式,根据函数名称分发到不同的处理方法。每个处理方法负责提取参数、调用控制器、处理返回结果。这种设计使得添加新功能只需要增加新的处理方法,不影响现有代码。

### 功能控制层

功能控制层包含多个专门的控制器,每个控制器负责特定类型的操作。

**音乐控制器** (`music_controller.py`) 使用 pygame 库实现音乐播放功能。该控制器维护了播放状态,支持播放、暂停、继续和停止操作。搜索功能可以在指定目录中查找音乐文件,支持多种音频格式。

**写作控制器** (`writing_controller.py`) 利用大模型的文本生成能力创建文章。该控制器会根据用户指定的主题和长度构建合适的提示词,调用大模型生成内容,然后保存到指定位置。生成的文章包含标题、时间戳和正文,采用 Markdown 格式。

**文件控制器** (`file_controller.py`) 提供基本的文件操作功能。该控制器实现了严格的安全检查,只允许在配置的安全目录内操作。所有路径都会转换为绝对路径进行验证,防止路径遍历攻击。

**应用控制器** (`app_controller.py`) 负责打开应用程序。该控制器根据不同的操作系统使用相应的命令启动应用。支持应用名称的模糊匹配,提高用户体验。

**系统控制器** (`system_controller.py`) 提供系统级操作。音量控制功能根据操作系统选择合适的命令行工具,截图功能会自动生成带时间戳的文件名。

## 核心技术实现

### Function Calling 实现

Function Calling 的实现分为三个步骤:定义函数、调用函数、处理结果。

**定义函数**: 在 `llm_client.py` 的 `get_available_functions()` 方法中,每个函数都按照 OpenAI 的规范定义,包括函数名、描述、参数类型和必需参数。参数描述要清晰准确,帮助大模型理解函数的用途。

**调用函数**: 当大模型决定调用函数时,会返回 `tool_calls` 对象,包含函数名和参数。系统解析这些信息,传递给任务执行引擎。

**处理结果**: 执行完函数后,将结果返回给大模型。大模型基于执行结果生成自然语言回复。如果需要继续调用其他函数,这个过程会循环进行。

### 对话管理

对话管理通过维护消息列表实现。每条消息包含角色(system/user/assistant/tool)和内容。系统消息定义助手的行为,用户消息是用户输入,助手消息是大模型回复,工具消息是函数执行结果。

为了控制上下文长度,系统会定期清理历史消息,保留系统消息和最近的对话。这样既能保持对话连贯性,又能避免 token 消耗过大。

### 错误处理策略

每个模块都实现了完善的错误处理。所有可能抛出异常的操作都包裹在 try-except 块中,捕获异常后返回友好的错误信息。错误信息会包含具体的错误原因,帮助用户理解问题。

对于系统级操作,会先检查必要的工具是否存在,如果不存在会给出明确的提示。对于文件操作,会验证路径的合法性,防止安全问题。

## 添加新功能指南

### 步骤一:创建控制器

在 `src/controllers/` 目录下创建新的控制器文件。控制器类应该包含初始化方法和具体的功能方法。每个方法都应该有清晰的文档字符串,说明参数和返回值。

```python
class NewController:
    """新功能控制器"""
    
    def __init__(self):
        """初始化控制器"""
        # 初始化必要的资源
        pass
    
    def execute_action(self, param: str) -> str:
        """
        执行具体操作
        
        Args:
            param: 参数说明
            
        Returns:
            执行结果的描述性文本
        """
        try:
            # 实现具体逻辑
            result = self._do_something(param)
            return f"操作成功: {result}"
        except Exception as e:
            return f"操作失败: {str(e)}"
```

### 步骤二:注册到执行引擎

在 `task_executor.py` 中导入新控制器,在 `__init__` 方法中创建实例,在 `execute` 方法中添加路由逻辑。

```python
from src.controllers.new_controller import NewController

class TaskExecutor:
    def __init__(self):
        self.new_controller = NewController()
    
    def execute(self, function_name: str, arguments: Dict[str, Any]) -> str:
        if function_name == "new_function":
            return self._handle_new_function(arguments)
    
    def _handle_new_function(self, args: Dict[str, Any]) -> str:
        param = args.get("param")
        if not param:
            return "错误: 缺少必需参数"
        return self.new_controller.execute_action(param)
```

### 步骤三:定义 Function Calling

在 `llm_client.py` 的 `get_available_functions()` 方法中添加函数定义。函数描述要清晰准确,参数定义要完整。

```python
{
    "type": "function",
    "function": {
        "name": "new_function",
        "description": "执行新功能的详细描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param": {
                    "type": "string",
                    "description": "参数的详细说明"
                }
            },
            "required": ["param"]
        }
    }
}
```

### 步骤四:添加测试

在 `tests/` 目录下添加测试函数,验证新功能的正确性。测试应该覆盖正常情况和异常情况。

```python
def test_new_controller():
    """测试新控制器"""
    controller = NewController()
    
    # 测试正常情况
    result = controller.execute_action("test")
    assert "成功" in result
    
    # 测试异常情况
    result = controller.execute_action("")
    assert "错误" in result or "失败" in result
```

### 步骤五:更新文档

在 README.md 和用户指南中添加新功能的说明,包括使用方法和示例。

## 测试指南

### 单元测试

每个控制器都应该有对应的单元测试,验证各个方法的功能。测试应该独立运行,不依赖外部资源。

运行测试: `python tests/test_basic.py`

### 集成测试

集成测试验证各个模块协同工作的情况。可以使用 `examples/demo_without_voice.py` 进行集成测试,该脚本模拟完整的交互流程。

### 手动测试

对于语音功能,需要进行手动测试。启动程序后,尝试各种语音命令,验证识别准确性和功能正确性。

## 性能优化

### 对话历史管理

限制对话历史长度可以减少 API 调用的 token 消耗,提高响应速度。当前默认保留最近 10 轮对话,可以根据实际需求调整。

### 缓存机制

对于频繁访问的数据,可以考虑添加缓存。例如,音乐文件列表可以缓存一段时间,避免每次都扫描目录。

### 异步处理

当前版本使用同步执行,对于耗时操作可以考虑改为异步处理,提高并发能力。

## 安全考虑

### 输入验证

所有用户输入都应该进行验证,防止注入攻击。文件路径要转换为绝对路径并检查是否在安全范围内。

### 权限控制

应用控制和系统操作应该有明确的权限限制,只允许执行安全的操作。使用白名单机制而不是黑名单。

### 错误信息

错误信息应该对用户友好,但不应该暴露系统内部细节,避免被利用。

## 调试技巧

### 日志输出

在关键位置添加 print 语句输出调试信息。可以打印函数调用、参数值、执行结果等。

### 异常追踪

使用 `traceback` 模块打印完整的异常堆栈,帮助定位问题。

### 分步调试

对于复杂的问题,可以使用 Python 调试器 pdb 进行分步调试,查看变量值和执行流程。

## 部署建议

### 虚拟环境

建议使用虚拟环境隔离依赖,避免与系统 Python 环境冲突。

### 配置管理

敏感信息如 API Key 应该通过环境变量管理,不要硬编码在代码中。

### 日志记录

在生产环境中应该使用专业的日志库如 logging,记录关键操作和错误信息。

## 常见问题

### 如何切换大模型?

修改 `config.py` 中的 `OPENAI_MODEL` 变量,支持的模型包括 gpt-4.1-mini、gpt-4.1-nano 和 gemini-2.5-flash。

### 如何添加新的应用程序?

在 `config.py` 的 `ALLOWED_APPLICATIONS` 字典中添加应用名称和对应的命令列表。

### 如何修改安全目录?

在 `config.py` 的 `SAFE_DIRECTORIES` 列表中添加或删除目录路径。

### 如何调整语音参数?

修改 `config.py` 中的 `TTS_RATE`(语速)和 `TTS_VOLUME`(音量)变量。

## 贡献代码

在提交代码前,请确保:

1. 代码遵循 PEP 8 规范
2. 添加了必要的注释和文档字符串
3. 通过了所有测试
4. 更新了相关文档

详细的贡献指南请参考 CONTRIBUTING.md 文件。

