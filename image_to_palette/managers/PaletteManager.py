from collections import Counter
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
import random

# Manages the color palette creation and display
class PaletteManager:
    def __init__(self, parent):
        self.parent = parent

    # Displays the current loaded palette
    def display_palette(self):
        self.parent.palette_layout.displayColorsInGrid(self.parent.palette)

    # Collects and stores all of the most common colors in the given image
    def collect_colors(self, image_path):
        palette = self.parent.palette
        palette.image_name = image_path.split('/')[-1]
        image = QImage(image_path)
        image = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        color_counter = Counter()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y).rgb()
                color_counter[color] += 1

        most_common_colors = color_counter.most_common()
        random.shuffle(most_common_colors)

        palette.total_colors = most_common_colors

    # Shuffles the current set of most common colors and sets the current set of displayed colors
    def generate_palette(self):
        palette = self.parent.palette
        random.shuffle(palette.total_colors)
        num_colors = 15
        step = len(palette.total_colors) // num_colors
        palette_colors = [palette.total_colors[i * step][0] for i in range(num_colors)]

        palette.clear_colors()

        for color in palette_colors:
            palette.add_color(f'#{color:06x}')

    # Creates and displays a new color palette from an image
    def create_color_palette(self):
        self.collect_colors(self.parent.image_path)
        self.generate_palette()
        self.display_palette()
        self.parent.button_regenerate.setEnabled(True)
        self.parent.button_save.setEnabled(True)

    # Regenerates the current loaded color palette
    def regenerate_palette(self):
        self.generate_palette()
        self.display_palette()