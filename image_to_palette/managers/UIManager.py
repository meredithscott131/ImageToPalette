from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QLabel, QSizePolicy, QPushButton, QGridLayout,  QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QVariantAnimation
from PyQt5.QtGui import QColor, QDragEnterEvent, QDropEvent
from krita import ManagedColor, Krita
from ..model.Palette import Palette

# Represents a square button with an icon and hovering tool description
class Button(QPushButton):
    def __init__(self, icon_name, tooltip):
        super().__init__()
        self.setIcon(Krita.instance().icon(icon_name))
        self.setFixedSize(32, 32)
        self.setToolTip(tooltip)
        self.setStyleSheet("""
            QPushButton {
                border: none;
            }
            QPushButton:hover {
                border: 1px solid #5e5e5e;
            }
        """)

# Represents the grid displaying the selectable colors in the palette
class PaletteGrid(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        self.setContentsMargins(5, 3, 5, 5)

    # Displays the color labels in the grid
    def displayColorsInGrid(self, palette, selectable=True):
        colors = [int(color.lstrip('#'), 16) for color in palette.cur_colors]
        num_cols = 5
        num_rows = 3

        # Iterates through each color and makes it a label
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

    # Sets the current foreground color of the canvas
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


# =========================================================================================================================== #


# Manages the UI display of the docker
class UIManager:
    def __init__(self, parent):
        self.parent = parent

    # Creates and returns the main widget of the docker
    def create_main_widget(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top-most row of buttons and Recent Palettes ComboBox
        button_layout = self.create_button_layout()
        main_layout.addLayout(button_layout)

        # Label displaying the origin image name of the palette
        self.parent.image_name_label = QLabel("No palette loaded")
        self.parent.image_name_label.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.parent.image_name_label)

        # 15-color palette grid
        self.parent.palette_layout = PaletteGrid()
        main_layout.addLayout(self.parent.palette_layout)

        main_widget.setLayout(main_layout)
        self.create_default_grid()
        return main_widget

    # Creates and returns the button layout
    def create_button_layout(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Button for loading a new palette from an image
        self.parent.button_load = self.create_button('folder-pictures', 'Create Palette from Image',
                                                     self.parent.file_manager.open_image_dialog)
        
        # Button for loading a pre-existing palette from a palette json file
        self.parent.button_load_palette = self.create_button('document-open', 'Load Palette',
                                                        self.parent.file_manager.load_palette_dialog)
        
        # Button for saving the currently loaded palette
        # Disabled until a palette is loaded
        self.parent.button_save = self.create_button('document-save', 'Save Palette',
                                                     self.parent.file_manager.save_palette_dialog, False)
        
        # Button for regenerating a new set of 15-colors for the currently loaded palette
        # Disabled until a palette is loaded
        self.parent.button_regenerate = self.create_button('view-refresh', 'Regenerate Palette',
                                                           self.parent.palette_manager.regenerate_palette, False)
        
        # ComboBox for displaying the 5 most recently opened saved palettes
        self.parent.recent_palettes_combo = QComboBox()
        self.parent.recent_palettes_combo.setEditable(True)
        self.parent.recent_palettes_combo.lineEdit().setReadOnly(True)
        self.parent.recent_palettes_combo.lineEdit().setAlignment(Qt.AlignLeft)
        self.parent.recent_palettes_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.parent.recent_palettes_combo.view().setTextElideMode(Qt.ElideRight)
        self.parent.recent_palettes_combo.lineEdit().setText("Recent Palettes")
        self.parent.recent_palettes_combo.activated.connect(self.parent.recent_palettes_manager.load_selected_recent_palette)

        # Adding components to the layout
        button_layout.addWidget(self.parent.button_load)
        button_layout.addWidget(self.parent.button_load_palette)
        button_layout.addWidget(self.parent.button_save)
        button_layout.addWidget(self.parent.button_regenerate)
        button_layout.addWidget(self.parent.recent_palettes_combo)

        return button_layout

    # Creates and returns a button with the given icon, tooltip, function call, and enabled state
    def create_button(self, icon_name, tooltip, callback, enabled=True):
        button = Button(icon_name=icon_name, tooltip=tooltip)
        button.clicked.connect(callback)
        button.setEnabled(enabled)
        return button

    # Enables the save and regenerate palette buttons
    def enable_buttons(self):
        self.parent.button_save.setEnabled(True)
        self.parent.button_regenerate.setEnabled(True)

    # Creates the default palette grid out of gray, unselectable color labels
    def create_default_grid(self):
        placeholder_palette = Palette()
        for _ in range(15):
            placeholder_palette.add_color("#919191")
        self.parent.palette_layout.displayColorsInGrid(placeholder_palette, selectable=False)

    # Handles the event where the user drags an image or palette json file over the docker
    # Animates a background fade
    def handle_drag_enter(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                if url.isLocalFile() and url.toLocalFile().lower().endswith(('.png', '.jpg', '.bmp', '.json')):
                    self.animate_background_color(QColor('#636363'))
                    event.acceptProposedAction()
                    return
        event.ignore()

    # Handles the event where the user drops an image or palette json file into the docker
    def handle_drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    
                    # User drops an image file to create a new palette
                    if file_path.endswith(('.png', '.jpg', '.bmp')):
                        try:
                            self.parent.file_manager.open_image(file_path)
                            event.acceptProposedAction()
                            self.animate_background_color(self.parent.original_bg_color)
                            return
                        except Exception as e:
                            self.show_error_popup("Error Loading File", f"An error occurred while loading the file: {e}")
                            self.set_background_color(self.parent.original_bg_color)  # Ensure background color is reset
                            return
                    # User drops a pre-existing palette json file
                    elif file_path.endswith('.json'):
                        try:
                            self.parent.file_manager.load_palette(file_path)
                            event.acceptProposedAction()
                            self.animate_background_color(self.parent.original_bg_color)
                            return
                        except Exception as e:
                            self.show_error_popup("Error Loading Palette", f"An error occurred while loading the palette: {e}")
                            self.set_background_color(self.parent.original_bg_color)  # Ensure background color is reset
                            return

        # Invalid file type or path so ignore
        self.set_background_color(self.parent.original_bg_color)
        event.ignore()
        
    # Animates the background color of the docker to indicate drag-and-drop
    def animate_background_color(self, color):
        self.animation = QVariantAnimation(self.parent)
        self.animation.setDuration(200)
        self.animation.setStartValue(self.parent.main_widget.palette().color(self.parent.main_widget.backgroundRole()))
        self.animation.setEndValue(color)
        self.animation.valueChanged.connect(self.set_background_color)
        self.animation.start()

    # Sets the background color of the docker
    def set_background_color(self, color):
        palette = self.parent.main_widget.palette()
        palette.setColor(self.parent.main_widget.backgroundRole(), color)
        self.parent.main_widget.setPalette(palette)
        self.parent.main_widget.setAutoFillBackground(True)
    
    # Displays an error popup with the given title and message
    def show_error_popup(self, title, message):
        error_dialog = QMessageBox(self.parent)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()