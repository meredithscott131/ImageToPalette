from PyQt5.QtWidgets import QPushButton
from krita import Krita

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