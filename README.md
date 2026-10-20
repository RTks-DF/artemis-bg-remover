# Artemis Background Remover

Artemis Background Remover is a powerful, standalone GUI application designed for removing backgrounds and precisely editing transparency masks of images and avatars.

## Features
- **AI Background Removal**: Automatically remove image backgrounds using `rembg`.
- **Smart Flood Fill**: Intelligently remove contiguous regions of similar colors with an adjustable tolerance slider.
- **Manual Brush Tools**: Use the erase and restore brushes with adjustable brush sizes to fine-tune masks.
- **High-Performance Infinite Zoom & Pan**: A hardware-accelerated viewport-based rendering engine allows zooming up to 4000% without lag.
- **Dark Mode UI**: A premium, modern dark mode interface built with CustomTkinter.

## Installation

We recommend using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python main.py
```

### Controls
- **Scroll Wheel**: Vertical Pan / Zoom (with Ctrl / Cmd)
- **Shift + Scroll**: Horizontal Pan
- **Right Click / Middle Click / Space + Drag**: Pan Canvas
- **Left Click**: Apply the selected tool (Fill / Erase / Restore)

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3).
See the `LICENSE` file for more details.
