from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QPushButton, QInputDialog, QMessageBox, QToolBar, QApplication
from PyQt6.QtGui import QFileSystemModel, QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QMimeData
import os
import shutil

class DocumentsWindow(QWidget):
    open_document = pyqtSignal(str)  # Signal to indicate opening a document

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize the file system model
        self.model = QFileSystemModel()
        self.model.setRootPath('src/docs')  # Root path for the file manager
        
        # Initialize the tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('src/docs'))
        self.tree.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        # Enable drag and drop
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeView.DragDropMode.InternalMove)

        # Set text wrap mode 
        self.tree.setTextElideMode(Qt.TextElideMode.ElideNone)

        # Connect double click event to slot
        self.tree.doubleClicked.connect(self.handle_double_click)

        # Add the tree view to the layout
        self.layout.addWidget(self.tree)

        # Initialize toolbar
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))

        # Create and add buttons to the toolbar
        self.create_folder_button = QPushButton(QIcon.fromTheme("folder-new"), "Create Folder")
        self.create_folder_button.clicked.connect(self.create_folder)
        self.toolbar.addWidget(self.create_folder_button)

        self.delete_button = QPushButton(QIcon.fromTheme("edit-delete"), "Delete")
        self.delete_button.clicked.connect(self.delete_item)
        self.toolbar.addWidget(self.delete_button)

        self.rename_button = QPushButton(QIcon.fromTheme("edit-rename"), "Rename")
        self.rename_button.clicked.connect(self.rename_item)
        self.toolbar.addWidget(self.rename_button)

        self.open_button = QPushButton(QIcon.fromTheme("document-open"), "Open")
        self.open_button.clicked.connect(self.open_item)  # Connect to open_item method
        self.toolbar.addWidget(self.open_button)

        self.properties_button = QPushButton(QIcon.fromTheme("document-properties"), "Properties")
        self.properties_button.clicked.connect(self.show_properties)
        self.toolbar.addWidget(self.properties_button)

        # Add "Go Up" button to navigate to parent directory
        self.go_up_button = QPushButton(QIcon.fromTheme("go-up"), "Go Up")
        self.go_up_button.clicked.connect(self.go_up)
        self.toolbar.addWidget(self.go_up_button)

        # Add the toolbar to the layout
        self.layout.addWidget(self.toolbar)

        # Set layout
        self.setLayout(self.layout)

    def handle_double_click(self, index):
        if not index.isValid():
            return

        if self.model.isDir(index):
            self.tree.setRootIndex(index)
        else:
            self.open_item()

    def create_folder(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            index = self.model.index('src/docs')

        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Folder name:")
        if ok and folder_name:
            # Get the path of the current index
            current_path = self.model.filePath(index)
            if not current_path:
                current_path = self.model.rootPath()

            # If the current path points to a file, use its directory as parent
            if os.path.isfile(current_path):
                current_path = os.path.dirname(current_path)

            # Append the new folder name to the current path
            new_folder_path = os.path.join(current_path, folder_name)

            # Check if the parent directory exists and is a directory
            parent_path = os.path.dirname(new_folder_path)
            if not os.path.isdir(parent_path):
                QMessageBox.warning(self, "Error", "Parent directory does not exist or is not a directory.")
                return

            # Check if the folder already exists
            if os.path.exists(new_folder_path):
                QMessageBox.warning(self, "Error", "Folder already exists.")
                return

            # Attempt to create the directory
            try:
                os.makedirs(new_folder_path)
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Failed to create the folder: {e}")
                return

            # Update the model and UI after creating the folder
            self.model.layoutAboutToBeChanged.emit()
            self.model.setRootPath(self.model.rootPath())
            self.model.layoutChanged.emit()

            # Navigate to parent directory
            parent_index = self.model.index(os.path.dirname(new_folder_path))
            self.tree.setRootIndex(parent_index)

    def delete_item(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        confirmation = QMessageBox.question(self, "Delete", f"Are you sure you want to delete '{file_path}'?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            if self.model.isDir(index):
                self.model.rmdir(index)
            else:
                self.model.remove(index)

    def rename_item(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        old_file_path = self.model.filePath(index)
        old_file_name = self.model.fileName(index)

        new_file_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=old_file_name)
        if ok and new_file_name and new_file_name != old_file_name:
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
            if os.path.exists(new_file_path):
                QMessageBox.warning(self, "Error", "A file with the same name already exists.")
                return

            try:
                os.rename(old_file_path, new_file_path)
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Failed to rename the file: {e}")
                return

            # Update the model and UI after renaming
            self.model.layoutAboutToBeChanged.emit()
            self.model.setRootPath(self.model.rootPath())
            self.model.layoutChanged.emit()

            # Update properties display if the renamed file is currently selected
            selected_index = self.tree.currentIndex()
            if selected_index.isValid() and selected_index == index:
                self.show_properties()

            QMessageBox.information(self, "Rename", f"File '{old_file_name}' renamed to '{new_file_name}'.")

    def open_item(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        if not self.model.isDir(index):
            self.open_document.emit(file_path)  # Emit signal to open the document

    def show_properties(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        properties = f"Name: {self.model.fileName(index)}\n"
        properties += f"Path: {file_path}\n"
        properties += f"Size: {self.model.size(index)} bytes\n"
        properties += f"Modified: {self.model.lastModified(index).toString(Qt.DateFormat.ISODate)}"

        QMessageBox.information(self, "Properties", properties)

    def go_up(self):
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        parent_index = self.model.parent(index)
        if parent_index.isValid():
            self.tree.setRootIndex(parent_index)

    def drop_event(self, event):
        drop_action = event.dropAction()
        drop_index = self.tree.indexAt(event.pos())
        if not drop_index.isValid():
            return

        drop_path = self.model.filePath(drop_index)

        mime_data = event.mimeData()
        if mime_data.hasUrls():
            for url in mime_data.urls():
                source_path = url.toLocalFile()
                if os.path.isdir(source_path):
                    # Dragged item is a directory, copy or move it
                    if drop_action == Qt.DropAction.CopyAction:
                        shutil.copytree(source_path, os.path.join(drop_path, os.path.basename(source_path)))
                    elif drop_action == Qt.DropAction.MoveAction:
                        shutil.move(source_path, os.path.join(drop_path, os.path.basename(source_path)))
                else:
                    # Dragged item is a file, copy or move it
                    if drop_action == Qt.DropAction.CopyAction:
                        shutil.copy(source_path, drop_path)
                    elif drop_action == Qt.DropAction.MoveAction:
                        shutil.move(source_path, drop_path)

        event.acceptProposedAction()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
