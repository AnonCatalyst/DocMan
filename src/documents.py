from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class DocumentsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Documents Window")
        self.setGeometry(400, 200, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        label = QLabel("This is the Documents Window")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(layout)
