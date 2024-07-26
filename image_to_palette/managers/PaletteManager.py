import json
from ..model.Palette import Palette

# Manages the color palette creation and display
class PaletteManager:
    def __init__(self, parent):
        self.parent = parent

    # Creates and displays a color palette
    def create_color_palette(self):
        self.parent.palette.collectColors(self.parent.image_path)
        self.parent.palette.generatePalette()
        self.display_palette()
        self.parent.button_regenerate.setEnabled(True)
        self.parent.button_save.setEnabled(True)

    # Regenerates the current loaded color palette
    def regenerate_palette(self):
        self.parent.palette.generatePalette()
        self.display_palette()

    # Displays the current loaded palette
    def display_palette(self):
        self.parent.palette_layout.displayColorsInGrid(self.parent.palette)