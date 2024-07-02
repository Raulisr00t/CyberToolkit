import sys
import time
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy,
    QMessageBox, QPushButton, QStackedWidget, QSpacerItem, QHBoxLayout, QDialog,
    QLineEdit, QComboBox, QCheckBox, QTextEdit,QFontComboBox,QTextBrowser
)
from PyQt5.QtGui import QColor, QPalette, QPixmap, QBrush,QFont,QTextCursor
from PyQt5.QtCore import Qt
import platform
import subprocess
import paramiko,netmiko
import ftplib
import urllib3
from  urllib.parse import urljoin
from bs4 import BeautifulSoup
import warnings

def background():
    #dont worry it's not malware it is for download app's background))
    url = "https://www.stjohns.edu/sites/default/files/2022-05/istock-1296650655.jpg"
    global home
    global filename
    if platform.uname().system.lower() == "windows":
        home = os.getenv("USERPROFILE")
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
        filename = f"{linux_home}/cybersec.jpg"
        if os.path.exists(filename):
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
            ["CrackMapExec", "Enum4linux", "Searchsploit"],
            ["Msfvenom", "Curl", "Nikto"],
            ["Nikto", "Sherloc", "Osintagram"]
        ]

        self.blue_team_tools = [
            ["Feroxbuster", "Wireshark", "Visual Studio Code"],
            ["Visual Studio", "Bettercap", "Responder"]
        ]

        self.general_team_tools = [
            ["SSH Connection", "FTP Connection", "RDP Connection"],
            ["Netcat Connection","OSINT Tool","DNS LookUP"]
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

        general_button = QPushButton("General Tools", initial_widget)
        general_button.setStyleSheet("background-color: gray; color: white; font-size: 60px; padding: 60px;")
        general_button.setFixedSize(520, 520)
        general_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        general_button.clicked.connect(self.show_general_tools)

        button_layout.addWidget(red_button, 0, 0, Qt.AlignCenter)
        button_layout.addWidget(blue_button, 0, 1, Qt.AlignCenter)
        button_layout.addWidget(general_button, 1, 0, 1, 2, Qt.AlignCenter)

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

    def show_general_tools(self):
        self.show_team_tools(self.general_team_tools, "General Tools")
        self.set_background_color(QColor(211, 211, 211))

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

        num_labels = len(labels)
        rows = (num_labels - 1) // 4 + 1
        cols = min(4, num_labels)

        for index, label_text in enumerate(labels):
            row = index // 4
            col = index % 4
            grid_label = QLabel(label_text, section_widget)
            grid_label.setAlignment(Qt.AlignCenter)
            grid_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_label.setStyleSheet("border: 1px solid black; background-color: white; font-size: 18px;")
            grid_label.mousePressEvent = self.create_handler(label_text)
            grid_layout.addWidget(grid_label, row, col)
        
        for index in range(num_labels, rows * 3):
            row = index // 4
            col = index % 4
            grid_label = QLabel("", section_widget)
            grid_label.setAlignment(Qt.AlignCenter)
            grid_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_label.setStyleSheet("border: 1px solid black; background-color: white; font-size: 18px;")
            grid_layout.addWidget(grid_label, row, col)

        section_widget.setLayout(section_layout)
        return section_widget

    def create_handler(self, label_text):
        def handler(event):
            if label_text == "Nmap":
                self.show_nmap_options()
            if label_text == "Hydra":
                self.show_hydra_options()
            if label_text == "Nikto":
                self.show_nikto_options()
            if label_text == "Curl":
                self.show_curl_options()
            if label_text == "Netcat Connection":
                self.show_ncat_options()
            if label_text == "Gobuster":
                self.show_gobuster_options()
            if label_text == "Searchsploit":
                self.show_searchsploit_options()
            if label_text == "SSH Connection":
                self.show_ssh_options()
            if label_text == "RDP Connection":
                self.show_rdp_options()
            if label_text == "FTP Connection":
                self.show_ftp_options()
            if label_text == "OSINT Tool":
                self.show_osint_options()
            if label_text == "DNS Lookup":
                self.show_lookup_options()
            if label_text == "Enum4Linux":
                self.show_enum_options()
            if label_text == "CrackMapExec":
                self.show_crack_options()
            else:
                self.show_tool_options(label_text)
        return handler

    def show_tool_options(self, tool_name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(f"{tool_name} Options")
        msg.setText(f"Options for {tool_name}")
        if platform.uname().system.lower() == "windows":
            program_files = os.getenv("ProgramFiles")
            program = f"{program_files}\\{tool_name}\\{tool_name}"
            program = program.split('\\')
            if os.path.exists(str(program)):
                os.system("start "+program[3])
                time.sleep(1)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            else:
                pass #for now 
        else:
            programs_path = "/usr/bin/"
            if os.path.exists(programs_path + tool_name):
                os.system(tool_name)
            else:
                pass #for now
    def show_crack_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("CrackMapExec options")
        dialog.setGeometry(100,100,500,500)

        layout = QVBoxLayout(dialog)

        username_layout = QHBoxLayout(dialog)
        username_label = QLabel("Enter Username:")
        username_input = QLineEdit(dialog)
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_input)
        layout.addLayout(username_layout)
        
        server_type_layout = QHBoxLayout()
        server_type_label = QLabel("Enter Server Type:", dialog)
        server_type_combo = QComboBox(dialog)
        server_type_combo.addItems(["Samba Server smb", "FTP Server ftp", "RDP Server rdp", "Mssql Server mssql", "WinRm Server winrm","Ldap Server ldap"])
        server_type_layout.addWidget(server_type_label)
        server_type_layout.addWidget(server_type_combo)
        layout.addLayout(server_type_layout)

        ip_layout = QHBoxLayout(dialog)
        ip_label = QLabel("Enter Ip Address:")
        ip_input = QLineEdit(dialog)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(ip_input)
        layout.addLayout(ip_layout)

        password_layout = QHBoxLayout(dialog)
        password_label = QLabel("Enter a Password:")
        password_input = QLineEdit(dialog)
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_input)
        layout.addLayout(password_layout)

        domain_layout = QHBoxLayout(dialog)
        domain_label = QLabel("Enter a Domain:")
        domain_input = QLineEdit(dialog)
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(domain_input)
        layout.addLayout(domain_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_crack():
            ip = ip_input.text()
            domain = domain_input.text()
            username = username_input.text()
            password = password_input.text()
            server = server_type_combo.currentText()
            server = server.split(' ')[2]

            if not domain:
                command = f"crackmapexec {server} {ip} -u {username} -p {password}"
            else:
                command = f"crackmapexec {server} {domain}\\{ip} -u {username} -p {password}"
            output_area.append(command)

            if not username or not password or not server:
                QMessageBox.warning(dialog, "Warning", "Please check your credentials")
            return command
        
        def run_crack():
            command = generate_command_crack()
            answer = QMessageBox.question(dialog, "Run CrackMapExec", "Do you want to start CrackMapExec? (Y/N)", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                result = subprocess.getoutput(command)
                result.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_crack)
        layout.addWidget(generate_button)
        run_button = QPushButton("Run Command", dialog)
        run_button.clicked.connect(run_crack)
        layout.addWidget(run_button)

        dialog.exec_()

    def show_nmap_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nmap Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        url_layout = QHBoxLayout()
        url_label = QLabel("Domain:", dialog)
        url_input = QLineEdit(dialog)
        url_layout.addWidget(url_label)
        url_layout.addWidget(url_input)
        layout.addLayout(url_layout)

        thread_count_layout = QHBoxLayout()
        thread_count_label = QLabel("Thread Count:", dialog)
        thread_count_input = QLineEdit(dialog)
        thread_count_layout.addWidget(thread_count_label)
        thread_count_layout.addWidget(thread_count_input)
        layout.addLayout(thread_count_layout)

        ip_address_layout = QHBoxLayout()
        ip_address_label = QLabel("IP Address:", dialog)
        ip_address_input = QLineEdit(dialog)
        ip_address_layout.addWidget(ip_address_label)
        ip_address_layout.addWidget(ip_address_input)
        layout.addLayout(ip_address_layout)

        scan_type_layout = QHBoxLayout()
        scan_type_label = QLabel("Scan Type:", dialog)
        scan_type_combo = QComboBox(dialog)
        scan_type_combo.addItems(["SYN Scan (-sS)", "UDP Scan (-sU)", "Script Scan (-sC)", "OS Detection (-O)", "Aggressive Scan (-A)","Extra Verbosity (-vv)"])
        scan_type_layout.addWidget(scan_type_label)
        scan_type_layout.addWidget(scan_type_combo)
        layout.addLayout(scan_type_layout)

        version_scan_layout = QHBoxLayout()
        version_scan_label = QLabel("Version Scan:", dialog)
        version_scan_yes = QCheckBox("Yes", dialog)
        version_scan_layout.addWidget(version_scan_label)
        version_scan_layout.addWidget(version_scan_yes)
        layout.addLayout(version_scan_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_nmap():
            url = url_input.text()
            thread_count = thread_count_input.text()
            ip_address = ip_address_input.text()
            scan_type = scan_type_combo.currentText()
            scan = scan_type.split("(")[1].split(")")[0]  # Correctly extract the scan type

            version_scan = "-sV" if version_scan_yes.isChecked() else ""

            command = f"nmap {scan} {version_scan} --min-rate={thread_count}"
            if url:
                command += f" {url}"
            if ip_address:
                command += f" {ip_address}"
            if not thread_count:
                command = command.split("-min-rate")
            output_area.setText(command)
            return command

        def run_nmap():
            command = generate_command_nmap()
            answer = QMessageBox.question(dialog, "Run Nmap", "Do you want to scan? (Y/N)", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                result = subprocess.getoutput(command)
                output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_nmap)
        layout.addWidget(generate_button)
        run_button = QPushButton("Run Command", dialog)
        run_button.clicked.connect(run_nmap)
        layout.addWidget(run_button)

        dialog.exec_()
    
    def show_enum_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enum4linux Options")
        dialog.setGeometry(100,100,200,300)

        layout = QVBoxLayout(dialog)

        ip_layout = QVBoxLayout()
        ip_lable = QLabel("IP Address:",dialog)
        ip_input = QLineEdit(dialog)
        ip_layout.addWidget(ip_lable)
        ip_layout.addWidget(ip_input)
        layout.addLayout(layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_enum():
            ip = ip_input.text()
            command = f" enum4linux {ip}"
            output_area.append(command)
        
        def run_enum():
            command = generate_command_enum()
            result = subprocess.getoutput(command)
            output_area.append("\n" + result)
            return result
        
        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(run_enum)
        layout.addWidget(generate_button)

        dialog.exec_()
        
    def show_nikto_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nikto Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        hostname_layout = QHBoxLayout()
        hostname_label = QLabel("Hostname:", dialog)
        hostname_input = QLineEdit(dialog)
        hostname_layout.addWidget(hostname_label)
        hostname_layout.addWidget(hostname_input)
        layout.addLayout(hostname_layout)

        output_layout = QHBoxLayout()
        output_label = QLabel("Output File:", dialog)
        output_input = QLineEdit(dialog)
        output_layout.addWidget(output_label)
        output_layout.addWidget(output_input)
        layout.addLayout(output_layout)

        port_layout = QHBoxLayout()
        port_label = QLabel("Specific Port:", dialog)
        port_input = QLineEdit(dialog)
        port_layout.addWidget(port_label)
        port_layout.addWidget(port_input)
        layout.addLayout(port_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_nikto():
            hostname = hostname_input.text()
            output = output_input.text()
            port = port_input.text()
            if not hostname:
                QMessageBox.warning(dialog, "Warning", "Please enter hostname for scanning!")
                return ""
            command = f"nikto -h {hostname} -p {port} -output {output}"
            output_area.setText(command)
            return command

        def run_nikto():
            command = generate_command_nikto()
            if command:
                result = subprocess.getoutput(command)
                output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_nikto)
        layout.addWidget(generate_button)

        start_button = QPushButton("Start Nikto", dialog)
        start_button.clicked.connect(run_nikto)
        layout.addWidget(start_button)

        dialog.exec_()

    def show_hydra_options(self):   
        dialog = QDialog(self)
        dialog.setWindowTitle("Hydra Options")
        dialog.setGeometry(100,100,600,500)

        layout = QVBoxLayout(dialog)

        username_layout = QHBoxLayout()
        username_label = QLabel("Username:",dialog)
        username_input = QLineEdit(dialog)
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_input)
        layout.addLayout(username_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel("Password:",dialog)
        password_input = QLineEdit(dialog)
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_input)
        layout.addLayout(password_layout)

        server_layout = QHBoxLayout()
        server_label = QLabel("Enter Server:",dialog)
        server_input = QLineEdit(dialog)
        server_layout.addWidget(server_label)
        server_layout.addWidget(server_input)
        layout.addLayout(server_layout)

        server_ip_layout = QHBoxLayout()
        server_ip_label = QLabel("Enter Server's IP:",dialog)
        server_ip_input = QLineEdit(dialog)
        server_ip_layout.addWidget(server_ip_label)
        server_ip_layout.addWidget(server_ip_input)
        layout.addLayout(server_ip_layout)

        port_layout = QHBoxLayout()
        port_label = QLabel("Enter Server's port:",dialog)
        port_input = QLineEdit(dialog)
        port_layout.addWidget(port_label)
        port_layout.addWidget(port_input)
        layout.addLayout(port_layout)

        verbose_layout = QHBoxLayout()
        verbose_label = QLabel("Verbose", dialog)
        verbose_yes = QCheckBox("Yes", dialog)
        verbose_layout.addWidget(verbose_label)
        verbose_layout.addWidget(verbose_yes)
        layout.addLayout(verbose_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_hydra():
            username = username_input.text()
            password = password_input.text()
            server = server_input.text()
            server_ip = server_ip_input.text()
            port = port_input.text()
            verbose = "-V" if verbose_yes.isChecked() else ""
            if verbose:
                command = f"hydra -l {username} -p {password} {server+"://"+server_ip+":"+port} -V" 
        
        def run_hydra():
            command = generate_command_hydra()
            answer = QMessageBox.question(dialog, "Run Hydra", "Do you want to do brute-force? (Y/N)", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                result = subprocess.getoutput(command)
                output_area.append("\n" + result)
        
        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(run_hydra)
        layout.addWidget(generate_button)
        dialog.exec_()

    def show_gobuster_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gobuster Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        url_layout = QHBoxLayout()
        url_label = QLabel("URL:", dialog)
        url_input = QLineEdit(dialog)
        url_layout.addWidget(url_label)
        url_layout.addWidget(url_input)
        layout.addLayout(url_layout)

        thread_count_layout = QHBoxLayout()
        thread_count_label = QLabel("Thread Count:", dialog)
        thread_count_input = QLineEdit(dialog)
        thread_count_layout.addWidget(thread_count_label)
        thread_count_layout.addWidget(thread_count_input)
        layout.addLayout(thread_count_layout)

        wordlist_layout = QHBoxLayout()
        wordlist_label = QLabel("Wordlist:", dialog)
        wordlist_input = QLineEdit(dialog)
        if os.path.exists(wordlist_input):
            wordlist_layout.addWidget(wordlist_label)
            wordlist_layout.addWidget(wordlist_input)
            layout.addLayout(wordlist_layout)

            def generate_command_gobuster():
                url = url_input.text()
                thread_count = thread_count_input.text()
                wordlist = wordlist_input.text()
                command = f"gobuster dir -u {url} -w {wordlist} -t {thread_count}"
                return command

            def run_gobuster():
                command = generate_command_gobuster()
                answer = QMessageBox.question(dialog, "Run Gobuster", "Do you want to start Gobuster? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    result.append("\n" + result)

            gobuster_command = QPushButton("Generate Command",dialog)
            gobuster_command.clicked.connect(generate_command_gobuster())
            layout.addWidget(gobuster_command)

            generate_button = QPushButton("Start Gobuster", dialog)
            generate_button.clicked.connect(run_gobuster)
            layout.addWidget(generate_button)

            dialog.exec_()
    
        else:
            QMessageBox.warning("Your wordlist path is incorrect,Please check again")

    def show_rdp_options(self):
        rdp_dialog = QDialog(self)
        rdp_dialog.setWindowTitle("RDP Options")
        rdp_dialog.setGeometry(100,100,600,500)
        global os_type
        os_type = platform.uname().system
        if os_type == "Linux" or os_type == "Darwin":
            layout = QVBoxLayout(rdp_dialog)

            ip_layout = QHBoxLayout()
            ip_label = QLabel("Enter ip address:")
            ip_input = QLineEdit(rdp_dialog)
            ip_layout.addWidget(ip_label)
            ip_layout.addWidget(ip_input)

            layout.addLayout(ip_layout)

            username_layout = QHBoxLayout()
            username_label = QLabel("Enter username:")
            username_input = QLineEdit(rdp_dialog)
            username_layout.addWidget(username_label)
            username_layout.addWidget(username_input)
            
            layout.addLayout(username_layout)

            password_layout = QHBoxLayout()
            password_label = QLabel("Enter password:")
            password_input = QLineEdit(rdp_dialog)
            password_layout.addWidget(password_label)
            password_layout.addWidget(password_input)

            layout.addLayout(password_layout)

            output_area = QTextEdit(rdp_dialog)
            output_area.setReadOnly(True)
            layout.addWidget(output_area)

            def generate_command_rdp():
                ip = ip_input.text()
                username = username_input.text()
                password = password_input.text()

                if not username or not ip or not password:
                    QMessageBox.warning(rdp_dialog,"Please check credentials")
                command = f"xfreedrp /v:{ip} /u:{username} /p:{password}"
                output_area.append(command)
                return command
            
            def run_rdp():
                command = generate_command_rdp()
                answer = QMessageBox.question(rdp_dialog, "Run RDP", "Do you want to start RDP? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    result.append("\n" + result)

            generate_button = QPushButton("Generate Command", rdp_dialog)
            generate_button.clicked.connect(generate_command_rdp)
            layout.addWidget(generate_button)
            run_button = QPushButton("Run Command", rdp_dialog)
            run_button.clicked.connect(run_rdp)
            layout.addWidget(run_button)

            rdp_dialog.exec_()

        else:
            rdp_dialog = QDialog(self)
            rdp_dialog.setWindowTitle("RDP Options")
            rdp_dialog.setGeometry(100,100,600,500)
            
            layout = QVBoxLayout(rdp_dialog)

            ip_layout = QHBoxLayout()
            ip_label = QLabel("Enter ip address:")
            ip_input = QLineEdit(rdp_dialog)
            ip_layout.addWidget(ip_label)
            ip_layout.addWidget(ip_input)

            output_area = QTextEdit(rdp_dialog)
            output_area.setReadOnly(True)
            layout.addWidget(output_area)

            def generate_command_rdp():
                ip = ip_input.text()

                if not ip:
                    QMessageBox.warning(rdp_dialog,"Please check IP address")
                command = f"mstsc /v:{ip}"
                output_area.append(command)
                return command
            
            def run_rdp():
                command = generate_command_rdp()
                answer = QMessageBox.question(rdp_dialog, "Run RDP", "Do you want to start RDP? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    result.append("\n" + result)

            generate_button = QPushButton("Generate Command", rdp_dialog)
            generate_button.clicked.connect(generate_command_rdp)
            layout.addWidget(generate_button)
            run_button = QPushButton("Run Command", rdp_dialog)
            run_button.clicked.connect(run_rdp)
            layout.addWidget(run_button)

            rdp_dialog.exec_()

    def show_curl_options(self):
        curl_dialog = QDialog(self)
        curl_dialog.setWindowTitle("Curl Options")
        curl_dialog.setGeometry(100,100,600,500)

        layout = QVBoxLayout(curl_dialog)

        ip_layout = QHBoxLayout()
        ip_label = QLabel("Enter ip address:")
        ip_input = QLineEdit(curl_dialog)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(ip_input)
        layout.addLayout(ip_layout)

        url_layout = QHBoxLayout()
        url_label = QLabel("Enter a url:")
        url_input = QLineEdit(curl_dialog)
        url_layout.addWidget(url_label)
        url_layout.addWidget(url_input)
        layout.addLayout(url_layout)

        request_type_layout = QHBoxLayout()
        request_type_label = QLabel("Request Type:", curl_dialog)
        request_type_combo = QComboBox(curl_dialog)
        request_type_combo.addItems(["GET", "POST", "OPTIONS", "PUT", "DELETE","HEAD"])
        request_type_layout.addWidget(request_type_label)
        request_type_layout.addWidget(request_type_combo)
        layout.addLayout(request_type_layout)
        
        server_info_layout = QHBoxLayout()
        server_info_label = QLabel("Server INFO")
        server_info_yes = QCheckBox("Yes",curl_dialog)
        server_info_layout.addWidget(server_info_label)
        server_info_layout.addWidget(server_info_yes)
        layout.addLayout(server_info_layout)

        output_area = QTextEdit(curl_dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_curl():
            url = url_input.text()
            ip = ip_input.text()
            request_type = request_type_combo.currentText()
            if "https" not in url or "http" not in url: 
                url = "http://" + url
                response = requests.get(url)
                if response.status_code < 400:
                    if request_type == "GET":
                        command = f"curl {url}"
                    if not request_type == "GET":
                        data_layout = QHBoxLayout()
                        data_label = QLabel("Enter Data:")
                        data_input = QLineEdit(curl_dialog)
                        data_layout.addWidget(data_label)
                        data_layout.addWidget(data_input)
                        
                        data = data_input.text()

                        if request_type == "POST":
                            command = f"curl -X POST {url} -d {data} -H application/json"
                        if request_type == "PUT":
                            command = f"curl -X PUT {url} -d {data} -h application/json"
                        if request_type == "OPTIONS":
                            command = f"curl -X OPTIONS {url} -H Access-Control-Request-Method:content-type {data}"
                        if request_type == "DELETE":
                            command = f"curl -X DELETE {url} {data}"
                else:
                    pass
                server_info = "" if server_info_yes.isChecked() else ""
                command = f"curl {url}"
                output_area.setText(command)

        def run_curl():
            command = generate_command_curl()
            answer = QMessageBox.question(curl_dialog, "Run Nmap", "Do you want to scan? (Y/N)", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                result = subprocess.getoutput(command)
                output_area.append("\n" + result)
        
        generate_button = QPushButton("Generate Command", curl_dialog)
        generate_button.clicked.connect(run_curl)
        layout.addWidget(generate_button)
        curl_dialog.exec_()

    def show_searchsploit_options(self):
        searchsploit_dialog = QDialog(self)
        searchsploit_dialog.setWindowTitle("Searchsploit Options")
        searchsploit_dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(searchsploit_dialog)

        cve_layout = QHBoxLayout()
        cve_label = QLabel("Enter a CVE-ID:", searchsploit_dialog)
        cve_input = QLineEdit(searchsploit_dialog)
        cve_layout.addWidget(cve_label)
        cve_layout.addWidget(cve_input)
        layout.addLayout(cve_layout)

        detailed_scan_layout = QHBoxLayout()
        detailed_scan_label = QLabel("Detailed Information", searchsploit_dialog)
        detailed_scan_yes = QCheckBox("Yes", searchsploit_dialog)
        detailed_scan_layout.addWidget(detailed_scan_label)
        detailed_scan_layout.addWidget(detailed_scan_yes)
        layout.addLayout(detailed_scan_layout)

        output_area = QTextEdit(searchsploit_dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_search():
            global cve
            cve = cve_input.text()
            global detailed
            detailed = "-w" if detailed_scan_yes.isChecked() else ""

            searchsploit = f"searchsploit {cve}"
            output_area.append(searchsploit)
            return searchsploit

        def run_search():
            command = generate_command_search()
            searchsploit = f"searchsploit {cve}"

            result = subprocess.getoutput(command)
            output_area.append("\n" + result)
            return searchsploit
            
        # if detailed:
        def detailed_info():
            url = "https://vulmon.com"
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/58.0.3029.110 Safari/537.36'
                }
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                urllib3.disable_warnings()

                def html_of_site3(url):
                    cve = cve_input
                    cve_modified = cve.replace("--", "-")
                    path = f'vulnerabilitydetails?qid=CVE-{cve_modified}'
                    query3 = urljoin(url, path)

                    response = requests.get(query3, headers=headers, verify=False)
                    if response.status_code != 200:
                        return None
                    return response.content.decode()

                html = html_of_site3(url)
                soup = BeautifulSoup(html, 'html.parser')
                description_tag = soup.find("p", {'class': 'jsdescription1'})
                cvss = soup.find("div", {'class': 'value'})
                references2_div = soup.find('div', class_='ui list ex5')

                if description_tag:
                    description = description_tag.get_text(strip=True)
                    output_area.append(f"Description: {description}")

                if cvss:
                    score = cvss.get_text(strip=True)
                    output_area.append(f"CVSS Score: {score}")

                if references2_div:
                    reference2 = references2_div.find_all('a')
                    for reference_2 in reference2:
                        output_area.append(f"Reference: {reference_2['href']}")

            except Exception as e:
                output_area.append(f"Error fetching details: {str(e)}")
        
        generate_button = QPushButton("Generate Command", searchsploit_dialog)
        generate_button.clicked.connect(generate_command_search)  # Correct connection
        layout.addWidget(generate_button)
        # generate_button = QPushButton("Generate Command", searchsploit_dialog)
        # generate_button.clicked.connect(run_search)
        # layout.addWidget(generate_button)
        # searchsploit_dialog.setLayout(layout)
        # searchsploit_dialog.exec_()

        generate_button2 = QPushButton("Run Command", searchsploit_dialog)
        generate_button2.clicked.connect(detailed_info)  # Correct connection
        layout.addWidget(generate_button2)

        searchsploit_dialog.setLayout(layout)
        searchsploit_dialog.exec_()

    def show_osint_options(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        bold_font = QFont("Helvetica", 10, QFont.Bold)

        # Search query input
        entry_label = QLabel("Enter your search query:")
        entry_label.setFont(bold_font)
        main_layout.addWidget(entry_label)

        self.entry = QLineEdit()
        main_layout.addWidget(self.entry)

        # Number of results input
        count_label = QLabel("How many results do you want to see:")
        count_label.setFont(bold_font)
        main_layout.addWidget(count_label)

        self.count_entry = QLineEdit()
        main_layout.addWidget(self.count_entry)

        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        main_layout.addWidget(search_button)

        # Results display area
        results_label = QLabel("Search Results:")
        results_label.setFont(bold_font)
        main_layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setLineWrapMode(QTextEdit.NoWrap)
        self.results_text.setFontPointSize(10)
        main_layout.addWidget(self.results_text)

    def perform_search(self):
        query = self.entry.text().strip()
        num_results_str = self.count_entry.text().strip()
        self.results_text.clear()

        try:
            num_results = int(num_results_str)
            if num_results <= 0:
                raise ValueError("Number of results must be greater than zero.")

            # Replace list(query, num_results=num_results) with actual search logic
            # For example, if you have a function that searches and returns links:
            links = self.search_and_return_links(query, num_results)

            actual_num_results = len(links)
            if actual_num_results > 0:
                self.results_text.append(f"Showing {min(num_results, actual_num_results)} out of {actual_num_results} results:\n")
                for idx, link in enumerate(links[:num_results]):
                    self.insert_link(link)
            else:
                self.results_text.append("No results found.\n")

        except ValueError as e:
            self.results_text.append(f"Error: {e}")
        except Exception as e:
            self.results_text.append(f"Error occurred: {e}")

    def insert_link(self, link):
        display_text = f"[+] Result: {link}\n"
        self.results_text.moveCursor(QTextCursor.End)
        self.results_text.insertPlainText(display_text)
        cursor = self.results_text.textCursor()
        cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.MoveAnchor, len(display_text))
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        self.results_text.setTextCursor(cursor)
        self.results_text.setTextColor(Qt.blue)
        self.results_text.setUnderlineColor(Qt.blue)
        self.results_text.setOpenExternalLinks(True)
        self.results_text.setHtml(f'<a href="{link}">{display_text}</a>')

    def show_ftp_options(self):
        ftp_dialog = QDialog(self)
        ftp_dialog.setWindowTitle("FTP Connection Options")
        ftp_dialog.setGeometry(250, 100, 450, 350)

        layout = QVBoxLayout(ftp_dialog)

        url_label = QLabel("Domain:", ftp_dialog)
        url_input = QLineEdit(ftp_dialog)
        layout.addWidget(url_label)
        layout.addWidget(url_input)

        ip_label = QLabel("Enter IP Address:", ftp_dialog)
        ip_input = QLineEdit(ftp_dialog)
        layout.addWidget(ip_label)
        layout.addWidget(ip_input)

        user_label = QLabel("Enter Username:", ftp_dialog)
        user_input = QLineEdit(ftp_dialog)
        layout.addWidget(user_label)
        layout.addWidget(user_input)

        passwd_label = QLabel("Enter Password:", ftp_dialog)
        passwd_input = QLineEdit(ftp_dialog)
        passwd_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(passwd_label)
        layout.addWidget(passwd_input)

        port_label = QLabel("Enter Port Address (Default is 21):", ftp_dialog)
        port_input = QLineEdit(ftp_dialog)
        layout.addWidget(port_label)
        layout.addWidget(port_input)

        output_area = QTextEdit(ftp_dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_ftp_command():
            domain = url_input.text()
            ip = ip_input.text()
            username = user_input.text()
            password = passwd_input.text()
            port = port_input.text() or "21"

            if domain:
                command = f"ftp {domain} {port}"
            else:
                command = f"ftp {ip} {port}"

            output_area.setText(command)
            return command, ip, username, password, port

        def run_ftp():
            command, ip, username, password, port = generate_ftp_command()

            try:
                if ip:
                    ftp = ftplib.FTP()
                    ftp.connect(ip, int(port))
                    ftp.login(user=username, passwd=password)
                    output_area.append("\nConnected successfully")
                    ftp.quit()
                else:
                    QMessageBox.warning(self, "Error", "IP Address is required")
            except Exception as e:
                output_area.append(f"\nError: {str(e)}")

        generate_button = QPushButton("Generate Command", ftp_dialog)
        generate_button.clicked.connect(generate_ftp_command)
        layout.addWidget(generate_button)

        run_button = QPushButton("Run Command", ftp_dialog)
        run_button.clicked.connect(run_ftp)
        layout.addWidget(run_button)

        ftp_dialog.setLayout(layout)
        ftp_dialog.exec_()

    def show_lookup_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("DNS Lookup Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        url_layout = QHBoxLayout()
        url_label = QLabel("Domain:", dialog)
        url_input = QLineEdit(dialog)
        url_layout.addWidget(url_label)
        url_layout.addWidget(url_input)
        layout.addLayout(url_layout)

        ip_address_layout = QHBoxLayout()
        ip_address_label = QLabel("IP Address:", dialog)
        ip_address_input = QLineEdit(dialog)
        ip_address_layout.addWidget(ip_address_label)
        ip_address_layout.addWidget(ip_address_input)
        layout.addLayout(ip_address_layout)

        scan_type_layout = QHBoxLayout()
        scan_type_label = QLabel("Query Type:", dialog)
        scan_type_combo = QComboBox(dialog)
        scan_type_combo.addItems([" IPv4 address (--querytype=A)", "IPv6 address (--querytype=AAAA)", "Hardware Related Information (--querytype==hinfo)", "Mail Server Records (--querytype=MX)", "ALL Availible Records (--querytype=any)"])
        scan_type_layout.addWidget(scan_type_label)
        scan_type_layout.addWidget(scan_type_combo)
        layout.addLayout(scan_type_layout)

        default_scan_layout = QHBoxLayout()
        default_scan_label = QLabel("Default Type:", dialog)
        default_scan_yes = QCheckBox("Yes", dialog)
        default_scan_layout.addWidget(default_scan_label)
        default_scan_layout.addWidget(default_scan_yes)
        layout.addLayout(default_scan_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_lookup():
            url = url_input.text()
            ip_address = ip_address_input.text()
            scan_type = scan_type_combo.currentText()
            s = scan_type.split("(")
            f = s[1]
            list = f.split(")")
            scan = list[0]

            version_scan = f"nslookup --querytype=A" if default_scan_yes.isChecked() else ""
            if url:
                command = f"nslookup {url} --querytype=={scan_type_combo}"
                output_area.setText(command)
            else:
                command = f"nslookup {ip_address} {scan}"

        def run_lookup():
            command = generate_command_lookup()
            answer = QMessageBox.question(dialog, "Run Nmap", "Do you want to scan? (Y/N)", QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                result = subprocess.getoutput(command)
                output_area.append("\n" + result)
        
        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(run_lookup)
        layout.addWidget(generate_button)
        dialog.exec_()

    def show_ssh_options(self):
        ssh_dialog = QDialog(self)
        ssh_dialog.setWindowTitle("SSH Connection Options")
        ssh_dialog.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(ssh_dialog)

        ip_label = QLabel("Enter IP Address:")
        self.ip_edit = QLineEdit()
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_edit)

        port_label = QLabel("Enter Port Number:(Default is 22)")
        self.port_edit = QLineEdit()
        layout.addWidget(port_label)
        layout.addWidget(self.port_edit)

        username_label = QLabel("Enter Username:")
        self.username_edit = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_edit)

        password_label = QLabel("Enter Password:")
        self.password_edit = QLineEdit()
        layout.addWidget(password_label)
        layout.addWidget(self.password_edit)

        button_box = QHBoxLayout()

        run_button = QPushButton("Run SSH")
        run_button.clicked.connect(self.run_ssh)
        button_box.addWidget(run_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(ssh_dialog.reject)
        button_box.addWidget(cancel_button)
        
        layout.addLayout(button_box)

        ssh_dialog.exec_()

    def run_ssh(self):
        ip = self.ip_edit.text()
        port = self.port_edit.text()
        username = self.username_edit.text()
        password = self.password_edit.text()

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=port, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command('ls')
            output = stdout.read().decode()
            ssh.close()
            self.show_message(f'SSH Command Output:\n{output}')

        except Exception as e:
            self.show_message(f'Error: {str(e)}')

    def show_ncat_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("NetCat Connection Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        ip_layout = QHBoxLayout()
        ip_label = QLabel("IP address:", dialog)
        ip_input = QLineEdit(dialog)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(ip_input)
        layout.addLayout(ip_layout)

        port_layout = QHBoxLayout()
        port_label = QLabel("Port:", dialog)
        port_input = QLineEdit(dialog)
        port_layout.addWidget(port_label)
        port_layout.addWidget(port_input)
        layout.addLayout(port_layout)

        shell_layout = QHBoxLayout()
        shell_label = QLabel("Executing command:", dialog)
        shell_input = QLineEdit(dialog)
        shell_layout.addWidget(shell_label)
        shell_layout.addWidget(shell_input)
        layout.addLayout(shell_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_ncat():
            ip = ip_input.text()
            port = port_input.text()
            command = shell_input.text()
            
            if not ip or not port:
                QMessageBox.warning(dialog, "Input Error", "Please enter both IP address and port.")
                return

            if command:
                command = f"ncat {ip} {port} -e {command}"
            else:
                command = f"ncat {ip} {port}"
            output_area.setText(command)
            return command

        def run_ncat():
            command = generate_command_ncat()
            if command:
                answer = QMessageBox.question(dialog, "Connect Netcat", "Do you want to create connection? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)
            
        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(run_ncat)
        layout.addWidget(generate_button)

        dialog.exec_()

def main():
    background()
    time.sleep(1.2)
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
