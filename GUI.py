import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QMessageBox, QPushButton, QStackedWidget, QSpacerItem, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAPSTONE Project--GROUP D")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.create_initial_screen()

        self.red_team_tools = [
            ["Nmap", "Hydra", "Gobuster"],
            ["Wpscan", "Enum4linux", "Searchsploit"],
            ["Msfvenom", "Curl", "Python3"],
            ["Havoc", "Sherloc", "Osintagram"]
        ]

        self.blue_team_tools = [
            ["Feroxbuster", "Wireshark", "Visual Studio Code"],
            ["Visual Studio", "Bettercap", "Responder"]
        ]

    def create_initial_screen(self):
        initial_widget = QWidget(self)
        initial_layout = QVBoxLayout(initial_widget)

        title_label = QLabel("Choose Your Team", initial_widget)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        initial_layout.addWidget(title_label)

        button_layout = QGridLayout()
        button_layout.setSpacing(20)

        red_button = QPushButton("RED", initial_widget)
        red_button.setStyleSheet("background-color: red; color: white; font-size: 40px; padding: 40px;")
        red_button.setFixedSize(600, 600)
        red_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        red_button.clicked.connect(self.show_red_team_tools)

        blue_button = QPushButton("BLUE", initial_widget)
        blue_button.setStyleSheet("background-color: blue; color: white; font-size: 40px; padding: 40px;")
        blue_button.setFixedSize(600, 600)
        blue_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        blue_button.clicked.connect(self.show_blue_team_tools)

        button_layout.addWidget(red_button, 0, 0, Qt.AlignCenter)
        button_layout.addWidget(blue_button, 0, 1, Qt.AlignCenter)

        initial_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        initial_layout.addLayout(button_layout)
        initial_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        initial_widget.setLayout(initial_layout)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(211, 211, 211))  # Light gray color
        initial_widget.setPalette(palette)
        initial_widget.setAutoFillBackground(True)

        self.stacked_widget.addWidget(initial_widget)
        self.stacked_widget.setCurrentWidget(initial_widget)

    def show_red_team_tools(self):
        self.show_team_tools(self.red_team_tools, "Red Team Tools")

    def show_blue_team_tools(self):
        self.show_team_tools(self.blue_team_tools, "Blue Team Tools")

    def show_team_tools(self, tools, team_label):
        tool_widget = QWidget(self)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(173, 216, 230))
        tool_widget.setPalette(palette)
        tool_widget.setAutoFillBackground(True)

        main_layout = QVBoxLayout(tool_widget)

        header_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)

        team_label_widget = QLabel(team_label, tool_widget)
        team_label_widget.setAlignment(Qt.AlignLeft)
        team_label_widget.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        header_layout.addWidget(team_label_widget)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        header_layout.addSpacerItem(spacer)

        return_button = QPushButton("Return to Choice", tool_widget)
        return_button.setStyleSheet("font-size: 16px; padding: 10px 20px;")
        return_button.setFixedSize(200, 50)
        return_button.clicked.connect(self.return_to_choice)
        header_layout.addWidget(return_button)

        for i, section_labels in enumerate(tools):
            section = self.create_section(f"Section {i + 1}", section_labels)
            main_layout.addWidget(section)

        tool_widget.setLayout(main_layout)
        self.stacked_widget.addWidget(tool_widget)
        self.stacked_widget.setCurrentWidget(tool_widget)

    def return_to_choice(self):
        self.stacked_widget.setCurrentIndex(0)

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
            grid_label.mousePressEvent = self.create_handler(label_text)
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
        program_files = os.getenv("ProgramFiles")
        program = f"{program_files}\\{tool_name}\\{tool_name}"
        program = program.split('\\')
        os.system("start "+program[3])
        time.sleep(1)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
