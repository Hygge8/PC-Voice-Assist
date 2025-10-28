"""
音乐控制器
负责音乐播放控制
"""
import os
from pathlib import Path
from typing import Optional
import pygame
import config


class MusicController:
    """音乐控制器"""
    
    def __init__(self):
        """初始化音乐控制器"""
        pygame.mixer.init()
        self.current_music: Optional[str] = None
        self.is_playing = False
        self.is_paused = False
    
    def play(self, file_path: str) -> str:
        """
        播放音乐
        
        Args:
            file_path: 音乐文件路径
            
        Returns:
            执行结果描述
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return f"错误: 文件不存在 - {file_path}"
            
            # 检查文件扩展名
            ext = Path(file_path).suffix.lower()
            if ext not in config.MUSIC_EXTENSIONS:
                return f"错误: 不支持的音乐格式 - {ext}"
            
            # 停止当前播放
            if self.is_playing:
                pygame.mixer.music.stop()
            
            # 加载并播放音乐
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            self.current_music = file_path
            self.is_playing = True
            self.is_paused = False
            
            return f"正在播放: {Path(file_path).name}"
            
        except Exception as e:
            return f"播放音乐时出错: {str(e)}"
    
    def pause(self) -> str:
        """
        暂停音乐
        
        Returns:
            执行结果描述
        """
        try:
            if not self.is_playing:
                return "当前没有正在播放的音乐"
            
            if self.is_paused:
                return "音乐已经处于暂停状态"
            
            pygame.mixer.music.pause()
            self.is_paused = True
            
            return "音乐已暂停"
            
        except Exception as e:
            return f"暂停音乐时出错: {str(e)}"
    
    def resume(self) -> str:
        """
        继续播放音乐
        
        Returns:
            执行结果描述
        """
        try:
            if not self.is_playing:
                return "当前没有音乐可以继续播放"
            
            if not self.is_paused:
                return "音乐正在播放中"
            
            pygame.mixer.music.unpause()
            self.is_paused = False
            
            return "继续播放音乐"
            
        except Exception as e:
            return f"继续播放时出错: {str(e)}"
    
    def stop(self) -> str:
        """
        停止音乐
        
        Returns:
            执行结果描述
        """
        try:
            if not self.is_playing:
                return "当前没有正在播放的音乐"
            
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_music = None
            
            return "音乐已停止"
            
        except Exception as e:
            return f"停止音乐时出错: {str(e)}"
    
    def search_music(self, keyword: str) -> str:
        """
        搜索音乐文件
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            搜索结果描述
        """
        try:
            music_dir = Path(config.DEFAULT_MUSIC_DIR)
            
            if not music_dir.exists():
                return f"音乐目录不存在: {music_dir}"
            
            # 搜索匹配的音乐文件
            matches = []
            for ext in config.MUSIC_EXTENSIONS:
                matches.extend(music_dir.glob(f"**/*{keyword}*{ext}"))
            
            if not matches:
                return f"未找到包含 '{keyword}' 的音乐文件"
            
            # 返回找到的文件列表
            result = f"找到 {len(matches)} 个匹配的音乐文件:\n"
            for i, match in enumerate(matches[:5], 1):  # 最多返回5个
                result += f"{i}. {match.name} ({match})\n"
            
            if len(matches) > 5:
                result += f"... 还有 {len(matches) - 5} 个文件"
            
            return result
            
        except Exception as e:
            return f"搜索音乐时出错: {str(e)}"
    
    def get_status(self) -> str:
        """
        获取播放状态
        
        Returns:
            状态描述
        """
        if not self.is_playing:
            return "当前没有播放音乐"
        
        status = f"当前播放: {Path(self.current_music).name if self.current_music else '未知'}"
        if self.is_paused:
            status += " (已暂停)"
        
        return status

