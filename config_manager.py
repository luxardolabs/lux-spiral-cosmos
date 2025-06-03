"""
Configuration management for cosmic spiral generator
"""

import json
import os
import logging
from typing import Dict, Any


class ConfigManager:
    """Manages preset configurations and validation"""

    def __init__(self, config_file: str = "config_presets.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")

        with open(self.config_file, "r") as f:
            return json.load(f)

    def get_preset_names(self) -> list[str]:
        """Get list of available preset names"""
        return list(self.config["presets"].keys())

    def get_preset(self, preset_name: str) -> Dict[str, Any]:
        """Get a specific preset configuration"""
        if preset_name not in self.config["presets"]:
            raise ValueError(f"Preset '{preset_name}' not found")
        return self.config["presets"][preset_name]

    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.config["output"]

    def list_presets(self) -> None:
        """Display available presets"""
        self.logger.info("Available presets:")
        self.logger.info("-" * 50)
        for name, preset in self.config["presets"].items():
            self.logger.info(f"{name:20} - {preset['description']}")

    def validate_preset(self, preset: Dict[str, Any]) -> bool:
        """Validate preset configuration structure"""
        required_sections = ["video", "hdr", "mathematical", "spiral_pulse", "colors"]

        for section in required_sections:
            if section not in preset:
                self.logger.error(f"Missing required section: {section}")
                return False

        # Validate video section
        video_required = ["width", "height", "num_frames", "fps"]
        for key in video_required:
            if key not in preset["video"]:
                self.logger.error(f"Missing video parameter: {key}")
                return False

        # Validate mathematical section
        math_required = ["n", "r_denominator", "time_speed", "scale_factor"]
        for key in math_required:
            if key not in preset["mathematical"]:
                self.logger.error(f"Missing mathematical parameter: {key}")
                return False

        return True

    def get_ffmpeg_command(
        self, preset_name: str, output_dir: str, timestamp: str
    ) -> str:
        """Generate FFmpeg command for HDR video encoding"""
        preset = self.get_preset(preset_name)
        use_16bit = self.get_output_config()["use_tiff_16bit"]
        extension = "tiff" if use_16bit else "png"
        fps = preset["video"]["fps"]

        command_parts = [
            f"ffmpeg -r {fps} -i {output_dir}/frame_%04d.{extension}",
            "-c:v libx265",
            "-pix_fmt yuv420p10le",
            "-color_primaries bt2020",
            "-color_trc smpte2084",
            "-colorspace bt2020nc",
            "-x265-params 'hdr-opt=1:repeat-headers=1:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc'",
            f"hdr_animation_{preset_name}_{timestamp}.mp4",
        ]

        return " \\\n  ".join(command_parts)
