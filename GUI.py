import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAPSTONE Project--GROUP D")
        self.setGeometry(100, 100, 800, 600)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(173, 216, 230))  
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

        main_layout = QVBoxLayout(widget)

        sections = [
            ["Nmap", "Hydra", "Gobuster"],
            ["Wpscan", "Enum4linux", "Searchsploit"],
            ["Msfvenom", "Curl", "Python3"],
            ["Havoc", "Sherloc", "Osintagram"],
            ["Feroxbuster", "Wireshark", "Visual Studio Code"],
            ["Visual Studio", "Bettercap", "Responder"]
        ]

        for i, section_labels in enumerate(sections):
            section = self.create_section(f"Section {i + 1}", section_labels)
            main_layout.addWidget(section)

    def create_section(self, title, labels):
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        
        title_label = QLabel(title, section_widget)
        section_layout.addWidget(title_label)
        
        grid_layout = QGridLayout()
        section_layout.addLayout(grid_layout)

        for index, label_text in enumerate(labels):
            row = index // 4
            col = index % 4
            grid_label = QLabel(label_text, section_widget)
            grid_label.setAlignment(Qt.AlignCenter)
            grid_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_label.setStyleSheet("border: 1px solid black; background-color: white;")
            grid_label.mousePressEvent = self.create_click_handler(label_text)
            grid_layout.addWidget(grid_label, row, col)
        
        for index in range(len(labels), 3):
            row = index // 4
            col = index % 4
            grid_label = QLabel("", section_widget)
            grid_label.setAlignment(Qt.AlignCenter)
            grid_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_label.setStyleSheet("border: 1px solid black; background-color: white;")
            grid_layout.addWidget(grid_label, row, col)

        return section_widget

    def create_handler(self, label_text):
        def handler(event):
            self.show_tool_options(label_text)
        return handler

    def show_tool_options(self, tool_name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(f"{tool_name} Options")
        msg.setText(f"Options for {tool_name}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
