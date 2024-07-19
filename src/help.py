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
            <p>DocMan is designed to streamline OSINT documentation tasks by providing a user-friendly interface and efficient management of documents and related data. This tool is developed as part of the BackDropBuild v5 session and aims to improve workflow in OSINT investigations.</p>

            <h3>Getting Started</h3>
            <p>To get started with DocMan, simply select a document from the file manager and start editing. You can create new folders, rename items, and manage your files with ease. For more detailed instructions, please refer to the <a href="https://github.com/AnonCatalyst/DocMan">DocMan GitHub repository</a>.</p>
        
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
""")
        layout.addWidget(help_content)
