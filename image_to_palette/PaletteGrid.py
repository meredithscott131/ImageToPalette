from PyQt5.QtWidgets import QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from krita import ManagedColor, Krita

class PaletteGrid(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        self.setContentsMargins(5, 3, 5, 5)

    def displayColorsInGrid(self, palette, selectable=True):
        colors = [int(color.lstrip('#'), 16) for color in palette.colors]
        num_cols = 5
        num_rows = (len(colors) + num_cols - 1) // num_cols

        for i, color in enumerate(colors):
            row, col = divmod(i, num_cols)
            color_label = QLabel()
            color_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            color_label.setStyleSheet(f"background-color: #{color:06x};")
            if selectable:
                color_label.mousePressEvent = lambda event, c=color: self.setFGColor(event, c)
            self.addWidget(color_label, row, col)

        for r in range(num_rows):
            self.setRowStretch(r, 1)

        for c in range(num_cols):
            self.setColumnStretch(c, 1)

    def clearPalette(self):
        while self.count():
            item = self.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def setFGColor(self, event, color):
        activeView = Krita.instance().activeWindow().activeView()
        managedColor = ManagedColor("RGBA", "U8", "")
        red = ((color >> 16) & 0xFF) / 255.0
        green = ((color >> 8) & 0xFF) / 255.0
        blue = (color & 0xFF) / 255.0
        colorComponents = managedColor.components()
        colorComponents[0] = blue
        colorComponents[1] = green
        colorComponents[2] = red
        colorComponents[3] = 1.0
        managedColor.setComponents(colorComponents)
        activeView.setForeGroundColor(managedColor)