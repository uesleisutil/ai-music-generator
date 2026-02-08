"""Music and image generators"""

__all__ = []

try:
    from .generate_music_ai import generate_music_ai  # noqa: F401
    from .generate_image_ai import generate_image_ai  # noqa: F401

    __all__.extend(["generate_music_ai", "generate_image_ai"])
except ImportError:
    # AI models not installed
    pass
