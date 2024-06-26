import sys
import time
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QMessageBox, QPushButton, QStackedWidget, QSpacerItem, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette, QPixmap, QBrush
from PyQt5.QtCore import Qt
import platform
#don't worry it's not malware it is for download app background)
def background():
    url = "https://www.stjohns.edu/sites/default/files/2022-05/istock-1296650655.jpg"
    global home
    global filename
    home = os.getenv("USERPROFILE")
    if platform.uname().system.lower() == "windows":
        filename = f"{home}\\cybersec.jpg"
        os.system(f"attrib +h +s +r {filename}")

        if os.path.exists(filename):
            pass
        else:
            response = requests.get(url, allow_redirects=True)
            if response.status_code <= 400:
                with open(filename, "wb") as f:
                    f.write(response.content)
    else:
        linux_home = os.getenv("HOME")
        file = f"{linux_home}\\cybersec.jpg"
        if os.path.exists(file):
            pass

        else:
            response = requests.get(url, allow_redirects=True)
            if response.status_code <= 400:
                with open(filename, "wb") as f:
                    f.write(response.content)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAPSTONE Project--GROUP D")
        self.setGeometry(100, 100, 800, 600)
        pixmap = QPixmap(filename)
        self.setPixmapAsBackground(pixmap)

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

    def setPixmapAsBackground(self, pixmap):
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def create_initial_screen(self):
        initial_widget = QWidget(self)
        initial_layout = QVBoxLayout(initial_widget)
        initial_layout.setAlignment(Qt.AlignTop)

        title_label = QLabel("Choose Your Team", initial_widget)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 70px; font-weight: bold; color: black; margin-bottom: 40px;")

        button_layout = QGridLayout()
        button_layout.setSpacing(10)

        red_button = QPushButton("RED", initial_widget)
        red_button.setStyleSheet("background-color: red; color: white; font-size: 60px; padding: 60px;")
        red_button.setFixedSize(520, 520)
        red_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        red_button.clicked.connect(self.show_red_team_tools)

        blue_button = QPushButton("BLUE", initial_widget)
        blue_button.setStyleSheet("background-color: blue; color: white; font-size: 60px; padding: 60px;")
        blue_button.setFixedSize(520, 520)
        blue_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        blue_button.clicked.connect(self.show_blue_team_tools)

        button_layout.addWidget(red_button, 0, 0, Qt.AlignCenter)
        button_layout.addWidget(blue_button, 0, 1, Qt.AlignCenter)

        initial_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        initial_layout.addSpacerItem(QSpacerItem(20, 160, QSizePolicy.Minimum, QSizePolicy.Fixed))
        initial_layout.addLayout(button_layout)

        initial_widget.setLayout(initial_layout)
        self.stacked_widget.addWidget(initial_widget)
        self.stacked_widget.setCurrentWidget(initial_widget)

    def show_red_team_tools(self):
        self.show_team_tools(self.red_team_tools, "Red Team Tools")
        self.set_background_color(QColor(255, 192, 203))  

    def show_blue_team_tools(self):
        self.show_team_tools(self.blue_team_tools, "Blue Team Tools")
        self.set_background_color(QColor(173, 216, 230))  

    def set_background_color(self, color):
        palette = QPalette()
        palette.setColor(QPalette.Window, color)
        self.stacked_widget.currentWidget().setPalette(palette)

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
        team_label_widget.setStyleSheet("font-size: 34px; font-weight: bold; margin-bottom: 20px;")
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
            grid_label.setStyleSheet("border: 1px solid black; background-color: white; font-size: 18px;")
            grid_label.mousePressEvent = self.create_handler(label_text)
            grid_layout.addWidget(grid_label, row, col)
        
        for index in range(len(labels), 3):
            row = index // 4
            col = index % 4
            grid_label = QLabel("", section_widget)
            grid_label.setAlignment(Qt.AlignCenter)
            grid_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_label.setStyleSheet("border: 1px solid black; background-color: white; font-size: 18px;")
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
    background()
    time.sleep(1.2)
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
