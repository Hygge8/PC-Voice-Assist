# 贡献指南

感谢您对 PC Voice Assist 项目的关注!我们欢迎任何形式的贡献,包括但不限于提交 Bug 报告、功能建议、代码改进和文档完善。

## 如何贡献

### 报告 Bug

如果您发现了 Bug,请通过 GitHub Issues 提交问题报告。在提交之前,请确保:

1. 搜索现有的 Issues,避免重复提交
2. 使用清晰的标题描述问题
3. 提供详细的复现步骤
4. 包含您的运行环境信息(操作系统、Python 版本等)
5. 如果可能,提供错误日志或截图

### 提出功能建议

我们欢迎新功能的建议!请通过 GitHub Issues 提交,并说明:

1. 功能的使用场景和价值
2. 期望的行为和效果
3. 可能的实现方案(如果有想法)

### 提交代码

#### 准备工作

1. Fork 本仓库到您的 GitHub 账号
2. 克隆您 Fork 的仓库到本地
3. 创建新的功能分支: `git checkout -b feature/your-feature-name`
4. 安装开发依赖: `pip install -r requirements.txt`

#### 开发规范

**代码风格**

- 遵循 PEP 8 Python 代码规范
- 使用有意义的变量名和函数名
- 保持函数简洁,单一职责
- 添加必要的注释和文档字符串

**文档字符串格式**

```python
def function_name(param1: str, param2: int) -> bool:
    """
    函数的简短描述
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        
    Returns:
        返回值的描述
        
    Raises:
        Exception: 异常情况的描述
    """
    pass
```

**提交信息规范**

使用清晰的提交信息,遵循以下格式:

```
<type>: <subject>

<body>

<footer>
```

类型(type)包括:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整(不影响功能)
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例:
```
feat: 添加语音唤醒功能

实现了基于关键词检测的语音唤醒功能,用户可以通过说"你好助手"来唤醒应用。

Closes #123
```

#### 测试

在提交代码之前,请确保:

1. 所有现有测试通过: `python tests/test_basic.py`
2. 为新功能添加相应的测试
3. 测试覆盖正常情况和异常情况

#### 提交 Pull Request

1. 推送您的分支到 GitHub: `git push origin feature/your-feature-name`
2. 在 GitHub 上创建 Pull Request
3. 填写 PR 描述,说明改动内容和原因
4. 等待代码审查和反馈
5. 根据反馈进行必要的修改

### 改进文档

文档改进同样重要!您可以:

1. 修正文档中的错误或不清晰的地方
2. 添加使用示例和教程
3. 翻译文档到其他语言
4. 改进代码注释

## 开发环境设置

### 系统要求

- Python 3.11 或更高版本
- 麦克风和扬声器(用于语音功能)
- OpenAI API Key

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/Hygge8/PC-Voice-Assist.git
cd PC-Voice-Assist

# 创建虚拟环境(推荐)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OPENAI_API_KEY="your-api-key"

# 运行测试
python tests/test_basic.py
```

### Linux 系统额外依赖

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev espeak

# Fedora
sudo dnf install portaudio-devel python3-devel espeak
```

## 项目结构

```
pc-voice-assist/
├── src/                    # 源代码
│   ├── controllers/        # 功能控制器
│   ├── llm_client.py       # 大模型客户端
│   ├── task_executor.py    # 任务执行引擎
│   └── ...
├── tests/                  # 测试文件
├── examples/               # 示例代码
├── docs/                   # 文档
└── main.py                 # 主入口
```

## 添加新功能的步骤

### 1. 创建新的控制器

在 `src/controllers/` 目录下创建新的控制器文件:

```python
# src/controllers/new_controller.py
class NewController:
    """新功能控制器"""
    
    def __init__(self):
        """初始化控制器"""
        pass
    
    def do_something(self, param: str) -> str:
        """
        执行某个操作
        
        Args:
            param: 参数描述
            
        Returns:
            执行结果描述
        """
        try:
            # 实现逻辑
            return "操作成功"
        except Exception as e:
            return f"操作失败: {str(e)}"
```

### 2. 在任务执行引擎中注册

在 `src/task_executor.py` 中:

```python
from src.controllers.new_controller import NewController

class TaskExecutor:
    def __init__(self):
        # 添加新控制器
        self.new_controller = NewController()
    
    def execute(self, function_name: str, arguments: Dict[str, Any]) -> str:
        # 添加路由逻辑
        if function_name == "new_function":
            return self._handle_new_function(arguments)
    
    def _handle_new_function(self, args: Dict[str, Any]) -> str:
        """处理新功能"""
        param = args.get("param")
        return self.new_controller.do_something(param)
```

### 3. 在 LLM 客户端中定义函数

在 `src/llm_client.py` 的 `get_available_functions()` 方法中添加:

```python
{
    "type": "function",
    "function": {
        "name": "new_function",
        "description": "新功能的描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param": {
                    "type": "string",
                    "description": "参数描述"
                }
            },
            "required": ["param"]
        }
    }
}
```

### 4. 添加测试

在 `tests/` 目录下添加测试:

```python
def test_new_controller():
    """测试新控制器"""
    controller = NewController()
    result = controller.do_something("test")
    assert "成功" in result
```

## 代码审查标准

我们会从以下方面审查代码:

1. **功能正确性**: 代码是否实现了预期功能
2. **代码质量**: 是否遵循编码规范,代码是否清晰易读
3. **测试覆盖**: 是否有足够的测试覆盖
4. **文档完整性**: 是否有清晰的注释和文档
5. **安全性**: 是否存在安全隐患
6. **性能**: 是否有明显的性能问题
7. **兼容性**: 是否保持向后兼容

## 社区行为准则

我们致力于为所有人提供友好、安全和包容的环境。参与本项目时,请:

1. 尊重他人,保持友善和专业
2. 接受建设性的批评
3. 关注对社区最有利的事情
4. 对其他社区成员表示同理心

不可接受的行为包括:
- 使用性化的语言或图像
- 人身攻击或侮辱性评论
- 骚扰行为
- 发布他人的私人信息

## 获取帮助

如果您在贡献过程中遇到问题,可以:

1. 查看项目文档和 README
2. 搜索现有的 Issues
3. 在 GitHub Issues 中提问
4. 查看示例代码和测试

## 许可证

通过向本项目贡献代码,您同意您的贡献将在 MIT 许可证下发布。

---

再次感谢您的贡献!每一个贡献都让这个项目变得更好。

