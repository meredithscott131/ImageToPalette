import sys
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication, QDockWidget, QPushButton, QFileDialog, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from collections import Counter
from PyQt5.QtGui import QImage

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

        # Create a grid layout for the color palette
        self.palette_layout = QGridLayout()
        self.palette_layout.setAlignment(Qt.AlignTop)  # Align grid layout to the top

        # Set margins for the palette layout
        self.palette_layout.setContentsMargins(5, 3, 5, 5)  # Add margins (left, top, right, bottom)

        # Create button
        self.button = QPushButton('Select Image')
        self.button.clicked.connect(self.openFileDialog)
        self.button.setStyleSheet("text-align: left; padding-left: 10px;")

        # Adding components
        main_layout.addWidget(self.button, alignment=Qt.AlignTop)
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

        # Get the most common colors (up to 10)
        most_common_colors = color_counter.most_common(10)
        palette = [color for color, _ in most_common_colors]
        print(f"Palette: {palette}")

        # Clear the previous palette
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Display the palette in the grid layout dynamically
        self.displayColorsInGrid(palette)

    def createDefaultGrid(self):
        # Create a default grid with placeholder colors
        placeholder_colors = [0x919191] * 10  # Default grey color placeholders
        self.displayColorsInGrid(placeholder_colors)

    def displayColorsInGrid(self, colors):
        # Determine grid size
        num_colors = len(colors)
        num_cols = min(num_colors, 5)  # Maximum of 5 columns
        num_rows = (num_colors + num_cols - 1) // num_cols  # Calculate number of rows

        for i, color in enumerate(colors):
            row, col = divmod(i, num_cols)
            color_label = QLabel()
            color_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set expanding size policy
            color_label.setStyleSheet(f"background-color: #{color:06x};")
            self.palette_layout.addWidget(color_label, row, col)

        # Set row and column stretches
        for r in range(num_rows):
            self.palette_layout.setRowStretch(r, 1)

        for c in range(num_cols):
            self.palette_layout.setColumnStretch(c, 1)

# Initialize the application (for standalone testing)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ImageToPalette()
    main_window.show()
    sys.exit(app.exec_())
