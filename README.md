# DocMan: OSINT Document Manager

DocMan is a document management system designed to streamline workflows and improve efficiency in OSINT investigations. Developed as a result of participation in the BackDropBuild v5 session from July 8th to August 3rd, DocMan provides a centralized interface for managing, editing, and organizing documents, facilitating collaboration and enhancing productivity.

<img src="src/img/screenshot.png" alt="DocMan: Document Manager (GUI) - screenshot" width="700" height="400"/>

# TO-DO
- `Add an icon for DocMan`
- `Fix issue with unable to create or open folders`
- `Fix issue where there is no visual indicator of what files have been tagged`
- `Fix issue with not being able to batch process delete all tagged folders or files`

### DocMan: Documents & Documenter Window Update

- 1. Enhanced UI: `Introduced QSplitter for Tree View and Preview Pane organization, alongside a custom ToolbarWithDividers for visual clarity.`
- 2. Actions Integrated: `Implemented Create Folder, Delete, Rename, Open, Properties, Go Up, Cut, Copy, Paste, Batch Process, and Tag Document functionalities.`
- 3. File System Management: `Leveraged QFileSystemModel for robust file system handling with read/write support.`
- 4. Enhanced Interaction: `Enabled context menu and drag-drop capabilities in QTreeView, enhancing user interaction.`
- 5. Preview Pane: `Dynamically updates to display selected file content, improving usability.`
- 6. Clipboard Support: `Integrated cut, copy, and paste operations within the application for seamless file management.`
- 7. Batch Processing: `Added support for renaming or deleting multiple files simultaneously, enhancing efficiency.`
- 8. Custom Signal: `Introduced `open_document` signal for efficient handling of document opening events.`
- 9. File Format `Support: Expanded file type support (doc, txt, md, pdf, html) in the file type combo box (`file_type_combo`).`
- 10. Document Management: `Implemented dynamic tab management for adding, deleting, saving all documents, saving individual documents, and opening files.`
- 11. Context Menu for Tabs: `Introduced context menu functionality for tabs in the tab widget (`tab_widget`), enabling actions like saving and renaming.`
- 12. `File Operations: Methods added for saving all documents (`save_documents`), saving individual documents (`save_individual_documents`), and opening files (`open_file_dialog`) with error handling and status bar feedback.`
- 13. `Document Loading and Editing: Implemented file loading into tabs (`load_file`) and content editing using `QTextEdit`.`
- 14. `UI and Layout: Enhanced UI with tab management (`tab_widget`) using `QVBoxLayout` and `QHBoxLayout`, supported by a status bar (`status_bar`) for feedback.`
- 15. `Tab Management: Methods (`add_document_tab`, `delete_current_tab`, `rename_tab`, `clear_all_tabs`) added for efficient tab management.`
- 16. `Signal Handling: Utilizes signals (`open_document`) for inter-widget communication and context menu actions (`show_tab_context_menu`).`
- 17. `File Thread Management: Introduced `file_threads` list for managing concurrent file operations.`

## BackDropBuild v5 Session

BackDropBuild v5 is a collaborative session focused on developing tools and solutions for enhancing OSINT capabilities. Held from July 8th to August 3rd, the session aims to address challenges in open-source intelligence gathering by fostering innovation and collaboration among participants.

Learn more about [BackDropBuild](https://backdropbuild.com).

Explore the specific build session for DocMan at [BackDropBuild v5 - OSINT Document Manager](https://backdropbuild.com/builds/v5/osint-document-manager).

## What is BackDropBuild?

BackDropBuild is an initiative that brings together experts and enthusiasts in various fields to collaborate on developing innovative tools and solutions for specific challenges. It provides a platform for intensive sessions, such as v5, which focuses on advancing OSINT capabilities through creative and collaborative efforts.

## Why DocMan?

DocMan stands out as a dedicated tool tailored specifically to speed up OSINT documentation workflows. Each feature in DocMan contributes to this goal:

- **Centralized Document Repository:** Provides quick access to all documents related to an investigation, reducing time spent searching for information.
  
- **Document Templates:** Standardizes reporting formats, saving time on formatting and ensuring consistency in documentation.
  
- **Version Control and Collaboration Tools:** Facilitates real-time collaboration among team members, enhancing efficiency in document review and updates.
  
- **Integrated Editor:** Offers formatting and styling options directly within the application, eliminating the need to switch between tools for document editing.
  
- **Real-Time Collaboration and Commenting:** Enables instant feedback and discussion on documents, speeding up the review process.
  
- **Customizable Dashboard:** Tailors the interface to individual workflow preferences, optimizing user interaction and task management.
  
- **Role-Based Access Control:** Ensures secure and controlled access to sensitive information, maintaining data integrity and compliance.

By focusing on these specific needs of OSINT practitioners, DocMan enhances workflow efficiency, accuracy, and collaboration in document management, making it an indispensable tool for accelerating investigative processes.

# INSTALL & RUN!
- `git clone https://github.com/AnonCatalyst/DocMan && cd DocMan`
- `pip install -r requirements.txt --break-system-packages`
- `python3 docman.py`
