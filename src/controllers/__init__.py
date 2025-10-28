"""
控制器模块
"""

from .music_controller import MusicController
from .writing_controller import WritingController
from .file_controller import FileController
from .app_controller import AppController
from .system_controller import SystemController

__all__ = [
    'MusicController',
    'WritingController',
    'FileController',
    'AppController',
    'SystemController'
]

