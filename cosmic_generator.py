"""
Main cosmic spiral animation generator
"""

import os
import sys
import time
import logging
from datetime import datetime
from math import pi, sin
from typing import Dict, Any
import cv2

from jit_core import compute_mathematical_system_16bit, compute_mathematical_system_8bit
from config_manager import ConfigManager


class CosmicSpiralGenerator:
    """Main generator class for cosmic spiral animations"""

    def __init__(self, config_file: str = "config_presets.json"):
        """Initialize the generator"""
        self.config_manager = ConfigManager(config_file)
        self.current_preset: Dict[str, Any] = {}
        self.current_preset_name: str = ""
        self.output_dir: str = ""
        self.timestamp: str = ""
        self._preset_loaded = False

        # Mathematical state (persistent across frames)
        self.x = 0.0
        self.u = 0.0
        self.v = 0.0

        # Setup logging
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Setup clean console logging"""
        logging.basicConfig(
            level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def set_debug_mode(self, enabled: bool = True) -> None:
        """Enable or disable debug logging"""
        level = logging.DEBUG if enabled else logging.INFO
        self.logger.setLevel(level)
        if enabled:
            self.logger.info(
                "Debug logging enabled - detailed performance metrics will be shown\n"
            )

    def load_preset(self, preset_name: str) -> None:
        """Load a specific preset configuration"""
        self.current_preset = self.config_manager.get_preset(preset_name)
        self.current_preset_name = preset_name
        self._preset_loaded = True

        # Validate the preset
        if not self.config_manager.validate_preset(self.current_preset):
            raise ValueError(f"Invalid preset configuration: {preset_name}")

        self.logger.info(f"Loaded preset: {preset_name}")
        self.logger.info(f"Description: {self.current_preset['description']}")

    def _setup_output_directory(self) -> None:
        """Create timestamped output directory with preset name"""
        output_config = self.config_manager.get_output_config()

        if output_config["create_timestamped_folder"]:
            self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = f"frames_{self.current_preset_name}_{self.timestamp}"
        else:
            self.output_dir = f"frames_{self.current_preset_name}"
            self.timestamp = f"{self.current_preset_name}_output"

        os.makedirs(self.output_dir, exist_ok=True)

    def _calculate_spiral_size_multiplier(self, t: float) -> float:
        """Calculate spiral size multiplier with pulsing effect"""
        if not self._preset_loaded:
            raise RuntimeError("No preset loaded")
        pulse_config = self.current_preset["spiral_pulse"]

        size_base = (pulse_config["size_max"] + pulse_config["size_min"]) / 2.0
        size_variation = (pulse_config["size_max"] - pulse_config["size_min"]) / 2.0

        return size_base + size_variation * sin(
            t * pulse_config["pulse_speed"] * 2 * pi
        )

    def render_frame(self, frame_number: int) -> None:
        """Render a single frame using JIT-compiled math"""
        if not self._preset_loaded:
            raise RuntimeError("No preset loaded")

        frame_start_time = time.time()

        video_config = self.current_preset["video"]
        math_config = self.current_preset["mathematical"]
        color_config = self.current_preset["colors"]
        hdr_config = self.current_preset["hdr"]

        # Setup frame
        width, height = video_config["width"], video_config["height"]
        use_16bit = self.config_manager.get_output_config()["use_tiff_16bit"]

        # Time progression
        t = frame_number * math_config["time_speed"]
        spiral_size_multiplier = self._calculate_spiral_size_multiplier(t)

        # JIT-compiled mathematical computation
        math_start = time.time()
        n = math_config["n"]
        r = 2 * pi / math_config["r_denominator"]
        scale_factor = math_config["scale_factor"]

        # Call the appropriate JIT-compiled function
        if use_16bit:
            img_array, pixels_processed, new_x, new_u, new_v = (
                compute_mathematical_system_16bit(
                    n,
                    r,
                    t,
                    self.x,
                    self.u,
                    self.v,
                    width,
                    height,
                    scale_factor,
                    spiral_size_multiplier,
                    frame_number,
                    color_config["speed"],
                    color_config["red_base"],
                    color_config["red_variation"],
                    color_config["green_base"],
                    color_config["green_variation"],
                    color_config["blue_base"],
                    color_config["blue_variation"],
                    color_config["saturation"],
                    hdr_config["max_nits"],
                    hdr_config["hdr_boost"],
                    hdr_config["cosmic_core_boost"],
                )
            )
        else:
            img_array, pixels_processed, new_x, new_u, new_v = (
                compute_mathematical_system_8bit(
                    n,
                    r,
                    t,
                    self.x,
                    self.u,
                    self.v,
                    width,
                    height,
                    scale_factor,
                    spiral_size_multiplier,
                    frame_number,
                    color_config["speed"],
                    color_config["red_base"],
                    color_config["red_variation"],
                    color_config["green_base"],
                    color_config["green_variation"],
                    color_config["blue_base"],
                    color_config["blue_variation"],
                    color_config["saturation"],
                    hdr_config["hdr_boost"],
                    hdr_config["cosmic_core_boost"],
                )
            )

        # Update mathematical state
        self.x, self.u, self.v = new_x, new_u, new_v
        math_time = time.time() - math_start

        # Save frame
        extension = "tiff" if use_16bit else "png"
        filename = f"{self.output_dir}/frame_{frame_number:04d}.{extension}"
        cv2.imwrite(filename, img_array)

        # Calculate totals
        total_iterations = n * n
        frame_total_time = time.time() - frame_start_time

        # INFO: Simple progress update
        self.logger.info(
            f"Frame {frame_number+1:3d}/{video_config['num_frames']}: {frame_total_time:.2f}s"
        )

        # DEBUG: Detailed performance metrics
        if self.logger.isEnabledFor(logging.DEBUG):
            setup_time = math_start - frame_start_time
            save_time = frame_total_time - math_time - setup_time

            self.logger.debug(f"=== FRAME {frame_number+1} DEBUG METRICS ===")
            self.logger.debug(f"Total time: {frame_total_time:.3f}s")
            self.logger.debug(
                f"Setup time: {setup_time:.3f}s ({(setup_time/frame_total_time)*100:.1f}%)"
            )
            self.logger.debug(
                f"Math time (JIT): {math_time:.3f}s ({(math_time/frame_total_time)*100:.1f}%)"
            )
            self.logger.debug(
                f"Save time: {save_time:.3f}s ({(save_time/frame_total_time)*100:.1f}%)"
            )
            self.logger.debug(f"Total iterations: {total_iterations:,}")
            self.logger.debug(f"Pixels processed: {pixels_processed:,}")
            self.logger.debug(
                f"Iterations per second: {total_iterations/math_time:,.0f}"
            )
            self.logger.debug(
                f"Time per iteration: {(math_time/total_iterations)*1000000:.2f} microseconds"
            )
            self.logger.debug("-" * 50)

    def generate_animation(self, preset_name: str) -> None:
        """Generate complete animation using specified preset"""
        self.load_preset(preset_name)
        self._setup_output_directory()

        video_config = self.current_preset["video"]
        num_frames = video_config["num_frames"]

        self.logger.info(
            f"Generating {num_frames} HDR frames at {video_config['width']}x{video_config['height']}..."
        )
        self.logger.info(
            f"HDR Settings: {self.current_preset['hdr']['max_nits']} nits peak, Rec. 2020 wide gamut"
        )
        self.logger.info(f"Output directory: {self.output_dir}")
        self.logger.info("")

        # Reset mathematical state
        self.x = self.u = self.v = 0.0

        # Render all frames
        start_time = time.time()
        for frame in range(num_frames):
            self.render_frame(frame)

        total_time = time.time() - start_time
        self.logger.info("")
        self.logger.info(f"Animation complete! Total time: {total_time/60:.1f} minutes")
        self.logger.info(f"Average: {total_time/num_frames:.2f}s per frame")
        self.logger.info("")

        self._print_completion_info()

    def _print_completion_info(self) -> None:
        """Print completion information and ffmpeg command"""
        if not self._preset_loaded:
            raise RuntimeError("No preset loaded")

        self.logger.info(f"Frames saved to: {self.output_dir}/")
        self.logger.info("")
        self.logger.info("To encode as HDR video, run this ffmpeg command:")
        self.logger.info("")

        ffmpeg_cmd = self.config_manager.get_ffmpeg_command(
            self.current_preset_name, self.output_dir, self.timestamp
        )
        self.logger.info(ffmpeg_cmd)

        self.logger.info("")
        self.logger.info(
            f"HDR Settings used: {self.current_preset['hdr']['max_nits']} nits peak brightness, Rec. 2020 color gamut"
        )


def main():
    """Main entry point"""
    generator = CosmicSpiralGenerator()

    if len(sys.argv) < 2:
        generator.config_manager.list_presets()
        generator.logger.info("")
        generator.logger.info("Usage: python cosmic_generator.py <preset_name>")
        generator.logger.info("       python cosmic_generator.py <preset_name> --debug")
        generator.logger.info("Default: python cosmic_generator.py original_settings")
        return

    preset_name = sys.argv[1]

    # Enable debug logging if requested
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        generator.set_debug_mode(True)

    try:
        generator.generate_animation(preset_name)
    except (FileNotFoundError, ValueError) as e:
        generator.logger.error(f"Error: {e}")
        generator.config_manager.list_presets()


if __name__ == "__main__":
    main()
