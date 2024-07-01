import sys
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication, QDockWidget, QPushButton, QFileDialog, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor
from collections import Counter

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

        # Create a grid layout for the color palette (2 rows, 5 columns)
        self.palette_layout = QGridLayout()
        self.palette_layout.setAlignment(Qt.AlignTop)  # Align grid layout to the top

         # Initialize the grid with white color labels
        for i in range(10):
            row, col = divmod(i, 5)
            color_label = QLabel()
            color_label.setFixedSize(50, 50)
            color_label.setStyleSheet("background-color: #919191;")
            self.palette_layout.addWidget(color_label, row, col)

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

        # Get the 10 most common colors
        most_common_colors = color_counter.most_common(10)
        palette = [color for color, _ in most_common_colors]
        print(f"Palette: {palette}")

        # Clear the previous palette
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Display the palette in the grid layout (2 rows, 5 columns)
        for i, color in enumerate(palette):
            row, col = divmod(i, 5)
            color_label = QLabel()
            color_label.setFixedSize(50, 50)
            color_label.setStyleSheet(f"background-color: #{color:06x};")
            self.palette_layout.addWidget(color_label, row, col)

# Initialize the application (for standalone testing)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ImageToPalette()
    main_window.show()
    sys.exit(app.exec_())