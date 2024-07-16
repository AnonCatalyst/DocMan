import os
import sys
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QDateTime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QVBoxLayout, QWidget,
    QPushButton, QDockWidget, QFrame, QStackedWidget, QTextEdit
)
from PyQt6.QtGui import QPixmap, QAction
import logging

# Import custom windows
from src.documents import DocumentsWindow
from src.documenter import Documenter
from src.help import HelpWindow
from src.home import HomeWindow
from src.logging import LoggingWindow

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
        self.parent = parent
        self.image_loader = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.setup_logo()
        self.setup_menu_buttons()
        self.setup_description()

        self.load_logo_image_async()

    def setup_logo(self):
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo_label)

        self.logo_separator = QLabel()
        self.logo_separator.setFixedHeight(1)
        self.logo_separator.setStyleSheet("background-color: #888888;")
        self.layout.addWidget(self.logo_separator)

        self.logo_description = QLabel(" DOCMAN MENU ")
        self.logo_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_description.setStyleSheet("color: #888888; font-size: 10px;")
        self.layout.addWidget(self.logo_description)

    def setup_menu_buttons(self):
        menu_items = ["DOCUMENTS", "DOCUMENTER"]
        for item in menu_items:
            button = QPushButton(item)
            button.setObjectName(item)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2E2E2E;
                    color: white;
                    border: none;
                    padding: 10px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #3E3E3E;
                }
                """
            )
            button.clicked.connect(self.handle_menu_item_click)
            self.layout.addWidget(button)

        self.button_separator = QLabel()
        self.button_separator.setFixedHeight(1)
        self.button_separator.setStyleSheet("background-color: #888888;")
        self.layout.addWidget(self.button_separator)

    def setup_description(self):
        self.button_description = QLabel("""DocMan was developed during
the 2024 v5 BackDropBuild
session (July 8 - August 3,
2024) to enhance OSINT
investigations. This four
-week program provided fu
nding and support for inn
ovative solutions. DocMan
was created to meet the 
specific needs of OSINT 
professionals, offering a
robust document management
system. The development
focused on modern software
practices, modular arch
itecture, and user-centric
design to improve workf
lows and data management.""")
        self.button_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_description.setStyleSheet("color: #888888; font-size: 10px;")
        self.layout.addWidget(self.button_description)
        self.layout.addStretch()

    def load_logo_image_async(self):
        file_path = os.path.join('src', 'assets', 'icons', 'side_logo.png')
        self.image_loader = ImageLoader(file_path)
        self.image_loader.image_loaded.connect(self.update_logo)
        self.image_loader.finished.connect(self.cleanup_thread)
        self.image_loader.start()

    def update_logo(self, pixmap):
        self.logo_label.setPixmap(pixmap.scaledToWidth(100))

    def cleanup_thread(self):
        if self.image_loader is not None:
            self.image_loader.quit()
            self.image_loader.wait()
            self.image_loader.deleteLater()
            self.image_loader = None

    def handle_menu_item_click(self):
        sender = self.sender()
        if sender:
            item_name = sender.objectName()
            self.parent.log_interaction(f"Button clicked: {item_name}")
            if item_name == "DOCUMENTS":
                self.parent.show_window(DocumentsWindow)
            elif item_name == "DOCUMENTER":
                self.parent.show_window(Documenter)

    def closeEvent(self, event):
        self.cleanup_thread()
        event.accept()

class MainStackedWidget(QStackedWidget):
    window_opened = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.home_window = HomeWindow()
        self.help_window = HelpWindow()
        self.documents_window = DocumentsWindow()
        self.documenter_window = Documenter()
        self.logging_window = LoggingWindow()

        self.addWidget(self.home_window)
        self.addWidget(self.help_window)
        self.addWidget(self.documents_window)
        self.addWidget(self.documenter_window)
        self.addWidget(self.logging_window)

        self.current_window_start_time = None
        self.current_window_name = None

    def show_window(self, window):
        if self.current_window_name:
            duration = QDateTime.currentDateTime().toSecsSinceEpoch() - self.current_window_start_time.toSecsSinceEpoch()
            self.window_opened.emit(f"Closed {self.current_window_name}, duration: {duration} seconds")

        self.current_window_start_time = QDateTime.currentDateTime()
        if window == HomeWindow:
            self.setCurrentWidget(self.home_window)
            self.current_window_name = "Home"
        elif window == HelpWindow:
            self.setCurrentWidget(self.help_window)
            self.current_window_name = "Help"
        elif window == DocumentsWindow:
            self.setCurrentWidget(self.documents_window)
            self.current_window_name = "Documents"
        elif window == Documenter:
            self.setCurrentWidget(self.documenter_window)
            self.current_window_name = "Documenter"
        elif window == LoggingWindow:
            self.setCurrentWidget(self.logging_window)
            self.current_window_name = "Logs"
        
        self.window_opened.emit(f"Opened {self.current_window_name}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DocMan")
        self.setGeometry(300, 300, 1100, 600)
        self.setFixedWidth(1100)

        self.setup_toolbar()
        self.setup_central_widget()
        self.setup_side_menu()

        self.setup_logging()

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

        self.add_toolbar_button(toolbar, "HOME")
        self.add_toolbar_button(toolbar, "HELP")
        self.add_toolbar_button(toolbar, "LOGGING")

    def add_toolbar_button(self, toolbar, text):
        button = QPushButton(text)
        button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #2c3e50; color: #ecf0f1; border: none;")
        button.clicked.connect(self.handle_toolbar_button_click)
        toolbar.addWidget(button)

    def handle_toolbar_button_click(self):
        sender = self.sender()
        if sender:
            item_name = sender.text()
            self.log_interaction(f"Toolbar button clicked: {item_name}")
            if item_name == "HOME":
                self.show_window(HomeWindow)
            elif item_name == "HELP":
                self.show_window(HelpWindow)
            elif item_name == "LOGGING":
                self.show_window(LoggingWindow)

    def setup_central_widget(self):
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        self.stacked_widget = MainStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        central_frame = QFrame()
        central_frame.setFrameShape(QFrame.Shape.StyledPanel)
        central_frame.setStyleSheet("background-color: #2c3e50; border: 2px solid #34495e;")
        central_frame.setLayout(central_layout)

        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.setContentsMargins(0, 0, 0, 0)
        central_widget_layout.addWidget(central_frame)

        self.setCentralWidget(central_widget)

    def setup_side_menu(self):
        side_menu = SideMenu(self)
        dock = QDockWidget()
        dock.setWidget(side_menu)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    def show_window(self, window):
        self.stacked_widget.show_window(window)

    def setup_logging(self):
        self.logging_window = self.stacked_widget.logging_window
        self.stacked_widget.window_opened.connect(self.log_interaction)

        logging.basicConfig(filename='docman.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log_interaction(self, message):
        self.logging_window.log_interaction(message)
        logging.info(message)

    def log_error(self, message):
        self.logging_window.log_error(message)
        logging.error(message)

    def closeEvent(self, event):
        self.log_interaction("Application closed")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
