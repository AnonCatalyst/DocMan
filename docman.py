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
        self.logo_description = QLabel(" DOCMAN MENU ")
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
        self.button_description = QLabel("""DocMan was developed during
the 2024 v5 BackDropBuild
session (July 8 - August
3, 2024) to enhance OSINT
investigations. This four
-week program provided fu
nding and support for inn
ovative solutions. DocMan
was created to meet the 
specific needs of OSINT 
professionals, offering a
robust document managemen
t system. The development
focused on modern softwar
e practices, modular arch
itecture, and user-centri
c design to improve workf
lows and data management.""")
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

        self.home_window = HomeWindow()
        self.help_window = HelpWindow()
        self.documents_window = DocumentsWindow()
        self.documenter_window = DocumenterWindow()

        self.addWidget(self.home_window)
        self.addWidget(self.help_window)
        self.addWidget(self.documents_window)
        self.addWidget(self.documenter_window)

    def show_window(self, window):
        if window == HomeWindow:
            self.setCurrentWidget(self.home_window)
        elif window == HelpWindow:
            self.setCurrentWidget(self.help_window)
        elif window == DocumentsWindow:
            self.setCurrentWidget(self.documents_window)
        elif window == DocumenterWindow:
            self.setCurrentWidget(self.documenter_window)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DocMan")
        self.setGeometry(300, 300, 1100, 600)
        self.setFixedWidth(1100)  # Set a fixed width

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
        button.clicked.connect(self.handle_toolbar_button_click)
        toolbar.addWidget(button)

    def handle_toolbar_button_click(self):
        sender = self.sender()  # Get the button that triggered the signal
        if sender:
            item_name = sender.text()
            if item_name == "Home":
                self.show_window(HomeWindow)
            elif item_name == "Help":
                self.show_window(HelpWindow)

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

class HomeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        welcome_label = QLabel("Welcome to DocMan!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #ecf0f1; font-size: 20px;")
        layout.addWidget(welcome_label)

        description_label = QLabel("DocMan is designed to streamline OSINT documentation tasks and enhance your workflow.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(description_label)
        layout.addStretch()

class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        help_label = QLabel("How DocMan Helps:")
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_label.setStyleSheet("color: #ecf0f1; font-size: 20px;")
        layout.addWidget(help_label)

        help_description = QLabel("""DocMan speeds up OSINT documentation tasks by providing a robust document management system. 
Developed in anticipation of the July 8th-August 3rd BackDropBuild v5 Session, DocMan offers several key features:
> https://backdropbuild.com/builds/v5/osint-document-manager
        
1. **Document Organization:** Easily manage and organize large volumes of documents, ensuring that important- 
 information is always at your fingertips.
2. **Efficient Data Handling:** Streamline data handling processes to reduce time spent on administrative- 
 tasks and increase time available for analysis.
3. **User-Friendly Interface:** Benefit from a user-friendly interface that simplifies navigation and improves overall user experience.
4. **GitHub Repository:** For more details, visit the DocMan repository on GitHub by AnonCatalyst.

DocMan is designed to enhance efficiency in managing large amounts of data, making it an invaluable tool for OSINT investigations. 
Explore the full potential of DocMan to streamline your workflow and improve investigative outcomes.""")
       
        help_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_description.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(help_description)
        layout.addStretch()

def main():
    app = QApplication(sys.argv)
    global main_window
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
