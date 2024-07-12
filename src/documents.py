import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTreeView, QInputDialog, 
    QMessageBox, QToolBar, QLabel, QSplitter
)
from PyQt6.QtGui import QIcon, QAction, QFileSystemModel, QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QModelIndex


class ToolbarWithDividers(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.darkGray, 1, Qt.PenStyle.SolidLine))
        painter.drawLine(0, 0, 0, self.height())


class DocumentsWindow(QWidget):
    open_document = pyqtSignal(str)  # Signal to indicate opening a document

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.clipboard = []

    def setup_ui(self):
        """Initialize UI components."""
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Set to the root path you want to display
        self.model.setReadOnly(False)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('src/docs'))  # Change to the desired root directory
        self.tree.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeView.DragDropMode.DragDrop)
        self.tree.setDropIndicatorShown(True)
        self.tree.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.tree.doubleClicked.connect(self.handle_double_click)
        self.tree.selectionModel().selectionChanged.connect(self.update_preview)

        self.preview = QLabel("Preview Pane")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.preview.setWordWrap(True)
        self.preview.setFixedWidth(300)  # Adjust as necessary

        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(splitter)

        self.toolbar = ToolbarWithDividers()
        self.toolbar.setIconSize(QSize(16, 16))
        self.setup_actions()
        self.layout.addWidget(self.toolbar, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.layout)

    def setup_actions(self):
        """Setup toolbar actions."""
        actions = [
            ("folder-new", "Create Folder", self.create_folder),
            ("edit-delete", "Delete", self.delete_item),
            ("edit-rename", "Rename", self.rename_item),
            ("document-open", "Open", self.open_item),
            ("document-properties", "Properties", self.show_properties),
            ("go-up", "Go Up", self.go_up),
            ("edit-cut", "Cut", self.cut_item),
            ("edit-copy", "Copy", self.copy_item),
            ("edit-paste", "Paste", self.paste_item),
            ("view-refresh", "Batch Process", self.batch_process),
            ("tag", "Tag Document", self.tag_item)
        ]

        for idx, (icon, text, slot) in enumerate(actions):
            action = QAction(QIcon.fromTheme(icon), text, self)
            action.triggered.connect(slot)
            self.toolbar.addAction(action)
            if idx < len(actions) - 1:
                self.toolbar.addSeparator()

    def handle_double_click(self, index: QModelIndex):
        """Handle double click event on a tree view item."""
        item_path = self.model.filePath(index)
        if os.path.isdir(item_path):
            self.tree.setRootIndex(index)
        else:
            self.open_item()

    def create_folder(self):
        """Create a new folder in the current directory."""
        index = self.tree.currentIndex()
        if not index.isValid():
            index = self.model.index(self.model.rootPath())

        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Folder name:")
        if ok and folder_name:
            parent_path = self.model.filePath(index)
            new_folder_path = os.path.join(parent_path, folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            self.model.refresh(index)

    def delete_item(self):
        """Delete the selected file or folder."""
        indexes = self.tree.selectedIndexes()
        for index in indexes:
            if index.column() == 0:  # We only want to delete each item once
                file_path = self.model.filePath(index)
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                self.model.remove(index)

    def rename_item(self):
        """Rename the selected file or folder."""
        index = self.tree.currentIndex()
        if index.isValid():
            item_path = self.model.filePath(index)
            new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=os.path.basename(item_path))
            if ok and new_name:
                new_path = os.path.join(os.path.dirname(item_path), new_name)
                os.rename(item_path, new_path)
                self.model.refresh(index.parent())

    def open_item(self):
        """Open the selected file."""
        index = self.tree.currentIndex()
        if index.isValid():
            item_path = self.model.filePath(index)
            if os.path.isfile(item_path):
                self.open_document.emit(item_path)

    def show_properties(self):
        """Show properties of the selected file or folder."""
        index = self.tree.currentIndex()
        if index.isValid():
            item_path = self.model.filePath(index)
            properties = f"Name: {os.path.basename(item_path)}\nSize: {os.path.getsize(item_path)} bytes"
            QMessageBox.information(self, "Properties", properties)

    def go_up(self):
        """Navigate to the parent directory."""
        current_root = self.tree.rootIndex()
        if current_root.isValid():
            parent_index = self.model.parent(current_root)
            if parent_index.isValid():
                self.tree.setRootIndex(parent_index)

    def cut_item(self):
        """Cut the selected item."""
        index = self.tree.currentIndex()
        if index.isValid():
            self.clipboard = (self.model.filePath(index), 'cut')

    def copy_item(self):
        """Copy the selected item."""
        index = self.tree.currentIndex()
        if index.isValid():
            self.clipboard = (self.model.filePath(index), 'copy')

    def paste_item(self):
        """Paste the item from the clipboard."""
        index = self.tree.currentIndex()
        if index.isValid() and self.clipboard:
            destination_path = self.model.filePath(index)
            source_path, action = self.clipboard

            if action == 'cut':
                shutil.move(source_path, destination_path)
            elif action == 'copy':
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
                else:
                    shutil.copy(source_path, destination_path)

            self.model.refresh(self.model.index(destination_path))

    def batch_process(self):
        """Batch process selected items."""
        indexes = self.tree.selectedIndexes()
        if not indexes:
            return

        actions = ["Rename", "Delete"]
        action, ok = QInputDialog.getItem(self, "Batch Process", "Select action:", actions, 0, False)
        if ok and action:
            for index in indexes:
                if index.column() == 0:
                    if action == "Rename":
                        self.rename_item()
                    elif action == "Delete":
                        self.delete_item()

    def tag_item(self):
        """Tag the selected item."""
        indexes = self.tree.selectedIndexes()
        if not indexes:
            return

        tag, ok = QInputDialog.getText(self, "Tag Document", "Enter tag:")
        if ok and tag:
            for index in indexes:
                if index.column() == 0:
                    item_path = self.model.filePath(index)

    def update_preview(self):
        """Update the preview pane with the selected item's content."""
        index = self.tree.currentIndex()
        if index.isValid():
            item_path = self.model.filePath(index)
            if os.path.isdir(item_path):
                self.preview.setText("Directory: " + item_path)
            else:
                with open(item_path, 'r') as file:
                    content = file.read(1024)  # Read the first 1024 bytes
                    self.preview.setText(content)
