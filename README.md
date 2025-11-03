# PC Voice Assist

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)
![CI](https://github.com/Hygge8/PC-Voice-Assist/workflows/CI/badge.svg)
[![CodeQL](https://github.com/Hygge8/PC-Voice-Assist/workflows/CodeQL%20Analysis/badge.svg)](https://github.com/Hygge8/PC-Voice-Assist/actions/workflows/codeql.yml)

**PC Voice Assist** 是一个基于大语言模型的智能语音控制应用,允许用户通过自然语言语音对话来控制电脑执行各种任务。

## ✨ 特性

- 🎤 **语音交互**: 支持语音输入和语音输出,实现自然对话体验
- 🎵 **音乐控制**: 播放、暂停、停止音乐,支持搜索音乐文件
- ✍️ **智能写作**: 使用AI生成文章并保存到指定位置
- 📁 **文件操作**: 创建、读取、删除文件
- 🚀 **应用控制**: 打开各种应用程序(浏览器、记事本等)
- 🔧 **系统控制**: 音量调节、截图等系统级操作
- 🧠 **智能编排**: 利用大模型的推理能力,自动组合多个基础能力完成复杂任务

## 🎬 演示

```bash
# 简单任务
用户: "播放音乐 ~/Music/song.mp3"
助手: "正在播放: song.mp3"

用户: "帮我写一篇关于人工智能的文章"
助手: "好的,我来为您生成一篇关于人工智能的文章..."

# 复杂任务编排
用户: "帮我写一篇关于环保的短文,保存到桌面,然后打开记事本"
助手: "好的,我会先生成文章,然后保存到桌面,最后打开记事本..."
```

## 🏗️ 架构

```
用户语音输入
    ↓
语音识别 (Speech-to-Text)
    ↓
大模型理解与决策 (LLM + Function Calling)
    ↓
任务执行引擎
    ↓
各类控制器 (音乐、文件、应用、系统等)
    ↓
语音合成 (Text-to-Speech)
    ↓
用户语音输出
```

## 📋 系统要求

- Python 3.11 或更高版本
- 麦克风和扬声器
- OpenAI API Key
- Linux / macOS / Windows

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Hygge8/PC-Voice-Assist.git
cd PC-Voice-Assist
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**Linux 系统额外依赖**:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev espeak

# Fedora
sudo dnf install portaudio-devel python3-devel espeak
```

### 3. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件,设置你的 API Key
export OPENAI_API_KEY="your-api-key-here"
```

### 4. 运行程序

```bash
python main.py
```

### 5. 快速测试

```bash
# 快速测试基本功能
python examples/quick_start.py

# 无语音演示(适用于没有麦克风的环境)
python examples/demo_without_voice.py

# 高级功能演示
python examples/advanced_demo.py

# 运行测试
python tests/test_basic.py
```

## 💡 使用示例

### 基础操作

**音乐控制**:
```
"播放音乐 /home/user/Music/song.mp3"
"暂停音乐"
"继续播放"
"停止播放"
"搜索音乐 轻音乐"
```

**AI 写作**:
```
"帮我写一篇关于人工智能的文章"
"写一篇短文,主题是环保"
"写一篇长文章关于量子计算,保存到桌面"
```

**文件操作**:
```
"创建一个文件,路径是 ~/Desktop/test.txt,内容是 Hello World"
"读取文件 ~/Desktop/test.txt"
"删除文件 ~/Desktop/test.txt"
```

**应用控制**:
```
"打开浏览器"
"打开记事本"
"打开文件管理器"
"打开终端"
```

**系统控制**:
```
"增加音量"
"降低音量"
"把音量设置为50"
"截图"
```

### 复杂场景

**多步骤任务**:
```
"帮我写一篇关于人工智能的文章,保存到桌面,然后播放一首轻音乐"
"搜索音乐目录中的古典音乐,播放第一首,然后把音量设置为30"
"在桌面创建一个笔记文件,内容是今天的待办事项,然后打开记事本"
```

### 控制命令

```
"退出" / "再见" / "结束" - 退出程序
"重置对话" / "清空历史" - 清空对话历史
```

## 📁 项目结构

```
pc-voice-assist/
├── README.md                           # 项目说明
├── LICENSE                             # MIT 许可证
├── CONTRIBUTING.md                     # 贡献指南
├── CHANGELOG.md                        # 更新日志
├── requirements.txt                    # 依赖列表
├── config.py                           # 配置文件
├── main.py                             # 主程序入口
├── .env.example                        # 环境变量示例
├── .gitignore                          # Git 忽略文件
├── .github/                            # GitHub 配置
│   ├── ISSUE_TEMPLATE/                 # Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md        # PR 模板
├── docs/                               # 文档
│   ├── architecture.md                 # 架构文档
│   ├── user_guide.md                   # 用户指南
│   └── development.md                  # 开发文档
├── src/                                # 源代码
│   ├── __init__.py
│   ├── speech_recognition_module.py    # 语音识别
│   ├── text_to_speech.py               # 语音合成
│   ├── llm_client.py                   # 大模型客户端
│   ├── task_executor.py                # 任务执行引擎
│   └── controllers/                    # 控制器模块
│       ├── __init__.py
│       ├── music_controller.py         # 音乐控制
│       ├── writing_controller.py       # 写作控制
│       ├── file_controller.py          # 文件操作
│       ├── app_controller.py           # 应用控制
│       └── system_controller.py        # 系统控制
├── tests/                              # 测试
│   └── test_basic.py                   # 基础测试
└── examples/                           # 示例
    ├── quick_start.py                  # 快速开始
    ├── demo_without_voice.py           # 无语音演示
    └── advanced_demo.py                # 高级功能演示
```

## ⚙️ 配置说明

在 `config.py` 中可以配置:

- **大模型设置**: 选择使用的模型 (gpt-4.1-mini, gemini-2.5-flash等)
- **语音识别**: 语言、超时时间等
- **语音合成**: 语速、音量等
- **安全设置**: 允许的应用程序、安全目录等
- **默认路径**: 音乐目录、文档目录等

## 🔒 安全性

- **路径验证**: 文件操作仅限于配置的安全目录
- **应用白名单**: 只能打开预定义的应用程序
- **权限控制**: 限制可执行的系统操作范围

## 🛠️ 技术栈

- **Python 3.11+**: 主要开发语言
- **OpenAI API**: 大语言模型服务
- **SpeechRecognition**: 语音识别
- **pyttsx3**: 离线语音合成
- **pygame**: 音乐播放
- **psutil**: 系统进程管理

## 📖 文档

- [用户指南](docs/user_guide.md) - 详细的使用说明
- [开发文档](docs/development.md) - 开发和扩展指南
- [架构文档](docs/architecture.md) - 系统架构设计
- [CI/CD 文档](docs/ci-cd.md) - 持续集成和部署说明
- [贡献指南](CONTRIBUTING.md) - 如何参与贡献
- [更新日志](CHANGELOG.md) - 版本更新记录

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

在贡献之前,请阅读 [贡献指南](CONTRIBUTING.md)。

## 📝 开发计划

- [ ] 支持更多的系统操作
- [ ] 添加语音唤醒功能
- [ ] 支持自定义插件
- [ ] 添加 Web 管理界面
- [ ] 支持多语言
- [ ] 添加更多的 AI 能力
- [ ] 支持云端同步

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 👥 作者

**Hygge8** - [GitHub](https://github.com/Hygge8)

## 🙏 致谢

感谢 OpenAI 提供的强大的大语言模型服务。

## 📮 联系方式

- GitHub Issues: [提交问题](https://github.com/Hygge8/PC-Voice-Assist/issues)
- GitHub Discussions: [参与讨论](https://github.com/Hygge8/PC-Voice-Assist/discussions)

---

如果这个项目对你有帮助,请给个 ⭐️ Star 支持一下!

