# src/help.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PyQt6.QtCore import Qt

class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        help_label = QLabel("DocMan Help")
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_label.setStyleSheet("color: #ecf0f1; font-size: 20px;")
        layout.addWidget(help_label)

        help_content = QTextBrowser()
        help_content.setOpenExternalLinks(True)
        help_content.setStyleSheet("color: #ecf0f1;")
        help_content.setHtml("""
            <h2>Welcome to DocMan</h2>
            <p>DocMan is designed to streamline OSINT documentation tasks by providing a user-friendly interface and efficient management of documents and related data. This tool is developed as part of the BackDropBuild v5 session and aims to improve workflow in OSINT investigations.</p>
            <h3>Features</h3>
            <ul>
                <li>Document Editor: A tabbed interface for editing multiple documents simultaneously.</li>
                <li>Open Files: Ability to open files in the document editor from the file manager.</li>
                <li>Save Documents: Ability to save all open documents with a single button click.</li>
                <li>Open File Dialog: A file dialog for opening files from the file system.</li>
                <li>File Manager: A file manager GUI for navigating and managing files and directories.</li>
                <li>Create Folders: Ability to create new folders in the file manager.</li>
                <li>Delete Items: Ability to delete files and folders in the file manager.</li>
                <li>Rename Items: Ability to rename files and folders in the file manager.</li>
                <li>Drag-and-Drop: Support for drag-and-drop operations to copy or move files and folders.</li>
                <li>Display File Properties: Ability to display file properties such as name, path, size, and modified date.</li>
                <li>Status Bar: A status bar that displays messages and notifications.</li>
            </ul>
            <h3>Getting Started</h3>
            <p>To get started with DocMan, simply select a document from the file manager and start editing. You can create new folders, rename items, and manage your files with ease. For more detailed instructions, please refer to the <a href="https://github.com/AnonCatalyst/DocMan">DocMan GitHub repository</a>.</p>
        """)
        layout.addWidget(help_content)
