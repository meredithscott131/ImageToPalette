from krita import *
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent
from image_to_palette.managers import UIManager, RecentPalettesManager, PaletteManager, FileManager
from .model.Palette import Palette
import os

#---------------------------------------------------------#
# Image to Palette - Copyright (c) 2024 - Meredith Scott  #
#---------------------------------------------------------#
# Image to Palette is shared under the GNU General        #
# Public License (GPL), version 3.                        #
#---------------------------------------------------------#
# A Krita docker plugin that allows you to quickly        #
# generate color palettes from images.                    #
#---------------------------------------------------------#
class ImageToPalette(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image to Palette')
        self.setAcceptDrops(True)

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Define RECENT_PALETTES_FILE in the current directory
        # File is for storing the recent palette history
        self.RECENT_PALETTES_FILE = os.path.join(current_dir, '.krita_recent_palettes.json')

        # Initializing Palette
        self.palette = Palette()

        # Initializing Managers
        self.recent_palettes_manager = RecentPalettesManager(self)
        self.ui_manager = UIManager(self)
        self.file_manager = FileManager(self)
        self.palette_manager = PaletteManager(self)

        # Initializing UI
        self.main_widget = self.ui_manager.create_main_widget()
        self.setWidget(self.main_widget)
        self.original_bg_color = self.main_widget.palette().color(self.main_widget.backgroundRole())

    # Sets recommended size of the docker    
    def sizeHint(self):
        return QSize(300, 200)

    # Handles the drag enter event
    def dragEnterEvent(self, event: QDragEnterEvent):
        self.ui_manager.handle_drag_enter(event)

    # Handles the drag leave event
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.ui_manager.animate_background_color(self.original_bg_color)

    # Handles the drop event
    def dropEvent(self, event: QDropEvent):
        self.ui_manager.handle_drop_event(event)

    # Handles a resize event
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.recent_palettes_manager.update_recent_palettes_combo()