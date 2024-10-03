from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
import hashlib, sys, re

# Style of drag and drop area
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop File Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class FileHashChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Set up the main window properties
        self.setWindowTitle("SHA256 Checker")
        self.resize(400, 400)
        self.setAcceptDrops(True)
        
        # Label to indicate drag and drop area
        self.photoViewer = ImageLabel()
        
        # Label to show the calculated SHA256
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        font_metrics = self.label.fontMetrics()
        label_height = font_metrics.height() + 10 
        self.label.setFixedHeight(label_height)
        self.label.setStyleSheet("border: 1px solid black;") 
        
        # Label to show the copied SHA256
        self.label2 = QLabel("Select correct SHA")
        self.label2.setAlignment(Qt.AlignCenter)
        font_metrics2 = self.label2.fontMetrics()
        label_height2 = font_metrics2.height() + 10 
        self.label2.setFixedHeight(label_height2)
        self.label2.setStyleSheet("border: 1px solid black; background-color: white") 
        
        # Button to paste the correct SHA256 from clipboard
        self.button = QPushButton('Paste from Clipboard', self)
        self.button.clicked.connect(self.paste_from_clipboard)
        
        # Button to open a file dialog for selecting a file
        self.btn = QPushButton('Select File', self)
        self.btn.clicked.connect(self.openFileDialog)
        
        # Create and configure the layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.label2)
        mainLayout.addWidget(self.button)
        mainLayout.addWidget(self.photoViewer)
        mainLayout.addWidget(self.btn)
        
        # Set the layout to the main window
        self.setLayout(mainLayout)
    
    def dragEnterEvent(self, event):
        # Accept drag event if it contains file URLs
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Handle file drop event
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.photoViewer.setText(file_path)
                self.hash_checker(file_path)
        else:
            event.ignore()
    
    def openFileDialog(self):
        # Open a file dialog to select a file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if file_path:
            self.photoViewer.setText(file_path)
            self.hash_checker(file_path)
    
    def hash_checker(self, path):
        # Compare with a precomputed hash
        result = self.get_file_checksum(path)
        self.label.setText(result)
        if result == self.label2.text():
            self.label.setStyleSheet("border: 1px solid black; background-color: lightgreen")
        else:
            self.label.setStyleSheet("border: 1px solid black; background-color: red; color: white")
    
    def get_file_checksum(self, filename):
        # Calculate the SHA256 hash of the file
        with open(filename, 'rb') as f:
            contents = f.read()
            sha256 = hashlib.sha256()
            sha256.update(contents)
            return sha256.hexdigest()
    
    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        if self.is_valid_sha256(clipboard_text):
            self.label2.setText(clipboard_text)
            self.hash_checker(self.photoViewer.text())
        else:
            self.label2.setText("Invalid!")
    
    def is_valid_sha256(self, hash_string):
        # Check if the string is exactly 64 characters long and contains only hexadecimal characters
        if re.fullmatch(r'[A-Fa-f0-9]{64}', hash_string): 
            return True
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FileHashChecker()
    ex.show()
    sys.exit(app.exec_())
