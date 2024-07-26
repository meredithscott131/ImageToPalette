import json
from collections import Counter
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
import random

# Represents a set of dominant colors in an image
class Palette:
    def __init__(self):
        self.image_name = None  # Name of the original image source
        self.cur_colors = []  # List of the current displayed colors
        self.total_colors = []  # List of the total colors found in the image
    
    # Adds the given color to the current list of colors
    def add_color(self, color):
        self.cur_colors.append(color)

    # Clears the current list of colors
    def clear_colors(self):
        self.cur_colors = []
    
    # Collects and stores all of the most common colors in the given image
    def collectColors(self, image_path):
        self.image_name = image_path.split('/')[-1]
        image = QImage(image_path)
        image = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        color_counter = Counter()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y).rgb()
                color_counter[color] += 1

        most_common_colors = color_counter.most_common()
        random.shuffle(most_common_colors)

        self.total_colors = most_common_colors
    
    # Shuffles the current set of most common colors and sets the current set of displayed colors
    def generatePalette(self):
        random.shuffle(self.total_colors)
        num_colors = 15
        step = len(self.total_colors) // num_colors
        palette_colors = [self.total_colors[i * step][0] for i in range(num_colors)]

        self.clear_colors()

        for color in palette_colors:
            self.add_color(f'#{color:06x}')
    
    # Initializes the palette from a dictionary
    def from_dict(self, data):
        self.image_name = data.get("image_name", "")
        self.cur_colors = data.get("current_colors", [])
        self.total_colors = [(color, count) for color, count in data.get("total colors", [])]
    
    # Converts the palette to a dictionary
    def to_dict(self):
        return {
            "current_colors": self.cur_colors,
            "total_colors": [(color, count) for color, count in self.total_colors],
            "image_name": self.image_name
        }

    # Launches dialog to select the location of the palette json file
    # Returns the created file path for the palette
    def save_palette(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Palette", "",
                                                   "JSON Files (*.json);;All Files (*)", options=options)
        
        # Transfers palette information to json file format
        if file_name:
            with open(file_name, 'w') as file:
                json.dump({
                    "current_colors": self.cur_colors,
                    "total_colors": [(color, count) for color, count in self.total_colors],
                    "image_name": self.image_name  # Save the image name
                }, file)
            return file_name
        
        return None

    # Launches dialog to select the palette file to load into the docker
    def load_palette(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Palette", "",
                                                   "JSON Files (*.json);;All Files (*)", options=options)
        
        # Transfers palette information from json file format
        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)
                self.cur_colors = data["current_colors"]
                self.total_colors = [(color, count) for color, count in data.get("total colors", [])]
                self.image_name = data.get("image_name")
            return file_name
        return None