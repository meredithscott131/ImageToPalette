import json
from PyQt5.QtWidgets import QFileDialog
from .UIManager import UIManager

class FileManager:
    def __init__(self, parent):
        self.parent = parent
        self.ui_manager = UIManager(self)

    # Opens a file dialog to select an image file
    def open_image_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Open Image File",
            "",
            "Images (*.png *.jpg *.bmp)",
            options=options)
        
        if file_name:
            try:
                self.open_image(file_name)
            except Exception as e:
                self.ui_manager.show_error_popup("Error Opening File", f"An error occurred while opening the file: {e}")
    
    # Opens a new palette from the loaded image
    def open_image(self, file_name):
        self.parent.image_path = file_name
        self.parent.palette_manager.create_color_palette()
        self.parent.image_name_label.setText(f"{self.parent.image_path.split('/')[-1]}")

    # Opens a file dialog to load a palette json file
    def load_palette_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Open Palette File",
            "",
            "JSON Files (*.json)",
            options=options)
        
        if file_name:
            try:
                self.load_palette(file_name)
            except Exception as e:
                self.ui_manager.show_error_popup("Error Loading File", f"An error occurred while loading the file: {e}")

    # Loads a palette from a file and updates the UI
    def load_palette(self, file_name):
        with open(file_name, 'r') as file:
            palette_data = json.load(file)
        
        # Initializes and displays the palette from the data
        self.parent.palette.from_json(palette_data)
        self.parent.palette_manager.display_palette()
        
        # Get and update the origin image name of the palette
        image_name = palette_data.get("image_name", "No image name.")
        self.parent.image_name_label.setText(image_name)
        
        # Update the Recent Palettes ComboBox to include the palette
        self.parent.recent_palettes_manager.update_recent_palettes(file_name)

        # Enable save and regenerate buttons
        self.parent.ui_manager.enable_buttons()

    # Opens a file dialog to save a palette json file
    def save_palette_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save Palette File",
            "",
            "JSON Files (*.json)",
            options=options)
        
        if file_name:
            if not file_name.lower().endswith('.json'):
                file_name += '.json'
            try:
                self.save_palette(file_name)
            except Exception as e:
                self.ui_manager.show_error_popup("Error Saving File", f"An error occurred while saving the file: {e}")

    # Saves the current palette to a json file
    def save_palette(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.parent.palette.to_json(), file)
        
        self.parent.recent_palettes_manager.update_recent_palettes(file_name)