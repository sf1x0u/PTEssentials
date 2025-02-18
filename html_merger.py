import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

def merge_html_files(file_paths):
    merged_content = ""
    
    # Process each file and extract the content
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            
            # Assume the files have a structure like <html>...</html>
            # We want to merge only the body content
            start_body = file_content.find('<body>')
            end_body = file_content.find('</body>') + len('</body>')
            
            if start_body != -1 and end_body != -1:
                body_content = file_content[start_body:end_body]
                merged_content += body_content
            else:
                merged_content += file_content  # If no <body> tag, just append full file content
    
    return merged_content

class HtmlMergerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Merger Tool")
        self.setGeometry(100, 100, 400, 300)

        # Set the background color to light yellow
        self.setStyleSheet("background-color: lightyellow;")

        # Layout
        layout = QVBoxLayout()

        # Label to show selected files
        self.selected_files_label = QLabel("No files selected", self)
        self.selected_files_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.selected_files_label)

        # Merge button
        merge_button = QPushButton("Merge HTML Files", self)
        merge_button.setStyleSheet("background-color: lightblue;")
        merge_button.clicked.connect(self.on_merge_button_click)
        layout.addWidget(merge_button)

        # Signature label
        signature_label = QLabel("Github: sf1x0u", self)
        signature_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(signature_label)

        self.setLayout(layout)

    def on_merge_button_click(self):
        # Ask user to select multiple HTML files
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select HTML files to merge", "", "HTML files (*.html)")

        if file_paths:
            # Show the selected files on screen
            self.selected_files_label.setText("Selected Files:\n" + "\n".join(file_paths))
            
            # Merge the files and get the resulting content
            merged_content = merge_html_files(file_paths)
            
            # Save the merged content to a file
            self.save_merged_file(merged_content)
        else:
            QMessageBox.warning(self, "Error", "No files selected.")

    def save_merged_file(self, merged_content):
        # Ask the user to choose the output file path
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Merged File", "", "HTML files (*.html)")

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(merged_content)
            QMessageBox.information(self, "Success", "Merged file saved successfully!")
            QMessageBox.information(self, "Done", "Merging Completed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HtmlMergerApp()
    window.show()
    sys.exit(app.exec_())
