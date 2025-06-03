"""
Lux Spiral Cosmos - HDR Mathematical Animation Generator
"""

from .cosmic_generator import CosmicSpiralGenerator
from .config_manager import ConfigManager
from .jit_core import (
    compute_mathematical_system_16bit,
    compute_mathematical_system_8bit,
)

__version__ = "1.0.0"
__author__ = "Luxardo Labs"
__description__ = (
    "Professional HDR cosmic spiral animation generator with JIT optimization"
)

__all__ = [
    "CosmicSpiralGenerator",
    "ConfigManager",
    "compute_mathematical_system_16bit",
    "compute_mathematical_system_8bit",
]
