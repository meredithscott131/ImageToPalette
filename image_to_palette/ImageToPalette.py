from krita import *
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QDockWidget, QHBoxLayout, QFileDialog, QLabel, QMenu, QAction
from PyQt5.QtCore import QSize, Qt

import json
import os
from .Button import Button
from .PaletteGrid import PaletteGrid
from .Palette import Palette

DOCKER_TITLE = 'Image to Palette'

# Path to store recent palettes
RECENT_PALETTES_FILE = os.path.join(os.path.expanduser('~'), '.krita_recent_palettes.json')

class ImageToPalette(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.setAcceptDrops(True)
        self.image_path = None
        self.palette = Palette()
        self.recent_palettes = self.load_recent_palettes()  # Load recent palettes from file
        self.initUI()
        self.original_bg_color = self.main_widget.palette().color(self.main_widget.backgroundRole())

    # Setting the initial UI of the docker
    def initUI(self):
        # Creating main widget and layout
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Creating a horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)  # Set spacing between buttons
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Creating "Load Image" button
        self.button_load = Button(icon_name='folder-pictures', tooltip='Create Palette from Image')
        self.button_load.clicked.connect(self.openFile)

        # Creating "Regenerate Palette" button
        self.button_regenerate = Button(icon_name='view-refresh', tooltip='Regenerate Palette')
        self.button_regenerate.clicked.connect(self.regeneratePalette)
        self.button_regenerate.setEnabled(False)

        # Creating "Save Palette" button
        self.button_save = Button(icon_name='document-save', tooltip='Save Palette')
        self.button_save.clicked.connect(self.save_palette)
        self.button_save.setEnabled(False)

        # Creating "Load Palette" button
        self.button_load_palette = Button(icon_name='document-open', tooltip='Load Palette')
        self.button_load_palette.clicked.connect(self.load_palette)

        # Dropdown for recent palettes
        self.recent_palettes_button = QPushButton("Recent Palettes")
        self.recent_palettes_button.setStyleSheet("text-align: left; padding-left: 10px; padding-right: 20px;")  # Adjust left padding
        self.recent_palettes_menu = QMenu(self.recent_palettes_button)
        self.recent_palettes_menu.aboutToShow.connect(self.adjust_menu_size)  # Adjust menu size just before it's shown
        self.recent_palettes_button.setMenu(self.recent_palettes_menu)

        # Adding buttons to the button layout
        button_layout.addWidget(self.button_load)
        button_layout.addWidget(self.button_load_palette)
        button_layout.addWidget(self.button_save)
        button_layout.addWidget(self.button_regenerate)
        button_layout.addWidget(self.recent_palettes_button)  # Add stretch factor to expand the dropdown

        # Adding the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Creating a label to display the loaded image's name
        self.image_name_label = QLabel("No image loaded")
        main_layout.addWidget(self.image_name_label)

        # Creating a grid layout for the color palette
        self.palette_layout = PaletteGrid()
        main_layout.addLayout(self.palette_layout)

        # Setting main layout
        self.main_widget.setLayout(main_layout)
        self.setWidget(self.main_widget)

        # Setting the default grid with placeholder colors
        self.createDefaultGrid()

    # Override sizeHint to set initial size of the docker widget
    def sizeHint(self):
        return QSize(200, 200)

    # Open file dialog to select image
    def openFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image_path = file_path
            self.createColorPalette()
            self.image_name_label.setText(os.path.basename(file_path))

    # Generating a color palette from the set image path
    def createColorPalette(self):
        self.palette.collectColors(self.image_path)
        self.palette.generatePalette()
        self.displayPalette()
        self.button_regenerate.setEnabled(True)
        self.button_save.setEnabled(True)

    # Display the palette in the grid layout
    def displayPalette(self):
        self.palette_layout.displayColorsInGrid(self.palette)

    # Regenerating the color palette from the current image path
    def regeneratePalette(self):
        self.palette.generatePalette()
        self.displayPalette()

    # Setting the default palette grid to a gray placeholder color
    def createDefaultGrid(self):
        placeholder_palette = Palette()
        for _ in range(15):
            placeholder_palette.add_color("#919191")
        self.palette_layout.displayColorsInGrid(placeholder_palette, selectable=False)

    def save_palette(self):
        file_name = self.palette.save_palette()
        if file_name:
            self.update_recent_palettes(file_name)

    def load_palette(self):
        file_name = self.palette.load_palette()
        if file_name:
            self.update_recent_palettes(file_name)
            self.displayPalette()
            self.image_name_label.setText(os.path.basename(self.palette.image_name))
            self.button_regenerate.setEnabled(True)
            self.button_save.setEnabled(True)

    def load_palette_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.update_recent_palettes(file)
            data = json.load(file)
            self.palette.name = data["name"]
            self.palette.cur_colors = data["current colors"]
            self.palette.total_colors = [(color, count) for color, count in data.get("total colors", [])]
            self.palette.image_name = data.get("image_name")  # Load the image name
            self.displayPalette()
            self.image_name_label.setText(os.path.basename(self.palette.image_name))
            self.button_regenerate.setEnabled(True)
            self.button_save.setEnabled(True)

    def update_recent_palettes_menu(self):
        self.recent_palettes_menu.clear()
        for palette_path in self.recent_palettes:
            action = QAction(os.path.basename(palette_path), self)
            action.triggered.connect(lambda checked=False, path=palette_path: self.load_palette_from_file(path))
            self.recent_palettes_menu.addAction(action)

    def update_recent_palettes(self, file_name):
        if file_name not in self.recent_palettes:
            self.recent_palettes.insert(0, file_name)
        if len(self.recent_palettes) > 5:
            self.recent_palettes.pop()
        self.update_recent_palettes_menu()
        self.save_recent_palettes()  # Save recent palettes to file

    def save_recent_palettes(self):
        with open(RECENT_PALETTES_FILE, 'w') as file:
            json.dump(self.recent_palettes, file)

    def load_recent_palettes(self):
        try:
            with open(RECENT_PALETTES_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def adjust_menu_size(self):
        # Calculate desired width based on parent button width
        width = self.recent_palettes_button.width()
        # Ensure it doesn't get wider than the docker width
        docker_width = self.width()
        if width > docker_width:
            width = docker_width
        self.recent_palettes_menu.setMinimumWidth(width)
        self.recent_palettes_menu.setMaximumWidth(width)

    def resizeEvent(self, event):
        # Adjust menu size when docker is resized
        self.adjust_menu_size()
        super().resizeEvent(event)

    def show_recent_palettes_menu(self):
        # Show the menu below the button
        self.recent_palettes_menu.exec_(self.recent_palettes_button.mapToGlobal(QPoint(0, self.recent_palettes_button.height())))

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                if url.isLocalFile() and url.toLocalFile().lower().endswith(('.png', '.jpg', '.bmp', '.json')):
                    self.animateBackgroundColor(QColor('#636363'))
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.animateBackgroundColor(self.original_bg_color)  # Default color

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile().lower()
                    if file_path.endswith(('.png', '.jpg', '.bmp')):
                        self.image_path = file_path
                        self.createColorPalette()
                        self.image_name_label.setText(f"{self.image_path.split('/')[-1]}")
                        event.acceptProposedAction()
                        self.animateBackgroundColor(self.original_bg_color)  # Reset color after drop
                        return
                    elif file_path.endswith('.json'):
                        self.load_palette_from_file(file_path)
                        event.acceptProposedAction()
                        self.animateBackgroundColor(self.original_bg_color)  # Reset color after drop
                        return
                    self.update_recent_palettes(file_path)
        event.ignore()

    def animateBackgroundColor(self, color):
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(200)  # Duration of the fade
        self.animation.setStartValue(self.main_widget.palette().color(self.main_widget.backgroundRole()))
        self.animation.setEndValue(color)
        self.animation.valueChanged.connect(self.setBackgroundColor)
        self.animation.start()

    def setBackgroundColor(self, color):
        palette = self.main_widget.palette()
        palette.setColor(self.main_widget.backgroundRole(), color)
        self.main_widget.setPalette(palette)
        self.main_widget.setAutoFillBackground(True)