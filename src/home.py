import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import Qt

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocMan HOME")
        self.setGeometry(100, 100, 800, 600)

        # Set dark theme background
        self.set_dark_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)  # Add margins for better spacing

        self.add_description_section()
        self.add_feature_section("Documents Management", [
            ("Browse and Organize", "Efficiently manage your files with intuitive navigation through directories. Create, rename, delete, and open files seamlessly."),
            ("Preview Pane", "Quickly preview file content directly within the application for easy reference and management."),
            ("Batch Operations", "Perform bulk actions such as renaming or deleting multiple files at once to streamline your workflow.")
        ])
        self.add_feature_section("Documenter: Creating and Editing Documents", [
            ("Create and Edit", "Use the Documenter module to create, edit, and manage various document types within individual tabs."),
            ("Save and Load", "Easily save individual documents or all open documents to specified directories. Load existing files for quick editing and management."),
            ("Context Menu", "Right-click on tabs for options like saving changes and renaming documents, enhancing document management efficiency.")
        ])

    def set_dark_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2c3e50"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(Qt.GlobalColor.white))  
        self.setPalette(palette)

    def add_description_section(self):
        description_label = QLabel(
            "<h1>Welcome to DocMan</h1>"
            "<p>Your comprehensive document management tool designed to enhance efficiency in OSINT investigations.</p>"
        )
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("background-color: #34495e; color: #ddd;")
        self.layout.addWidget(description_label)

        self.add_divider_line()

    def add_feature_section(self, title, features):
        section_frame = QFrame()
        section_frame.setFrameShape(QFrame.Shape.StyledPanel)
        section_frame.setStyleSheet("background-color: #2c3e50; border-radius: 5px;")

        section_layout = QVBoxLayout(section_frame)

        title_label = QLabel(f"<h2>{title}</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("background-color: #34495e; color: #ddd;")
        section_layout.addWidget(title_label)

        for feature in features:
            feature_label = QLabel(f"<b>{feature[0]}</b><br>{feature[1]}")
            feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feature_label.setWordWrap(True)
            feature_label.setStyleSheet("color: #eee;")
            section_layout.addWidget(feature_label)

        self.layout.addWidget(section_frame)
        self.add_divider_line()

    def add_divider_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("border-color: #333;")
        self.layout.addWidget(line)