import sys
from krita import *
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication, QDockWidget, QPushButton, QFileDialog, QGridLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QColor, QPalette, QBrush
from collections import Counter
import random

DOCKER_TITLE = 'Image to Palette'

class ImageToPalette(QDockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.setAcceptDrops(True)
        self.image_path = None
        self.initUI()

    def initUI(self):
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create "Select Image" button
        self.button_select = QPushButton()
        self.button_select.setIcon(Krita.instance().icon('document-open'))
        self.button_select.setFixedSize(32, 32)
        self.button_select.setToolTip("Load Image")
        self.button_select.setStyleSheet("""
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                border: 1px solid #5e5e5e;
            }
        """)
        self.button_select.clicked.connect(self.openFileDialog)

        # Create "Regenerate Palette" button with Krita icon
        self.button_regenerate = QPushButton()
        self.button_regenerate.setIcon(Krita.instance().icon('view-refresh'))
        self.button_regenerate.setFixedSize(32, 32)
        self.button_regenerate.setToolTip("Regenerate Palette")
        self.button_regenerate.setStyleSheet("""
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                border: 1px solid #5e5e5e;
            }
        """)
        self.button_regenerate.clicked.connect(self.regeneratePalette)

        # Add buttons to the button layout
        button_layout.addWidget(self.button_select)
        button_layout.addWidget(self.button_regenerate)
        button_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        main_layout.addLayout(button_layout)

        # Create a grid layout for the color palette
        self.palette_layout = QGridLayout()
        self.palette_layout.setAlignment(Qt.AlignTop)  # Align grid layout to the top

        # Set margins for the palette layout
        self.palette_layout.setContentsMargins(5, 3, 5, 5)  # Add margins (left, top, right, bottom)

        # Adding components
        main_layout.addLayout(self.palette_layout)

        # Set main layout
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)

        # Create the default grid with placeholder colors
        self.createDefaultGrid()

    def sizeHint(self):
        # Override sizeHint to set initial size of the docker widget
        return QSize(300, 400)  # Adjust these values as needed

    def openFileDialog(self):
        # Open file dialog to select image
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image_path = file_path
            print(f"Selected image path: {self.image_path}")
            self.createColorPalette()

    def createColorPalette(self):
        # Load the image
        image = QImage(self.image_path)

        # Resize the image to reduce the number of pixels to process
        image = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Count the frequency of each color in the image
        color_counter = Counter()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y).rgb()
                color_counter[color] += 1

        # Get the most common colors
        most_common_colors = color_counter.most_common()
        
        # Shuffle the list of most common colors
        random.shuffle(most_common_colors)
        
        # Manually select diverse colors
        num_colors = 15
        step = len(most_common_colors) // num_colors
        palette = [most_common_colors[i * step][0] for i in range(num_colors)]
        
        print(f"Palette: {palette}")

        # Clear the previous palette
        self.clearPalette()

        # Display the palette in the grid layout dynamically
        self.displayColorsInGrid(palette)

    def regeneratePalette(self):
        if self.image_path:
            self.createColorPalette()

    def createDefaultGrid(self):
        # Create a default grid with placeholder colors
        placeholder_colors = [0x919191] * 15  # Default grey color placeholders
        self.displayColorsInGrid(placeholder_colors)

    def displayColorsInGrid(self, colors):
        # Determine grid size
        num_cols = 5
        num_rows = 3

        for i, color in enumerate(colors):
            row, col = divmod(i, num_cols)
            color_label = QLabel()
            color_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set expanding size policy
            color_label.setStyleSheet(f"background-color: #{color:06x};")
            color_label.mousePressEvent = lambda event, c=color: self.setFGColor(event, c)
            self.palette_layout.addWidget(color_label, row, col)

        # Set row and column stretches
        for r in range(num_rows):
            self.palette_layout.setRowStretch(r, 1)

        for c in range(num_cols):
            self.palette_layout.setColumnStretch(c, 1)

    def clearPalette(self):
        # Clear the previous palette
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def setFGColor(self, event, color):
        activeView = Krita.instance().activeWindow().activeView()
        
        # Create a ManagedColor object
        colorRed = ManagedColor("RGBA", "U8", "")
        
        # Extract RGB components from the color
        red = ((color >> 16) & 0xFF) / 255.0
        green = ((color >> 8) & 0xFF) / 255.0
        blue = (color & 0xFF) / 255.0
        
        # Set the color components
        colorComponents = colorRed.components()
        colorComponents[0] = blue
        colorComponents[1] = green
        colorComponents[2] = red
        colorComponents[3] = 1.0  # Alpha (fully opaque)
        
        # Set the components back to the ManagedColor object
        colorRed.setComponents(colorComponents)
        
        # Set the foreground color in the active view
        activeView.setForeGroundColor(colorRed)


# Initialize the application (for standalone testing)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ImageToPalette()
    main_window.show()
    sys.exit(app.exec_())