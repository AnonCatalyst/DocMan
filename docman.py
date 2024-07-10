from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QVBoxLayout, QWidget, 
    QPushButton, QDockWidget, QFrame, QStackedWidget, QTextBrowser
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices
import os
import sys

# Import custom windows
from src.documents import DocumentsWindow
from src.documenter import Documenter


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
        """Sets up the logo and description under it."""
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
        """Creates and styles menu buttons."""
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
        """Adds the description label."""
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
        """Loads logo image asynchronously."""
        file_path = os.path.join('src', 'assets', 'icons', 'side_logo.png')
        self.image_loader = ImageLoader(file_path)
        self.image_loader.image_loaded.connect(self.update_logo)
        self.image_loader.finished.connect(self.cleanup_thread)
        self.image_loader.start()

    def update_logo(self, pixmap):
        """Updates the logo label with the loaded pixmap."""
        self.logo_label.setPixmap(pixmap.scaledToWidth(100))

    def cleanup_thread(self):
        """Cleans up the image loader thread."""
        if self.image_loader is not None:
            self.image_loader.quit()
            self.image_loader.wait()
            self.image_loader.deleteLater()
            self.image_loader = None

    def handle_menu_item_click(self):
        """Handles menu item clicks to switch windows."""
        sender = self.sender()
        if sender:
            item_name = sender.objectName()
            if item_name == "DOCUMENTS":
                self.parent.show_window(DocumentsWindow)
            elif item_name == "DOCUMENTER":
                self.parent.show_window(Documenter)

    def closeEvent(self, event):
        self.cleanup_thread()
        event.accept()


class MainStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.home_window = HomeWindow()
        self.help_window = HelpWindow()
        self.documents_window = DocumentsWindow()
        self.documenter_window = Documenter()

        self.addWidget(self.home_window)
        self.addWidget(self.help_window)
        self.addWidget(self.documents_window)
        self.addWidget(self.documenter_window)

    def show_window(self, window):
        """Shows the specified window."""
        if window == HomeWindow:
            self.setCurrentWidget(self.home_window)
        elif window == HelpWindow:
            self.setCurrentWidget(self.help_window)
        elif window == DocumentsWindow:
            self.setCurrentWidget(self.documents_window)
        elif window == Documenter:
            self.setCurrentWidget(self.documenter_window)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DocMan")
        self.setGeometry(300, 300, 1100, 600)
        self.setFixedWidth(1100)

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

        self.add_toolbar_button(toolbar, "HOME")
        self.add_toolbar_button(toolbar, "HELP")

    def add_toolbar_button(self, toolbar, text):
        """Adds a button to the toolbar."""
        button = QPushButton(text)
        button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #2c3e50; color: #ecf0f1; border: none;")
        button.clicked.connect(self.handle_toolbar_button_click)
        toolbar.addWidget(button)

    def handle_toolbar_button_click(self):
        """Handles toolbar button clicks to switch windows."""
        sender = self.sender()
        if sender:
            item_name = sender.text()
            if item_name == "HOME":
                self.show_window(HomeWindow)
            elif item_name == "HELP":
                self.show_window(HelpWindow)

    def setup_central_widget(self):
        """Sets up the central widget with a stacked layout."""
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
        """Sets up the side menu dock widget."""
        dock_widget = QDockWidget(self)
        dock_widget.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        self.side_menu = SideMenu(self)
        self.side_menu.setStyleSheet("QDockWidget { border: none; }")

        dock_widget.setFeatures(dock_widget.features() & ~QDockWidget.DockWidgetFeature.DockWidgetClosable)
        dock_widget.setWidget(self.side_menu)
        dock_widget.setMinimumWidth(150)
        dock_widget.setMaximumWidth(150)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)

    def show_window(self, window_class):
        """Shows the specified window in the stacked widget."""
        self.stacked_widget.show_window(window_class)


class HomeWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        welcome_label = QLabel("Welcome to DocMan!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #ecf0f1; font-size: 20px;")
        layout.addWidget(welcome_label)

        description_label = QLabel("""DocMan is designed to streamline OSINT documentation tasks.
DocMan helps speed up OSINT documentation tasks by providing a user-friendly interface 
and efficient management of documents and related data. This tool is developed as part 
of the BackDropBuild v5 session and aims to improve workflow in OSINT investigations.""")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(description_label)


class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("DocMan Help")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Welcome to DocMan Help")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ecf0f1;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Help text
        help_text = """
        <p>New to DocMan? Here’s how to get started:</p>
        <ul style="margin-left: 20px;">
            <li>Explore documentation and document management options using the side menu.</li>
            <li>Visit the HOME window to learn more about DocMan's features.</li>
            <li>For support or bug reports, return to this section.</li>
            <li>Manage your documents under the "DOCUMENTS" option in the side menu. This feature helps 
                speed up your OSINT workflow by organizing and accessing critical information efficiently.</li>
            <li>Create single or multiple documentation files using the "DOCUMENTER" option in the side menu. 
                This tool is a dream for OSINT professionals, enabling them to streamline their investigative process 
                by quickly generating detailed documentation.</li>
        </ul>
        
        <p>Support or Report bugs?</p>
        <ul style="list-style-type: none; margin-left: 20px;">
            <li>Email: hard2find.co.01@gmail.com</li>
            <li>Instagram: @istoleyourbutter</li>
            <li>Github: AnonCatalyst</li>
            <li>Discord: 6TFBKgjaAz</li>
        </ul>
        """

        help_browser = QTextBrowser()
        help_browser.setHtml(help_text)
        help_browser.setStyleSheet("color: #bdc3c7; font-size: 14px; font-family: Arial, sans-serif; background-color: #34495e;")
        help_browser.setReadOnly(True)  # Ensure the text is read-only
        
        layout.addWidget(help_browser)
        
        self.setStyleSheet("background-color: #2c3e50;")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
