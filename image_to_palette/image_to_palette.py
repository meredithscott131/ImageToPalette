import sys
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication, QDockWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QImage, qRgb

from PyQt5.QtWidgets import ( 
        QLabel, QHBoxLayout, QDialog, QWidget, QVBoxLayout, QPlainTextEdit
) 

DOCKER_TITLE = 'Image to Palette'

class ImageToPalette(QDockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_TITLE)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        self.output_container = QHBoxLayout()
        self.output_container.setContentsMargins(5, 5, 5, 5) 
        self.setLayout(self.output_container)
        self.general_container =  QHBoxLayout()
        self.general_widget = QWidget() 

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.processImage(file_path)
        else:
            event.ignore()

    def processImage(self, file_path):
        self.label.setText("Processing image...")
        image = QImage(file_path)
        
        color_counts = {}
        for y in range(image.height()):
            for x in range(image.width()):
                pixel = image.pixel(x, y)
                rgb = qRgb(pixel & 0xff, (pixel >> 8) & 0xff, (pixel >> 16) & 0xff)
                if rgb in color_counts:
                    color_counts[rgb] += 1
                else:
                    color_counts[rgb] = 1

        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:5]  # Get top 5 colors

        palette = ""
        for color, _ in sorted_colors:
            palette += f"RGB: {qRed(color)}, {qGreen(color)}, {qBlue(color)}\n"

        self.paletteLabel.setText(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    docker_palette = ImageToPalette()
    app.setActiveWindow(docker_palette)
    docker_palette.show()
    sys.exit(app.exec_())