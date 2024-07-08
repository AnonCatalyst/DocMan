from PyQt6.QtWidgets import QMainWindow, QToolBar, QLabel, QVBoxLayout, QWidget, QPushButton, QApplication, QDockWidget, QFrame, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap
import os
import sys
from src.documents import DocumentsWindow
from src.documenter import DocumenterWindow

class ImageLoader(QThread):
    image_loaded = pyqtSignal(QPixmap)
    finished = pyqtSignal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        pixmap = QPixmap()
        if pixmap.load(self.file_path):
            self.image_loaded.emit(pixmap)
        self.finished.emit()

class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # Add logo image
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Add a border and description label below the logo
        self.logo_separator = QLabel()
        self.logo_separator.setFixedHeight(1)
        self.logo_separator.setStyleSheet("background-color: #888888;")
        self.layout.addWidget(self.logo_separator)

        # Centered title
        self.logo_description = QLabel(" DocMan MENU ")
        self.logo_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_description.setStyleSheet("color: #888888; font-size: 10px;")
        self.layout.addWidget(self.logo_description)

        menu_items = ["DOCUMENTS", "DOCUMENTER"]
        for item in menu_items:
            button = QPushButton(item)
            button.setObjectName(item)  # Set object name to identify the button
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2E2E2E;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: center;  /* Center-align text */
                }
                QPushButton:hover {
                    background-color: #3E3E3E;
                }
                """
            )
            button.clicked.connect(self.handle_menu_item_click)  # Connect clicked signal to handler
            self.layout.addWidget(button)

        # Add a border and description label below the buttons
        self.button_separator = QLabel()
        self.button_separator.setFixedHeight(1)
        self.button_separator.setStyleSheet("background-color: #888888;")
        self.layout.addWidget(self.button_separator)

        # Centered description text
        self.button_description = QLabel(""" ~ Back Drop Build:v5:2024
DocMan: Document Manager
- Speed up your workflow!""")
        self.button_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_description.setStyleSheet("color: #888888; font-size: 10px;")
        self.layout.addWidget(self.button_description)

        # Add an additional stretch to move the border label close to the last menu item
        self.layout.addStretch()

        # Load logo image asynchronously
        self.load_logo_image_async()

    def load_logo_image_async(self):
        file_path = os.path.join('src', 'assets', 'icons', 'side_logo.png')
        self.image_loader = ImageLoader(file_path)
        self.image_loader.image_loaded.connect(self.update_logo)
        self.image_loader.finished.connect(self.cleanup_thread)
        self.image_loader.start()

    def update_logo(self, pixmap):
        self.logo_label.setPixmap(pixmap.scaledToWidth(100))

    def cleanup_thread(self):
        self.image_loader.quit()
        self.image_loader.wait()
        self.image_loader.deleteLater()

    def handle_menu_item_click(self):
        sender = self.sender()  # Get the button that triggered the signal
        if sender:
            item_name = sender.objectName()
            if item_name == "DOCUMENTS":
                main_window.show_window(DocumentsWindow)
            elif item_name == "DOCUMENTER":
                main_window.show_window(DocumenterWindow)

    def closeEvent(self, event):
        if hasattr(self, 'image_loader'):
            self.cleanup_thread()
        event.accept()

class MainStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.documents_window = DocumentsWindow()
        self.documenter_window = DocumenterWindow()

        self.addWidget(self.documents_window)
        self.addWidget(self.documenter_window)

    def show_window(self, window):
        if window == DocumentsWindow:
            self.setCurrentWidget(self.documents_window)
        elif window == DocumenterWindow:
            self.setCurrentWidget(self.documenter_window)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DocMan")
        self.setGeometry(300, 300, 1100, 600)

        self.setup_toolbar()
        self.setup_central_widget()
        self.setup_side_menu()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QToolBar {
                background-color: #34495e;
                border-bottom: 2px solid #2c3e50;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
            }
            QLabel {
                color: #ecf0f1;
            }
        """)

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setFloatable(False)

        self.add_toolbar_button(toolbar, "Home")
        self.add_toolbar_button(toolbar, "Help")

    def add_toolbar_button(self, toolbar, text):
        button = QPushButton(text)
        button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #2c3e50; color: #ecf0f1; border: none;")
        toolbar.addWidget(button)

    def setup_central_widget(self):
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        self.stacked_widget = MainStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        central_frame = QFrame()
        central_frame.setFrameShape(QFrame.Shape.StyledPanel)
        central_frame.setStyleSheet("background-color: #2c3e50; border: 2px solid #34495e;")
        central_frame.setLayout(central_layout)

        self.setCentralWidget(central_frame)

    def setup_side_menu(self):
        dock_widget = QDockWidget(self)
        dock_widget.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        self.side_menu = SideMenu(self)
        self.side_menu.setStyleSheet("QDockWidget { border: none; }")

        # Disable the closable feature to remove the close button
        dock_widget.setFeatures(dock_widget.features() & ~QDockWidget.DockWidgetFeature.DockWidgetClosable)

        dock_widget.setWidget(self.side_menu)
        dock_widget.setMinimumWidth(150)
        dock_widget.setMaximumWidth(150)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)

    def show_window(self, window_class):
        self.stacked_widget.show_window(window_class)

def main():
    app = QApplication(sys.argv)
    global main_window
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
