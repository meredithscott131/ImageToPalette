import json
import os
from PyQt5.QtCore import Qt

# Manages the Recent Palettes ComboBox
class RecentPalettesManager:
    def __init__(self, parent):
        self.parent = parent
        self.recent_palettes = self.load_recent_palettes()

    # Loads the palette selected by the user from the recent palettes list
    def load_selected_recent_palette(self, index):
        if 0 <= index < len(self.recent_palettes):
            palette_path = self.recent_palettes.pop(index)
            
            # Load the palette from the file
            self.parent.file_manager.load_palette(palette_path)
            
            # Update the combo box and save changes
            self.update_recent_palettes_combo()
            self.save_recent_palettes()
        else:
            print(f"Index {index} is out of range for recent palettes.")

    # Updates the list of recent palettes with a new file
    def update_recent_palettes(self, file_name):
        # Remove the file if it is already in the list
        if file_name in self.recent_palettes:
            self.recent_palettes.remove(file_name)
        
        # Add the new file to the top of the list
        self.recent_palettes.insert(0, file_name)

        # Keep the list length to a max of 5
        if len(self.recent_palettes) > 5:
            self.recent_palettes.pop()
        
        # Update the combo box and save changes
        self.update_recent_palettes_combo()
        self.save_recent_palettes()

    # Updates the Recent Palettes ComboBox UI
    def update_recent_palettes_combo(self):
        # Clear existing items
        self.parent.recent_palettes_combo.clear()

        # Get font metrics for text
        font_metrics = self.parent.recent_palettes_combo.fontMetrics()
        
        # Get the current width of the combo box
        combo_width = self.parent.recent_palettes_combo.width()
        
        for palette_path in self.recent_palettes:
            # Check if the palette file exists
            if os.path.exists(palette_path) and os.path.isfile(palette_path):
                file_name = os.path.basename(palette_path)
                elided_text = font_metrics.elidedText(file_name, Qt.ElideRight, combo_width - 20)
                self.parent.recent_palettes_combo.addItem(elided_text)
        
        # Setting the default text of the box
        self.parent.recent_palettes_combo.lineEdit().setText("Recent Palettes")

    # Saves the list of recent palettes to the krita_recent_palettes json file
    def save_recent_palettes(self):
        with open(self.parent.RECENT_PALETTES_FILE, 'w') as file:
            json.dump(self.recent_palettes, file)

    # Loads the list of recent palettes from the krita_recent_palettes json file
    def load_recent_palettes(self):
        try:
            with open(self.parent.RECENT_PALETTES_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []