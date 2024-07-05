from PyQt5.QtWidgets import QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from krita import ManagedColor, Krita

class PaletteGrid(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        self.setContentsMargins(5, 3, 5, 5)

    def displayColorsInGrid(self, colors, selectable=True):
        # Determine grid size
        num_cols = 5
        num_rows = 3

        for i, color in enumerate(colors):
            row, col = divmod(i, num_cols)
            color_label = QLabel()
            color_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set expanding size policy
            color_label.setStyleSheet(f"background-color: #{color:06x};")
            if selectable:
                color_label.mousePressEvent = lambda event, c=color: self.setFGColor(event, c)
            self.addWidget(color_label, row, col)

        # Set row and column stretches
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
        
        # Create a ManagedColor object
        managedColor = ManagedColor("RGBA", "U8", "")
        
        # Extract RGB components from the color
        red = ((color >> 16) & 0xFF) / 255.0
        green = ((color >> 8) & 0xFF) / 255.0
        blue = (color & 0xFF) / 255.0
        
        # Set the color components
        colorComponents = managedColor.components()
        colorComponents[0] = blue
        colorComponents[1] = green
        colorComponents[2] = red
        colorComponents[3] = 1.0  # Alpha (fully opaque)
        
        # Set the components back to the ManagedColor object
        managedColor.setComponents(colorComponents)
        
        # Set the foreground color in the active view
        activeView.setForeGroundColor(managedColor)