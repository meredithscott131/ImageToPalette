import json
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FileManager:
    def __init__(self, parent):
        self.parent = parent

    # Displays an error popup with the given title and message
    def show_error_popup(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    # Opens a file dialog to select an image file
    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Open Image File",
            "",
            "Images (*.png *.jpg *.bmp)",
            options=options)
        
        if file_name:
            try:
                self.open_file(file_name.lower())
            except Exception as e:
                self.show_error_popup("Error Opening File", f"An error occurred while opening the file: {e}")
    
    # Opens a new palette from the loaded image
    def open_file(self, file_name):
        self.parent.image_path = file_name
        self.parent.palette_manager.create_color_palette()
        self.parent.image_name_label.setText(f"{self.parent.image_path.split('/')[-1]}")

    # Loads a file dialog to load a palette json file
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
                self.load_palette(file_name.lower())
            except Exception as e:
                self.show_error_popup("Error Loading File", f"An error occurred while loading the file: {e}")

    # Loads a palette from a file and updates the UI
    def load_palette(self, file_name):
        with open(file_name, 'r') as file:
            palette_data = json.load(file)
        
        # Updates and displays the palette from the data
        self.parent.palette.from_dict(palette_data)
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
                self.save_palette(file_name.lower())
            except Exception as e:
                self.show_error_popup("Error Saving File", f"An error occurred while saving the file: {e}")

    # Saves the current palette to a json file
    def save_palette(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.parent.palette.to_dict(), file)
        
        self.parent.recent_palettes_manager.update_recent_palettes(file_name)