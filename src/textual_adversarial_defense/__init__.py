"""Textual Adversarial Defense - Unicode-based attacks and defenses for text models."""

__version__ = "0.1.0"

try:
    from . import _pipeline
except ImportError:
    _pipeline = None

__all__ = ["_pipeline"]
