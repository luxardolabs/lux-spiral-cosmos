"""
JIT-compiled mathematical core for cosmic spiral generation
"""

from math import pi, sin, cos, pow
from typing import Tuple
import numpy as np
from numba import jit


@jit(nopython=True, cache=True)
def compute_mathematical_system_16bit(
    n: int,
    r: float,
    t: float,
    initial_x: float,
    initial_u: float,
    initial_v: float,
    width: int,
    height: int,
    scale_factor: float,
    spiral_size_multiplier: float,
    frame_number: int,
    color_speed: int,
    red_base: float,
    red_variation: float,
    green_base: float,
    green_variation: float,
    blue_base: float,
    blue_variation: float,
    hdr_saturation: float,
    max_nits: int,
    hdr_boost: float,
    cosmic_core_boost: float,
) -> Tuple[np.ndarray, int, float, float, float]:
    """JIT-compiled mathematical system computation for 16-bit HDR output"""

    # Initialize 16-bit output array
    img_array = np.zeros((height, width, 3), dtype=np.uint16)
    max_value = 65535

    # Mathematical state
    x, u, v = initial_x, initial_u, initial_v
    pixels_processed = 0

    # Constants
    pi_val = 3.141592653589793

    for i in range(n):
        for j in range(n):
            # Core mathematical system
            u_raw = sin(i + v) + sin(r * i + x)
            v_raw = cos(i + v) + cos(r * i + x)
            x = u_raw + t

            # Apply spiral size multiplier
            u = u_raw * spiral_size_multiplier
            v = v_raw * spiral_size_multiplier

            # Screen coordinates
            px = int(width // 2 + scale_factor * u)
            py = int(height // 2 + scale_factor * v)

            if 0 <= px < width and 0 <= py < height:
                pixels_processed += 1

                # Color calculation
                color_phase = (i + j + frame_number * color_speed) * 0.01

                r_hdr = red_base + red_variation * sin(color_phase)
                g_hdr = green_base + green_variation * sin(color_phase + pi_val / 3)
                b_hdr = blue_base + blue_variation * sin(color_phase + 2 * pi_val / 3)

                # Clamp and apply saturation
                r_hdr = max(0.0, min(1.0, r_hdr * hdr_saturation))
                g_hdr = max(0.0, min(1.0, g_hdr * hdr_saturation))
                b_hdr = max(0.0, min(1.0, b_hdr * hdr_saturation))

                # Simple Rec. 2020 conversion (inlined for JIT)
                r_2020 = min(1.0, r_hdr * 1.2)
                g_2020 = min(1.0, g_hdr * 1.15)
                b_2020 = min(1.0, b_hdr * 1.1)

                # HDR luminance calculation (simplified for JIT)
                base_luminance = abs(sin(i * 0.05 + v)) * abs(cos(j * 0.05 + u))
                core_intensity = abs(u) + abs(v) + abs(x)

                if core_intensity > 2.0:
                    # Blazing bright cores
                    luminance = min(1.0, base_luminance * cosmic_core_boost * hdr_boost)
                else:
                    # Regular space luminance
                    luminance = base_luminance * hdr_boost * 0.3

                # Apply luminance to colors
                r_final = r_2020 * luminance
                g_final = g_2020 * luminance
                b_final = b_2020 * luminance

                # Convert to 16-bit format with simplified PQ curve
                normalized_r = min(1.0, r_final * max_nits / 10000)
                normalized_g = min(1.0, g_final * max_nits / 10000)
                normalized_b = min(1.0, b_final * max_nits / 10000)

                # Simplified PQ approximation
                r_col = int(pow(normalized_r, 0.159) * max_value)
                g_col = int(pow(normalized_g, 0.159) * max_value)
                b_col = int(pow(normalized_b, 0.159) * max_value)

                # Set pixel (BGR for OpenCV)
                img_array[py, px, 0] = b_col
                img_array[py, px, 1] = g_col
                img_array[py, px, 2] = r_col

    return img_array, pixels_processed, x, u, v


@jit(nopython=True, cache=True)
def compute_mathematical_system_8bit(
    n: int,
    r: float,
    t: float,
    initial_x: float,
    initial_u: float,
    initial_v: float,
    width: int,
    height: int,
    scale_factor: float,
    spiral_size_multiplier: float,
    frame_number: int,
    color_speed: int,
    red_base: float,
    red_variation: float,
    green_base: float,
    green_variation: float,
    blue_base: float,
    blue_variation: float,
    hdr_saturation: float,
    hdr_boost: float,
    cosmic_core_boost: float,
) -> Tuple[np.ndarray, int, float, float, float]:
    """JIT-compiled mathematical system computation for 8-bit standard output"""

    # Initialize 8-bit output array
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    max_value = 255

    # Mathematical state
    x, u, v = initial_x, initial_u, initial_v
    pixels_processed = 0

    # Constants
    pi_val = 3.141592653589793

    for i in range(n):
        for j in range(n):
            # Core mathematical system
            u_raw = sin(i + v) + sin(r * i + x)
            v_raw = cos(i + v) + cos(r * i + x)
            x = u_raw + t

            # Apply spiral size multiplier
            u = u_raw * spiral_size_multiplier
            v = v_raw * spiral_size_multiplier

            # Screen coordinates
            px = int(width // 2 + scale_factor * u)
            py = int(height // 2 + scale_factor * v)

            if 0 <= px < width and 0 <= py < height:
                pixels_processed += 1

                # Color calculation
                color_phase = (i + j + frame_number * color_speed) * 0.01

                r_hdr = red_base + red_variation * sin(color_phase)
                g_hdr = green_base + green_variation * sin(color_phase + pi_val / 3)
                b_hdr = blue_base + blue_variation * sin(color_phase + 2 * pi_val / 3)

                # Clamp and apply saturation
                r_hdr = max(0.0, min(1.0, r_hdr * hdr_saturation))
                g_hdr = max(0.0, min(1.0, g_hdr * hdr_saturation))
                b_hdr = max(0.0, min(1.0, b_hdr * hdr_saturation))

                # Simple Rec. 2020 conversion (inlined for JIT)
                r_2020 = min(1.0, r_hdr * 1.2)
                g_2020 = min(1.0, g_hdr * 1.15)
                b_2020 = min(1.0, b_hdr * 1.1)

                # HDR luminance calculation (simplified for JIT)
                base_luminance = abs(sin(i * 0.05 + v)) * abs(cos(j * 0.05 + u))
                core_intensity = abs(u) + abs(v) + abs(x)

                if core_intensity > 2.0:
                    # Blazing bright cores
                    luminance = min(1.0, base_luminance * cosmic_core_boost * hdr_boost)
                else:
                    # Regular space luminance
                    luminance = base_luminance * hdr_boost * 0.3

                # Apply luminance to colors
                r_final = r_2020 * luminance
                g_final = g_2020 * luminance
                b_final = b_2020 * luminance

                # Convert to 8-bit format
                r_col = int(r_final * max_value)
                g_col = int(g_final * max_value)
                b_col = int(b_final * max_value)

                # Set pixel (BGR for OpenCV)
                img_array[py, px, 0] = b_col
                img_array[py, px, 1] = g_col
                img_array[py, px, 2] = r_col

    return img_array, pixels_processed, x, u, v
