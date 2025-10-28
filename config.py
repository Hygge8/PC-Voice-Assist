"""
配置文件
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# OpenAI配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4.1-mini"  # 可选: gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash

# 语音识别配置
SPEECH_RECOGNITION_LANGUAGE = "zh-CN"
SPEECH_RECOGNITION_TIMEOUT = 5  # 秒

# 语音合成配置
TTS_RATE = 150  # 语速
TTS_VOLUME = 0.9  # 音量

# 系统控制配置
ALLOWED_APPLICATIONS = {
    "浏览器": ["google-chrome", "firefox", "chromium-browser"],
    "记事本": ["gedit", "nano", "vim"],
    "文件管理器": ["nautilus", "dolphin", "thunar"],
    "终端": ["gnome-terminal", "konsole", "xterm"],
    "音乐播放器": ["rhythmbox", "vlc", "audacious"],
}

# 文件操作配置
SAFE_DIRECTORIES = [
    str(Path.home() / "Desktop"),
    str(Path.home() / "Documents"),
    str(Path.home() / "Downloads"),
    str(Path.home() / "Music"),
]

# 音乐文件配置
MUSIC_EXTENSIONS = [".mp3", ".wav", ".ogg", ".flac", ".m4a"]
DEFAULT_MUSIC_DIR = str(Path.home() / "Music")

# 写作配置
DEFAULT_ARTICLE_DIR = str(Path.home() / "Documents")
ARTICLE_LENGTHS = {
    "short": "300-500字",
    "medium": "800-1200字",
    "long": "2000-3000字"
}

# 对话配置
MAX_CONVERSATION_HISTORY = 10  # 保留的对话轮数
SYSTEM_PROMPT = """你是一个智能PC语音助手,可以帮助用户通过自然语言控制电脑。
你可以执行以下操作:
1. 播放音乐、暂停音乐、停止音乐
2. 写文章并保存到指定位置
3. 打开各种应用程序
4. 进行文件操作(创建、读取、删除)
5. 系统控制(音量调节、截图等)

当用户提出复杂需求时,你可以组合多个功能来完成任务。
请始终以友好、专业的方式与用户交流。"""

