# Lux Spiral Cosmos

**Professional HDR Mathematical Animation Generator**

Generate stunning 4K HDR cosmic visualizations using mathematical spiral dynamics with JIT-optimized performance.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/numpy-latest-orange.svg)](https://numpy.org/)
[![Numba JIT](https://img.shields.io/badge/numba-jit%20optimized-green.svg)](https://numba.pydata.org/)
[![HDR](https://img.shields.io/badge/HDR-Rec.2020-purple.svg)](https://en.wikipedia.org/wiki/Rec._2020)

---

## 🎬 Demo

**Sample Animation (HDR):**

[![HDR Animation Demo](https://labs.lux4rd0.com/wp-content/uploads/2025/06/frame_original_settings.jpg)](https://labs.lux4rd0.com/wp-content/uploads/2025/06/hdr_animation_original_settings_20250602_191023.mp4)

*Click image to view HDR animation (works best on HDR-capable displays)*

---

## 🌌 Overview

Lux Spiral Cosmos transforms mathematical equations into mesmerizing cosmic animations through:

- **Mathematical Beauty**: Coupled sine/cosine dynamical systems create organic spiral patterns
- **HDR Excellence**: True 16-bit Rec. 2020 color gamut with PQ tone mapping for 4000+ nit displays
- **JIT Performance**: Numba-optimized computation achieving 6M+ iterations/second (22x speedup)
- **Professional Output**: 4K resolution with FFmpeg-ready HDR video encoding


## ✨ Features

### 🎯 Core Capabilities
- **4K HDR Rendering**: Native 3840×2160 with 16-bit TIFF output
- **Mathematical Continuity**: Frame-to-frame state persistence for smooth evolution
- **Dynamic Spiral Sizing**: Configurable pulsing effects and size modulation
- **Preset System**: JSON-based configurations for instant style switching
- **Performance Monitoring**: Detailed timing analysis and optimization metrics

### 🚀 Performance
- **22x Speed Improvement**: JIT compilation reduces render time from 15s to 0.7s per frame
- **Memory Efficient**: ~100MB RAM usage during processing
- **Scalable**: From 1080p quick previews to 4K production renders

### 🎨 Visual Quality
- **HDR Brilliance**: 1000-4000 nits peak brightness for blazing cosmic cores
- **Wide Color Gamut**: Rec. 2020 color space for impossible-on-sRGB colors
- **Deep Space Blacks**: True 0.01 nit darkness for dramatic contrast
- **Smooth Animation**: Deterministic mathematical evolution between frames

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/luxardolabs/lux-spiral-cosmos.git
cd lux-spiral-cosmos
pip install -r requirements.txt
```

### Generate Your First Animation

```bash
# Use the default preset (matches original settings)
python cosmic_generator.py original_settings

# Try different presets
python cosmic_generator.py cosmic_intense
python cosmic_generator.py giant_spirals

# Enable debug mode for performance analysis
python cosmic_generator.py original_settings --debug
```

### Create HDR Video

```bash
# The generator provides the exact FFmpeg command needed:
ffmpeg -r 24 -i frames_original_settings_20250602_183755/frame_%04d.tiff \
  -c:v libx265 -pix_fmt yuv420p10le \
  -color_primaries bt2020 -color_trc smpte2084 -colorspace bt2020nc \
  -x265-params 'hdr-opt=1:repeat-headers=1:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc' \
  hdr_animation_original_settings_20250602_183755.mp4
```

---

## 🎛️ Available Presets

| Preset | Description | Characteristics |
|--------|-------------|-----------------|
| **`original_settings`** | Exact replica of development settings - **DEFAULT** | Balanced 4K HDR with subtle spiral pulsing |
| **`cosmic_gentle`** | Soft, meditative spirals | Gentle pulsing, lower brightness, peaceful |
| **`cosmic_intense`** | Dramatic HDR experience | 4000 nits peak, rapid pulses, vivid colors |
| **`tiny_details`** | High-resolution intricate patterns | 3000 density, fine spiral structures |
| **`giant_spirals`** | Massive spiral structures | Huge patterns, slow evolution, dramatic scale |
| **`rainbow_chaos`** | Fast color cycling chaos | Rapid rainbow shifts, chaotic dynamics |

---

## ⚙️ Configuration

### Customize Existing Presets

Edit `config_presets.json` to modify any preset:

```json
{
  "presets": {
    "my_custom_preset": {
      "description": "My custom cosmic animation",
      "video": {
        "width": 3840, "height": 2160,
        "num_frames": 240, "fps": 24
      },
      "hdr": {
        "max_nits": 4000,
        "cosmic_core_boost": 5.0
      },
      "mathematical": {
        "n": 2000,
        "r_denominator": 125,
        "time_speed": 0.01,
        "scale_factor": 700
      },
      "spiral_pulse": {
        "size_min": 0.98, "size_max": 1.02,
        "pulse_speed": 2.0
      },
      "colors": {
        "speed": 2, "saturation": 1.5,
        "red_base": 0.3, "red_variation": 0.7,
        "green_base": 0.2, "green_variation": 0.8,
        "blue_base": 0.5, "blue_variation": 0.8
      }
    }
  }
}
```

### Key Parameters

#### Mathematical Controls
- **`n`**: Point density (1000=balanced, 2000=detailed, 3000=ultra-fine)
- **`r_denominator`**: Spiral tightness (50=loose, 125=balanced, 300=tight)
- **`time_speed`**: Evolution rate (0.01=slow, 0.05=normal, 0.1=fast)
- **`scale_factor`**: Pattern size (400=small, 700=screen-filling, 1000=oversized)

#### Visual Effects
- **`spiral_pulse`**: Dynamic size modulation (0.5-3.0 range creates dramatic effects)
- **`max_nits`**: HDR peak brightness (1000=standard, 4000=premium displays)
- **`cosmic_core_boost`**: Brightness multiplier for pattern centers (1.0-10.0)

#### Color System
- **`saturation`**: Color intensity (1.0=natural, 2.0=vivid, 3.0=extreme)
- **`speed`**: Color cycling rate (1=slow, 5=fast, 10=strobing)
- **Base/Variation**: Fine-tune individual color channels (0.0-1.0 range)

---

## 🔬 Technical Details

### Mathematical System

The core animation is generated by a coupled dynamical system:

```python
u = sin(i + v) + sin(r * i + x)
v = cos(i + v) + cos(r * i + x)  
x = u + t
```

Where:
- `i, j`: Iteration indices creating the base pattern
- `r`: Controls spiral frequency and tightness
- `t`: Time parameter providing smooth evolution
- State (`x, u, v`) carries forward between frames for continuity

### HDR Pipeline

1. **Mathematical Computation**: JIT-compiled spiral generation
2. **Color Space**: sRGB → Rec. 2020 wide gamut conversion
3. **HDR Mapping**: PQ (Perceptual Quantizer) tone curve application
4. **Output**: 16-bit TIFF with proper HDR metadata

### Performance Optimization

- **Numba JIT**: Machine code compilation for inner loops
- **Type Specialization**: Separate 8-bit/16-bit code paths
- **Memory Efficiency**: Minimal allocations, cache-friendly access
- **Vectorization Ready**: Architecture supports future SIMD optimization

---

## 📊 Performance Benchmarks

| Configuration | Render Time | Iterations/sec | Speedup |
|---------------|-------------|----------------|---------|
| Python (original) | 14.7s/frame | 277K | 1x baseline |
| **Numba JIT** | **0.97s/frame** | **6.1M** | **22x faster** |

### Scaling Performance
- **1080p**: ~0.25s per frame
- **4K**: ~0.97s per frame  
- **n=1000**: ~0.5s per frame
- **n=3000**: ~2.1s per frame

**Total Animation Times:**
- 240 frames @ 4K: **3.9 minutes** (was 59 minutes)
- 120 frames @ 1080p: **30 seconds**

---

## 🖥️ HDR Display Requirements

### For Optimal Viewing
- **HDR10-compatible display** (1000+ nits peak brightness)
- **Wide color gamut support** (DCI-P3 minimum, Rec. 2020 preferred)
- **HDR video player** (VLC, MPV, or native TV apps)
- **Proper HDMI 2.1** or DisplayPort 1.4+ connection

### Tested Displays
- ✅ LG OLED C/G series (4000 nits peak)
- ✅ Samsung QLED (2000+ nits)
- ✅ Apple Pro Display XDR (1600 nits)
- ✅ Most modern HDR TVs

### Fallback Support
- Standard displays show reduced dynamic range
- Still visually appealing but without HDR "wow" factor
- 8-bit PNG output available for standard workflows

---

## 🏗️ Project Structure

```
lux-spiral-cosmos/
├── cosmic_generator.py      # Main generator class and CLI
├── config_manager.py        # Configuration management
├── jit_core.py             # JIT-optimized mathematical core
├── config_presets.json     # Preset configurations
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── __init__.py            # Package initialization
```

### Module Overview

- **`cosmic_generator.py`**: Main orchestration, rendering pipeline, user interface
- **`config_manager.py`**: JSON loading, validation, preset management, FFmpeg commands
- **`jit_core.py`**: Numba-compiled mathematical functions for maximum performance
- **`config_presets.json`**: User-editable preset configurations

---

## 🛠️ Development

### Running in Debug Mode

```bash
python cosmic_generator.py original_settings --debug
```

Provides detailed performance analysis:
```
=== FRAME 1 DEBUG METRICS ===
Total time: 0.973s
Setup time: 0.000s (0.0%)
Math time (JIT): 0.654s (67.2%)
Save time: 0.319s (32.8%)
Total iterations: 4,000,000
Pixels processed: 3,261,955
Iterations per second: 6,106,519
Time per iteration: 0.16 microseconds
```

### Code Quality
- **Type hints** throughout for better IDE support
- **Modular architecture** for easy maintenance
- **Professional logging** with configurable verbosity
- **Error handling** with meaningful messages
- **Performance monitoring** built-in

### Extending the System

The modular design makes it easy to:
- Add new mathematical systems in `jit_core.py`
- Create new presets in `config_presets.json`
- Modify HDR pipeline in `cosmic_generator.py`
- Add new output formats in `config_manager.py`

---

## 🎯 Use Cases

### Creative Applications
- **Digital Art**: High-resolution prints and installations
- **Video Production**: HDR background elements and transitions
- **Music Visualization**: Sync mathematical parameters to audio
- **Meditation Content**: Slow, hypnotic spiral evolution

### Technical Applications  
- **Algorithm Visualization**: Demonstrate dynamical systems
- **Performance Testing**: Benchmark JIT compilation and HDR pipelines
- **Display Calibration**: Test HDR brightness and color accuracy
- **Educational Content**: Mathematical beauty made visible

### Professional Workflows
- **Motion Graphics**: Export for After Effects/DaVinci Resolve
- **Broadcast**: HDR content for modern television
- **Streaming**: Netflix/YouTube HDR-ready content
- **Gaming**: Procedural background generation

---

## 🤝 Contributing

We welcome contributions! Areas of interest:

### Performance
- GPU acceleration with CuPy/CUDA
- Multi-core CPU parallelization
- Memory usage optimization
- Alternative mathematical systems

### Features
- Audio-reactive parameters
- Real-time preview mode
- Additional output formats
- Web-based configuration interface

### Quality
- Unit tests for mathematical accuracy
- Automated performance benchmarking
- Cross-platform compatibility testing
- Documentation improvements

---

## 📄 License

AGPL-3.0 - see LICENSE file for details.

---

## 🏷️ Credits

**Developed by Luxardo Labs**

- **Mathematical Foundation**: Coupled sine/cosine dynamical systems
- **HDR Implementation**: Rec. 2020 + PQ tone mapping standards
- **Performance**: Numba JIT compilation techniques
- **Inspiration**: The infinite beauty of mathematical visualization

---

## 🔗 Links

- **GitHub**: [luxardolabs/lux-spiral-cosmos](https://github.com/luxardolabs/lux-spiral-cosmos)
- **Issues**: [Report bugs or request features](https://github.com/luxardolabs/lux-spiral-cosmos/issues)
- **Discussions**: [Community discussions](https://github.com/luxardolabs/lux-spiral-cosmos/discussions)

---

*"Where mathematics meets cosmos, beauty emerges infinite."* ✨
