from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

class DocumenterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Documenter Window")
        self.setGeometry(400, 200, 600, 400)

        label = QLabel("Documenter Window Content")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
