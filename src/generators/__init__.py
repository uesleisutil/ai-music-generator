"""Music and image generators"""

__all__ = []

try:
    from .generate_music_ai import generate_music_ai
    from .generate_image_ai import generate_image_ai
    __all__.extend(['generate_music_ai', 'generate_image_ai'])
except ImportError:
    # AI models not installed
    pass
