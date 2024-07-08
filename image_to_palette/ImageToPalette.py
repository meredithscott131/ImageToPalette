from krita import *
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QDockWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, QSize, QUrl, QPropertyAnimation, QVariantAnimation
from PyQt5.QtGui import QImage, QDragEnterEvent, QDropEvent, QColor
from collections import Counter
import json
import random
from .Button import Button
from .PaletteGrid import PaletteGrid

DOCKER_TITLE = 'Image to Palette'

class ImageToPalette(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.setAcceptDrops(True)
        self.image_path = None
        self.initUI()

    # Setting the initial UI of the docker
    def initUI(self):
        # Creating main widget and layout
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Creating a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Creating "Load Image" button
        self.button_load = Button(icon_name='document-open', tooltip='Load Image')
        self.button_load.clicked.connect(self.openFile)

        # Creating "Regenerate Palette" button
        self.button_regenerate = Button(icon_name='view-refresh', tooltip='Regenerate Palette')
        self.button_regenerate.clicked.connect(self.regeneratePalette)

        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_palette)

        # Adding buttons to the button layout
        button_layout.addWidget(self.button_load)
        button_layout.addWidget(self.button_regenerate)
        button_layout.addWidget(self.button_save)
        button_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        main_layout.addLayout(button_layout)

        # Creating a grid layout for the color palette
        self.palette_layout = PaletteGrid()
        main_layout.addLayout(self.palette_layout)

        # Setting main layout
        self.main_widget.setLayout(main_layout)
        self.setWidget(self.main_widget)

        # Setting the default grid with placeholder colors
        self.createDefaultGrid()

        # Store the original background color
        self.original_bg_color = self.main_widget.palette().color(self.main_widget.backgroundRole())
    
    # Override sizeHint to set initial size of the docker widget
    def sizeHint(self):
        return QSize(300, 400)

    # Open file dialog to select image
    def openFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image_path = file_path
            print(f"Selected image path: {self.image_path}")
            self.createColorPalette()

    # Generating a color palette from the set image path
    def createColorPalette(self):
        # Loading the image
        image = QImage(self.image_path)

        # Resizing the image to reduce the number of pixels to process
        image = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Counting the frequency of each color in the image
        color_counter = Counter()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y).rgb()
                color_counter[color] += 1

        # Collecting and shuffling the most common colors
        most_common_colors = color_counter.most_common()
        random.shuffle(most_common_colors)
        
        # Manually selecting diverse colors
        num_colors = 15
        step = len(most_common_colors) // num_colors
        palette = [most_common_colors[i * step][0] for i in range(num_colors)]
        
        print(f"Palette: {palette}")

        # Clearing the previous palette
        self.clearPalette()

        # Displaying the palette in the grid layout
        self.palette_layout.displayColorsInGrid(palette, selectable=True)

    # Regenerating the color palette from the current image path
    def regeneratePalette(self):
        if self.image_path:
            self.createColorPalette()

    # Setting the default palette grid to a gray placeholder color
    def createDefaultGrid(self):
        placeholder_colors = [0x919191] * 15
        self.palette_layout.displayColorsInGrid(placeholder_colors, selectable=False)

    # Clearing the current palette
    def clearPalette(self):
        self.palette_layout.clearPalette()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                if url.isLocalFile() and url.toLocalFile().lower().endswith(('.png', '.jpg', '.bmp')):
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
                if url.isLocalFile() and url.toLocalFile().lower().endswith(('.png', '.jpg', '.bmp')):
                    self.image_path = url.toLocalFile()
                    print(f"Dropped image path: {self.image_path}")
                    self.createColorPalette()
                    event.acceptProposedAction()
                    self.animateBackgroundColor(self.original_bg_color)  # Reset color after drop
                    return
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
    
    def get_palette_colors(self):
        # Implement this function to return the current palette colors
        # Example: return a list of color hex codes
        return ['#FF5733', '#33FF57', '#3357FF']

    def save_palette(self):
        # Get the palette colors
        palette_colors = self.get_palette_colors()
        
        # Open a file dialog to select the save location
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Palette", "", "JSON Files (*.json);;All Files (*)", options=options)
        
        if file_name:
            # Save the palette colors to the selected file
            with open(file_name, 'w') as file:
                json.dump(palette_colors, file)