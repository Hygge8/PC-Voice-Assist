"""
语音合成模块
负责将文本转换为语音
"""
import pyttsx3
import config


class TextToSpeech:
    """文本转语音"""
    
    def __init__(self):
        """初始化TTS引擎"""
        self.engine = pyttsx3.init()
        
        # 设置语速
        self.engine.setProperty('rate', config.TTS_RATE)
        
        # 设置音量
        self.engine.setProperty('volume', config.TTS_VOLUME)
        
        # 尝试设置中文语音
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # 寻找中文语音
            if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text: str):
        """
        朗读文本
        
        Args:
            text: 要朗读的文本
        """
        if not text:
            return
        
        print(f"\n🔊 助手: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"❌ 语音合成出错: {e}")
    
    def stop(self):
        """停止朗读"""
        try:
            self.engine.stop()
        except Exception as e:
            print(f"❌ 停止语音出错: {e}")

