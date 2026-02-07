"""Music and image generators"""
from .generate_music_simple import generate_simple_music
from .generate_image_simple import generate_simple_image

__all__ = ['generate_simple_music', 'generate_simple_image']

try:
    from .generate_music_ai import generate_music_ai
    from .generate_image_ai import generate_image_ai
    __all__.extend(['generate_music_ai', 'generate_image_ai'])
except ImportError:
    # AI models not installed
    pass
