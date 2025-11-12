"""
控制器模块
"""

from .app_controller import AppController
from .file_controller import FileController
from .music_controller import MusicController
from .system_controller import SystemController
from .writing_controller import WritingController

__all__ = [
    "MusicController",
    "WritingController",
    "FileController",
    "AppController",
    "SystemController",
]
