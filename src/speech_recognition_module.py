"""
语音识别模块
负责将语音转换为文本
"""

import speech_recognition as sr

import config
from src.logger import logger


class SpeechRecognizer:
    """语音识别器"""

    def __init__(self):
        """初始化识别器"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # 调整环境噪音
        print("正在校准环境噪音...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("校准完成!")

    def listen(self) -> str:
        """
        监听并识别语音

        Returns:
            识别出的文本,如果识别失败返回空字符串
        """
        try:
            print("\n🎤 请说话...")
            with self.microphone as source:
                # 监听音频
                audio = self.recognizer.listen(
                    source, timeout=config.SPEECH_RECOGNITION_TIMEOUT, phrase_time_limit=10
                )

            print("🔄 正在识别...")

            # 使用Google Speech Recognition识别
            text = self.recognizer.recognize_google(
                audio, language=config.SPEECH_RECOGNITION_LANGUAGE
            )

            print(f"✅ 识别结果: {text}")
            return text

        except sr.WaitTimeoutError:
            logger.warning("等待超时,未检测到语音")
            return ""
        except sr.UnknownValueError:
            logger.warning("无法识别语音内容")
            return ""
        except sr.RequestError as e:
            logger.error(f"识别服务出错: {e}")
            return ""
        except Exception as e:
            logger.error(f"发生错误: {e}")
            return ""   def listen_once(self) -> str:
        """
        监听一次语音输入

        Returns:
            识别出的文本
        """
        return self.listen()
