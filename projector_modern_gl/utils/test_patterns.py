"""
Test Pattern Generator
Generate various calibration patterns for projector alignment
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np


class TestPatternGenerator:
    """Generate test patterns for projector calibration"""

    def __init__(self, width=1920, height=1080):
        """
        Initialize test pattern generator

        Args:
            width: Pattern width in pixels
            height: Pattern height in pixels
        """
        self.width = width
        self.height = height

    def generate_grid(self, grid_size=120, line_width=2, color=(255, 255, 255), bg_color=(0, 0, 0)):
        """
        Generate grid pattern

        Args:
            grid_size: Grid cell size in pixels
            line_width: Line width in pixels
            color: Line color RGB
            bg_color: Background color RGB

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Vertical lines
        for x in range(0, self.width, grid_size):
            draw.line([(x, 0), (x, self.height)], fill=color, width=line_width)

        # Horizontal lines
        for y in range(0, self.height, grid_size):
            draw.line([(0, y), (self.width, y)], fill=color, width=line_width)

        # Center cross (red)
        draw.line([(self.width//2, 0), (self.width//2, self.height)], fill=(255, 0, 0), width=4)
        draw.line([(0, self.height//2), (self.width, self.height//2)], fill=(255, 0, 0), width=4)

        # Corner markers (green)
        marker_size = 60
        draw.rectangle([0, 0, marker_size, marker_size], fill=(0, 255, 0))
        draw.rectangle([self.width-marker_size, 0, self.width, marker_size], fill=(0, 255, 0))
        draw.rectangle([0, self.height-marker_size, marker_size, self.height], fill=(0, 255, 0))
        draw.rectangle([self.width-marker_size, self.height-marker_size, self.width, self.height], fill=(0, 255, 0))

        return img

    def generate_crosshatch(self, spacing=40, line_width=1, color=(255, 255, 255), bg_color=(0, 0, 0)):
        """
        Generate crosshatch pattern for fine alignment

        Args:
            spacing: Line spacing in pixels
            line_width: Line width
            color: Line color RGB
            bg_color: Background color RGB

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Dense grid
        for x in range(0, self.width, spacing):
            draw.line([(x, 0), (x, self.height)], fill=color, width=line_width)

        for y in range(0, self.height, spacing):
            draw.line([(0, y), (self.width, y)], fill=color, width=line_width)

        # Center target
        center_x = self.width // 2
        center_y = self.height // 2
        for radius in [20, 40, 60, 80, 100]:
            draw.ellipse(
                [center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                outline=(255, 0, 0), width=2
            )

        return img

    def generate_checkerboard(self, square_size=64, color1=(255, 255, 255), color2=(0, 0, 0)):
        """
        Generate checkerboard pattern

        Args:
            square_size: Size of each square
            color1: First color RGB
            color2: Second color RGB

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height), color=color2)
        draw = ImageDraw.Draw(img)

        cols = self.width // square_size + 1
        rows = self.height // square_size + 1

        for row in range(rows):
            for col in range(cols):
                if (row + col) % 2 == 0:
                    x = col * square_size
                    y = row * square_size
                    draw.rectangle(
                        [x, y, x + square_size, y + square_size],
                        fill=color1
                    )

        return img

    def generate_color_bars(self, bar_type='smpte'):
        """
        Generate color bars for color calibration

        Args:
            bar_type: 'smpte' or 'full'

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height))

        if bar_type == 'smpte':
            # SMPTE color bars
            bar_width = self.width // 7
            colors = [
                (192, 192, 192),  # 75% White
                (192, 192, 0),     # Yellow
                (0, 192, 192),     # Cyan
                (0, 192, 0),       # Green
                (192, 0, 192),     # Magenta
                (192, 0, 0),       # Red
                (0, 0, 192)        # Blue
            ]

            # Main bars (top 2/3)
            bar_height = int(self.height * 0.667)
            for i, color in enumerate(colors):
                x = i * bar_width
                img.paste(Image.new('RGB', (bar_width, bar_height), color), (x, 0))

            # Lower section (bottom 1/3)
            lower_y = bar_height
            lower_height = self.height - bar_height

            # Lower colors
            lower_colors = [
                (0, 0, 192),      # Blue
                (0, 0, 0),        # Black
                (192, 0, 192),    # Magenta
                (0, 0, 0),        # Black
                (0, 192, 192),    # Cyan
                (0, 0, 0),        # Black
                (192, 192, 192)   # White
            ]

            for i, color in enumerate(lower_colors):
                x = i * bar_width
                img.paste(Image.new('RGB', (bar_width, lower_height), color), (x, lower_y))

        else:  # Full color bars
            bar_width = self.width // 8
            colors = [
                (255, 255, 255),  # White
                (255, 255, 0),    # Yellow
                (0, 255, 255),    # Cyan
                (0, 255, 0),      # Green
                (255, 0, 255),    # Magenta
                (255, 0, 0),      # Red
                (0, 0, 255),      # Blue
                (0, 0, 0)         # Black
            ]

            for i, color in enumerate(colors):
                x = i * bar_width
                img.paste(Image.new('RGB', (bar_width, self.height), color), (x, 0))

        return img

    def generate_gradient(self, direction='horizontal', start_color=(0, 0, 0), end_color=(255, 255, 255)):
        """
        Generate gradient pattern

        Args:
            direction: 'horizontal', 'vertical', or 'radial'
            start_color: Start color RGB
            end_color: End color RGB

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height))

        if direction == 'horizontal':
            for x in range(self.width):
                t = x / self.width
                color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * t) for i in range(3))
                for y in range(self.height):
                    img.putpixel((x, y), color)

        elif direction == 'vertical':
            for y in range(self.height):
                t = y / self.height
                color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * t) for i in range(3))
                for x in range(self.width):
                    img.putpixel((x, y), color)

        elif direction == 'radial':
            center_x = self.width // 2
            center_y = self.height // 2
            max_radius = np.sqrt(center_x**2 + center_y**2)

            for y in range(self.height):
                for x in range(self.width):
                    dx = x - center_x
                    dy = y - center_y
                    radius = np.sqrt(dx**2 + dy**2)
                    t = min(radius / max_radius, 1.0)
                    color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * t) for i in range(3))
                    img.putpixel((x, y), color)

        return img

    def generate_geometry(self, shapes='circles'):
        """
        Generate geometric test pattern

        Args:
            shapes: 'circles', 'squares', or 'mixed'

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        center_x = self.width // 2
        center_y = self.height // 2

        if shapes == 'circles':
            # Concentric circles
            for i, radius in enumerate(range(50, min(self.width, self.height)//2, 50)):
                color_val = 255 - (i * 30) % 255
                draw.ellipse(
                    [center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                    outline=(color_val, color_val, color_val), width=2
                )

        elif shapes == 'squares':
            # Concentric squares
            for i, size in enumerate(range(50, min(self.width, self.height)//2, 50)):
                color_val = 255 - (i * 30) % 255
                draw.rectangle(
                    [center_x-size, center_y-size, center_x+size, center_y+size],
                    outline=(color_val, color_val, color_val), width=2
                )

        elif shapes == 'mixed':
            # Mixed patterns
            # Corner circles
            radius = 100
            positions = [
                (radius, radius),
                (self.width - radius, radius),
                (radius, self.height - radius),
                (self.width - radius, self.height - radius)
            ]
            for x, y in positions:
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline=(255, 255, 255), width=3)

            # Center target
            for r in range(20, 120, 20):
                draw.ellipse([center_x-r, center_y-r, center_x+r, center_y+r], outline=(255, 0, 0), width=2)

        return img

    def generate_focus_pattern(self):
        """
        Generate focus test pattern with fine details

        Returns:
            PIL Image
        """
        img = Image.new('RGB', (self.width, self.height), color=(128, 128, 128))
        draw = ImageDraw.Draw(img)

        # Fine grid for focus testing
        for x in range(0, self.width, 10):
            draw.line([(x, 0), (x, self.height)], fill=(0, 0, 0), width=1)

        for y in range(0, self.height, 10):
            draw.line([(0, y), (self.width, y)], fill=(0, 0, 0), width=1)

        # Thicker lines every 50 pixels
        for x in range(0, self.width, 50):
            draw.line([(x, 0), (x, self.height)], fill=(255, 255, 255), width=2)

        for y in range(0, self.height, 50):
            draw.line([(0, y), (self.width, y)], fill=(255, 255, 255), width=2)

        # Focus zones in corners with increasing line density
        zone_size = 200
        for density in [1, 2, 3, 4, 5]:
            offset = (density - 1) * 40
            for i in range(0, zone_size, density):
                # Top-left
                draw.line([(offset, offset + i), (offset + zone_size, offset + i)], fill=(255, 255, 255))
                # Top-right
                x_offset = self.width - zone_size - offset
                draw.line([(x_offset, offset + i), (x_offset + zone_size, offset + i)], fill=(255, 255, 255))

        return img

    def generate_all_patterns(self):
        """
        Generate all test patterns

        Returns:
            Dictionary of pattern_name: PIL Image
        """
        patterns = {
            'grid': self.generate_grid(),
            'crosshatch': self.generate_crosshatch(),
            'checkerboard': self.generate_checkerboard(),
            'color_bars_smpte': self.generate_color_bars('smpte'),
            'color_bars_full': self.generate_color_bars('full'),
            'gradient_horizontal': self.generate_gradient('horizontal'),
            'gradient_vertical': self.generate_gradient('vertical'),
            'gradient_radial': self.generate_gradient('radial'),
            'geometry_circles': self.generate_geometry('circles'),
            'geometry_squares': self.generate_geometry('squares'),
            'geometry_mixed': self.generate_geometry('mixed'),
            'focus': self.generate_focus_pattern()
        }

        return patterns
