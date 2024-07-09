from krita import *
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QDockWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, QSize, QVariantAnimation
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QColor
from .Button import Button
from .PaletteGrid import PaletteGrid
from .Palette import Palette

DOCKER_TITLE = 'Image to Palette'

class ImageToPalette(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.setAcceptDrops(True)
        self.image_path = None
        self.palette = Palette()  # Initialize Palette object
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

        # Creating "Save Palette" button
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save_palette)

        # Creating "Load Palette" button
        self.button_load_palette = QPushButton("Load Palette")
        self.button_load_palette.clicked.connect(self.load_palette)

        # Adding buttons to the button layout
        button_layout.addWidget(self.button_load)
        button_layout.addWidget(self.button_regenerate)
        button_layout.addWidget(self.button_save)
        button_layout.addWidget(self.button_load_palette)
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
            self.createColorPalette()

    # Generating a color palette from the set image path
    def createColorPalette(self):
        self.palette.createColorPalette(self.image_path)
        self.displayPalette()

    # Display the palette in the grid layout
    def displayPalette(self):
        self.palette_layout.displayColorsInGrid(self.palette)

    # Regenerating the color palette from the current image path
    def regeneratePalette(self):
        self.palette.regeneratePalette()
        self.displayPalette()

    # Setting the default palette grid to a gray placeholder color
    def createDefaultGrid(self):
        placeholder_palette = Palette()
        for _ in range(15):
            placeholder_palette.add_color("#919191")
        self.palette_layout.displayColorsInGrid(placeholder_palette, selectable=False)

    def save_palette(self):
        self.palette.save_palette()

    def load_palette(self):
        self.palette.load_palette()
        self.displayPalette()

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