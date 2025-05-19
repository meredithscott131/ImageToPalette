from collections import Counter
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
import random

from ..model.Palette import Palette

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
    def regenerate_palette(self):
        # Generate new palette
        palette = self.parent.palette
        random.shuffle(palette.total_colors)
        num_colors = 10
        step = len(palette.total_colors) // num_colors
        palette_colors = [palette.total_colors[i * step][0] for i in range(num_colors)]

        palette.clear_colors()
        for color in palette_colors:
            palette.add_color(f'#{color:06x}')

        # Create a snapshot of the current palette
        palette_snapshot = Palette()
        palette_snapshot.cur_colors = list(self.parent.palette.cur_colors)
        palette_snapshot.total_colors = list(self.parent.palette.total_colors)
        palette_snapshot.image_name = self.parent.palette.image_name

        # Add to list (up to 5)
        self.parent.palette.palette_list.append(palette_snapshot)
        if len(self.parent.palette.palette_list) > 5:
            self.parent.palette.palette_list.pop(0)

        # Update index to last one
        self.parent.palette.set_index(len(self.parent.palette.palette_list) - 1)

        self.display_palette()
        self.update_nav_buttons()
        #self.update_index_label()

    def show_previous_palette(self):
        index = self.parent.palette.get_index()
        length = len(self.parent.palette.palette_list)

        if length == 0:
            return

        # Wrap to last if at first
        if index <= 0:
            new_index = length - 1
        else:
            new_index = index - 1

        self.parent.palette.set_index(new_index)
        self.display_palette()
        self.update_nav_buttons()
        #self.update_index_label()


    def show_next_palette(self):
        index = self.parent.palette.get_index()
        length = len(self.parent.palette.palette_list)

        if length == 0:
            return

        # Wrap to first if at last
        if index >= length - 1:
            new_index = 0
        else:
            new_index = index + 1

        self.parent.palette.set_index(new_index)
        self.display_palette()
        self.update_nav_buttons()
        #self.update_index_label()

    # Creates and displays a new color palette from an image
    def create_palette_from_image(self):
        # Reset history
        self.parent.palette.palette_list.clear()
        self.parent.palette.set_index(-1)

        self.collect_colors(self.parent.image_path)
        self.generate_palette()
        self.display_palette()

        # Add the generated palette as the first snapshot
        palette_snapshot = Palette()
        palette_snapshot.cur_colors = list(self.parent.palette.cur_colors)
        palette_snapshot.total_colors = list(self.parent.palette.total_colors)
        palette_snapshot.image_name = self.parent.palette.image_name

        self.parent.palette.palette_list.append(palette_snapshot)
        self.parent.palette.set_index(0)  # Default to first (visible as "1/1")

        self.update_nav_buttons()
        #self.update_index_label()
        self.parent.button_regenerate.setEnabled(True)
        self.parent.button_save.setEnabled(True)

    
    def update_nav_buttons(self):
        length = len(self.parent.palette.palette_list)
        # With wrap-around, only disable if < 2 palettes
        self.parent.button_previous.setEnabled(length > 1)
        self.parent.button_next.setEnabled(length > 1)

    """
    def update_index_label(self):
        index = self.parent.palette.get_index()
        length = len(self.parent.palette.palette_list)
        if length > 0 and 0 <= index < length:
            self.parent.palette_index_label.setText(f"{index + 1}/{length}")
        else:
            self.parent.palette_index_label.setText("0/0")
    """

    def generate_palette(self):
        palette = self.parent.palette
        random.shuffle(palette.total_colors)
        num_colors = 10
        step = max(1, len(palette.total_colors) // num_colors)
        palette_colors = [palette.total_colors[i * step][0] for i in range(num_colors)]

        palette.clear_colors()
        for color in palette_colors:
            palette.add_color(f'#{color:06x}')