# PC Voice Assist

**PC Voice Assist** 是一个基于大语言模型的智能语音控制应用,允许用户通过自然语言语音对话来控制电脑执行各种任务。

## ✨ 特性

- 🎤 **语音交互**: 支持语音输入和语音输出,实现自然对话体验
- 🎵 **音乐控制**: 播放、暂停、停止音乐,支持搜索音乐文件
- ✍️ **智能写作**: 使用AI生成文章并保存到指定位置
- 📁 **文件操作**: 创建、读取、删除文件
- 🚀 **应用控制**: 打开各种应用程序(浏览器、记事本等)
- 🔧 **系统控制**: 音量调节、截图等系统级操作
- 🧠 **智能编排**: 利用大模型的推理能力,自动组合多个基础能力完成复杂任务

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

- Python 3.11+
- Linux / macOS / Windows
- 麦克风和扬声器
- OpenAI API Key

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

**注意**: 
- 在Linux上,可能需要安装额外的系统依赖:
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  sudo apt-get install espeak  # 用于语音合成
  ```

### 3. 配置环境变量

创建 `.env` 文件并设置OpenAI API Key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

或者直接在终端中设置:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 4. 运行程序

```bash
python main.py
```

## 💡 使用示例

### 基础操作

**播放音乐**:
- "播放音乐 /home/user/Music/song.mp3"
- "暂停音乐"
- "继续播放"
- "停止播放"

**写文章**:
- "帮我写一篇关于人工智能的文章"
- "写一篇短文,主题是环保"
- "写一篇长文章关于量子计算,保存到桌面"

**文件操作**:
- "创建一个文件,路径是 /home/user/Desktop/test.txt,内容是 Hello World"
- "读取文件 /home/user/Desktop/test.txt"
- "删除文件 /home/user/Desktop/test.txt"

**打开应用**:
- "打开浏览器"
- "打开记事本"
- "打开文件管理器"

**系统控制**:
- "增加音量"
- "降低音量"
- "截图"

### 复杂场景

**组合任务**:
- "帮我写一篇关于人工智能的文章,然后保存到桌面,保存完后播放一首轻音乐"
- "搜索音乐文件中包含'轻音乐'的歌曲,然后播放第一首"

## 📁 项目结构

```
pc-voice-assist/
├── README.md                    # 项目说明
├── requirements.txt             # 依赖列表
├── config.py                    # 配置文件
├── main.py                      # 主入口
├── src/
│   ├── __init__.py
│   ├── speech_recognition_module.py  # 语音识别
│   ├── text_to_speech.py            # 语音合成
│   ├── llm_client.py                 # 大模型客户端
│   ├── task_executor.py              # 任务执行引擎
│   └── controllers/                  # 控制器模块
│       ├── __init__.py
│       ├── music_controller.py       # 音乐控制
│       ├── writing_controller.py     # 写作控制
│       ├── file_controller.py        # 文件操作
│       ├── app_controller.py         # 应用控制
│       └── system_controller.py      # 系统控制
├── tests/                       # 测试文件
└── examples/                    # 示例文件
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

## 📝 开发计划

- [ ] 支持更多的系统操作
- [ ] 添加语音唤醒功能
- [ ] 支持自定义插件
- [ ] 添加Web界面
- [ ] 支持多语言
- [ ] 添加更多的AI能力

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可证

MIT License

## 👥 作者

Hygge8

## 🙏 致谢

感谢 OpenAI 提供的强大的大语言模型服务。

