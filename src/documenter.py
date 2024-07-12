from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLineEdit,
    QMessageBox, QTabWidget, QHBoxLayout, QFileDialog, QStatusBar, QMenu
)
from PyQt6.QtCore import pyqtSignal, Qt


class Documenter(QWidget):
    open_document = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Add buttons layout
        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        # Add buttons: Add Document, Delete Document, Save All, Save Individual, Open File
        self.add_tab_button = QPushButton("Add Document")
        self.add_tab_button.clicked.connect(self.add_document_tab)
        self.buttons_layout.addWidget(self.add_tab_button)

        self.delete_tab_button = QPushButton("Delete Document")
        self.delete_tab_button.clicked.connect(self.delete_current_tab)
        self.buttons_layout.addWidget(self.delete_tab_button)

        self.save_all_button = QPushButton("Save All")
        self.save_all_button.clicked.connect(self.save_documents)
        self.buttons_layout.addWidget(self.save_all_button)

        self.save_individual_button = QPushButton("Save File")
        self.save_individual_button.clicked.connect(self.save_individual_documents)
        self.buttons_layout.addWidget(self.save_individual_button)

        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file_dialog)
        self.buttons_layout.addWidget(self.open_button)

        # Add Status Bar
        self.status_bar = QStatusBar()
        self.layout.addWidget(self.status_bar)

        # Initialize with one document tab
        self.add_document_tab()

        self.setLayout(self.layout)

        # List to keep track of file threads (if applicable)
        self.file_threads = []

        # Connect tab context menu
        self.tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_widget.customContextMenuRequested.connect(self.show_tab_context_menu)

    def add_document_tab(self):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        text_edit = QTextEdit()
        tab_layout.addWidget(text_edit)

        file_widget_layout = QVBoxLayout()
        tab_layout.addLayout(file_widget_layout)

        file_type_combo = QComboBox()
        file_type_combo.addItems(["doc", "txt", "md", "pdf", "html"])  # Added more file formats
        file_widget_layout.addWidget(file_type_combo)

        file_name_input = QLineEdit()
        file_name_input.setPlaceholderText("Enter file name...")
        file_widget_layout.addWidget(file_name_input)

        self.tab_widget.addTab(tab, f"Document {self.tab_widget.count()}")
        self.tab_widget.setCurrentWidget(tab)

    def delete_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

    def save_documents(self):
        docs_directory = "src/docs"
        if not os.path.exists(docs_directory):
            os.makedirs(docs_directory)

        for i in range(self.tab_widget.count()):
            tab_widget = self.tab_widget.widget(i)
            text_edit = tab_widget.findChild(QTextEdit)
            file_type_combo = tab_widget.findChild(QComboBox)
            file_name_input = tab_widget.findChild(QLineEdit)

            content = text_edit.toPlainText()
            file_type = file_type_combo.currentText()
            file_name = file_name_input.text()

            if not file_name:
                QMessageBox.warning(self, "Warning", "Please enter a file name for all documents.")
                return

            if content:
                file_path = os.path.join(docs_directory, f"{file_name}.{file_type.lower()}")
                try:
                    with open(file_path, "w") as file:
                        file.write(content)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file {file_path}: {e}")
                    return

        QMessageBox.information(self, "Success", "Documents saved successfully.")

    def save_individual_documents(self):
        docs_directory = "src/docs"
        if not os.path.exists(docs_directory):
            os.makedirs(docs_directory)

        for i in range(self.tab_widget.count()):
            tab_widget = self.tab_widget.widget(i)
            text_edit = tab_widget.findChild(QTextEdit)
            file_type_combo = tab_widget.findChild(QComboBox)
            file_name_input = tab_widget.findChild(QLineEdit)

            content = text_edit.toPlainText()
            file_type = file_type_combo.currentText()
            file_name = file_name_input.text()

            if not file_name:
                continue

            if content:
                file_path = os.path.join(docs_directory, f"{file_name}.{file_type.lower()}")
                try:
                    with open(file_path, "w") as file:
                        file.write(content)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file {file_path}: {e}")
                    return

        QMessageBox.information(self, "Success", "Individual documents saved successfully.")

    def open_file_dialog(self):
        docs_directory = "src/docs"
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", docs_directory)
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            file_name = os.path.basename(file_path)
            file_name = os.path.splitext(file_name)[0]

            text_edit = QTextEdit()
            text_edit.setPlainText(content)
            self.tab_widget.addTab(text_edit, file_name)
            self.tab_widget.setCurrentWidget(text_edit.parentWidget())

            self.status_bar.showMessage(f"File '{file_name}' loaded successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file {file_path}: {e}")

    def show_tab_context_menu(self, position):
        tab_index = self.tab_widget.tabBar().tabAt(position)
        if tab_index >= 0:
            menu = QMenu()
            save_action = QAction("Save", self)
            save_action.triggered.connect(lambda: self.save_tab_content(tab_index))
            menu.addAction(save_action)

            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.rename_tab(tab_index))
            menu.addAction(rename_action)

            menu.exec(self.tab_widget.tabBar().mapToGlobal(position))

    def save_tab_content(self, tab_index):
        tab_widget = self.tab_widget.widget(tab_index)
        text_edit = tab_widget.findChild(QTextEdit)
        file_type_combo = tab_widget.findChild(QComboBox)
        file_name_input = tab_widget.findChild(QLineEdit)

        content = text_edit.toPlainText()
        file_type = file_type_combo.currentText()
        file_name = file_name_input.text()

        if not file_name:
            QMessageBox.warning(self, "Warning", "Please enter a file name for this document.")
            return

        if content:
            docs_directory = "src/docs"
            if not os.path.exists(docs_directory):
                os.makedirs(docs_directory)

            file_path = os.path.join(docs_directory, f"{file_name}.{file_type.lower()}")
            try:
                with open(file_path, "w") as file:
                    file.write(content)
                QMessageBox.information(self, "Success", f"Document '{file_name}' saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file {file_path}: {e}")

    def rename_tab(self, tab_index):
        tab_widget = self.tab_widget.widget(tab_index)
        current_tab_text = self.tab_widget.tabText(tab_index)
        new_tab_text, ok_pressed = QInputDialog.getText(self, "Rename Document", "Enter new name:", text=current_tab_text)
        if ok_pressed and new_tab_text:
            self.tab_widget.setTabText(tab_index, new_tab_text)
            self.status_bar.showMessage(f"Document renamed to '{new_tab_text}'.")

    def clear_all_tabs(self):
        self.tab_widget.clear()

