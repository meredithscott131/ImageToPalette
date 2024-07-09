import json
from collections import Counter
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
import random

class Palette:
    def __init__(self):
        self.name = "Default"
        self.colors = []
        self.most_common_colors = []  # Store all most_common_colors

    def add_color(self, color):
        self.colors.append(color)

    def clear_colors(self):
        self.colors = []

    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            json.dump({
                "name": self.name,
                "colors": self.colors,
                "most_common_colors": [(color, count) for color, count in self.most_common_colors]
            }, file)

    def load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            self.name = data["name"]
            self.colors = data["colors"]
            self.most_common_colors = [(color, count) for color, count in data.get("most_common_colors", [])]

    def get_palette_colors(self):
        return self.colors

    def save_palette(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Palette", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            self.save_to_file(file_name)

    def load_palette(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Palette", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            self.load_from_file(file_name)

    def createColorPalette(self, image_path):
        image = QImage(image_path)
        image = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        color_counter = Counter()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y).rgb()
                color_counter[color] += 1

        most_common_colors = color_counter.most_common()
        random.shuffle(most_common_colors)

        self.most_common_colors = most_common_colors  # Store all colors with their counts

        num_colors = 15
        step = len(most_common_colors) // num_colors
        palette_colors = [most_common_colors[i * step][0] for i in range(num_colors)]
        
        self.clear_colors()

        for color in palette_colors:
            self.add_color(f'#{color:06x}')

    def regeneratePalette(self):
        if self.most_common_colors:
            num_colors = 15
            step = len(self.most_common_colors) // num_colors
            palette_colors = [self.most_common_colors[i * step][0] for i in range(num_colors)]

            self.clear_colors()

            for color in palette_colors:
                self.add_color(f'#{color:06x}')