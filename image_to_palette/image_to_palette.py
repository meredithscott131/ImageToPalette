import sys
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QDockWidget, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

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

        # Create button
        self.button = QPushButton('Select Image')
        self.button.clicked.connect(self.openFileDialog)
        self.button.setStyleSheet("text-align: left; padding-left: 10px;")

        # Add button to layout with alignment to the top
        main_layout.addWidget(self.button, alignment=Qt.AlignTop)

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

# Initialize the application (for standalone testing)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ImageToPalette()
    main_window.show()
    sys.exit(app.exec_())