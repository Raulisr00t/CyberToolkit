import sys
import time
import os
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy,
    QMessageBox, QPushButton, QStackedWidget, QSpacerItem, QHBoxLayout, QDialog,
    QLineEdit, QComboBox, QCheckBox, QTextEdit,QFontComboBox,QTextBrowser
)
from PyQt5.QtGui import QColor, QPalette, QPixmap, QBrush,QFont,QTextCursor
from PyQt5.QtCore import Qt , QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
import platform
import subprocess
import paramiko,netmiko
import ftplib
import urllib3
from  urllib.parse import urljoin
from bs4 import BeautifulSoup
import warnings
import tkinter as tk
from tkinter import scrolledtext
from googlesearch import search
import webbrowser
import pyuac

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))
        self.setMinimumSize(QtCore.QSize(250, 100))
        self.setMouseTracking(True)
        self.initialized = False

    def enterEvent(self, event):
        self.update_button_geometry()
        self.on_hover()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.on_leave()
        super().leaveEvent(event)

    def update_button_geometry(self):
        self.position = self.geometry().topLeft()
        self.sizes = self.geometry().size()
        self.initialized = True

    def on_hover(self):
        if not self.initialized:
            self.update_button_geometry()

        self.anim_group = QParallelAnimationGroup(self)
        
        size_animation = QPropertyAnimation(self, b"size")
        size_animation.setEasingCurve(QEasingCurve.InOutCubic)
        size_animation.setEndValue(QtCore.QSize(self.sizes.width() + 16, self.sizes.height() + 16))
        size_animation.setDuration(100)
        self.anim_group.addAnimation(size_animation)
        
        pos_animation = QPropertyAnimation(self, b"pos")
        pos_animation.setEasingCurve(QEasingCurve.InOutCubic)
        pos_animation.setEndValue(QtCore.QPoint(self.position.x() - 8, self.position.y() - 8))
        pos_animation.setDuration(100)
        self.anim_group.addAnimation(pos_animation)
        
        self.anim_group.start()

    def on_leave(self):
        if not self.initialized:
            self.update_button_geometry()

        self.anim_group = QParallelAnimationGroup(self)
        
        size_animation = QPropertyAnimation(self, b"size")
        size_animation.setEasingCurve(QEasingCurve.InOutCubic)
        size_animation.setEndValue(self.sizes)
        size_animation.setDuration(100)
        self.anim_group.addAnimation(size_animation)
        
        pos_animation = QPropertyAnimation(self, b"pos")
        pos_animation.setEasingCurve(QEasingCurve.InOutCubic)
        pos_animation.setEndValue(self.position)
        pos_animation.setDuration(100)
        self.anim_group.addAnimation(pos_animation)
        
        self.anim_group.start()



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CAPSTONE Project--GROUP D")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.buttons = []
        
        self.red_team_tools = [
            ["Nmap", "Hydra", "Gobuster"],
            ["CrackMapExec", "Enum4linux", "Searchsploit"],
            ["Msfvenom", "Curl", "Nikto"],
            ["(Coming Soon)", "Sherloc", "(Coming Soon)"]
        ]

        self.blue_team_tools = [
            ["Snort", "(Coming Soon)", "Zeek"],
            ["Dcfldd", "TcpDump", "Registry Editor"],
            ["(Coming Soon)", "(Coming Soon)","(Coming Soon)"]
        ]

        self.general_team_tools = [
            ["SSH Connection", "FTP Connection", "RDP Connection"],
            ["Netcat Connection", "OSINT Tool", "DNS Lookup"]
        ]
        self.setupUi()

###################################################################
    def setupUi(self):
        Main = QWidget(self)
        Main.setObjectName("Main")
        Main.setStyleSheet("#Main{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgb(173, 216, 230), stop:1 rgb(147, 112, 219))}\n"
"#BlueTeamButton{\n"
"                background-color: #3498db;\n"
"                border-radius: 15px;\n"
"                margin: 5px;\n"
"                padding:10px 0;\n"
"            }\n"
"#RedTeamButton{\n"
"                background-color: #e74c3c;\n"
"                border-radius: 15px;\n"
"                margin: 5px;\n"
"                padding:10px 0;\n"
"           }\n"
"#GeneralToolsButton{\n"
"                background-color: #95a5a6;\n"
"                border-radius: 15px;\n"
"                margin: 5px;\n"
"                padding:10px 0;\n"
"            }\n"
"\n"
"#Buttons_widget{\n"
"    background-color: rgba(0, 0, 0, 0.5);\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"\n"
"#Help_Button{\n"
"border-radius: 24px;\n"
"background-color: white;\n"
"border: 0px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Main)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.Mid = QtWidgets.QWidget(Main)
        self.Mid.setObjectName("Mid")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Mid)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_wiget = QtWidgets.QWidget(self.Mid)
        self.label_wiget.setObjectName("label_wiget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.label_wiget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel("Choose Your Team",self.label_wiget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.label_wiget)
        self.widget = QtWidgets.QWidget(self.Mid)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Buttons_widget = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Buttons_widget.sizePolicy().hasHeightForWidth())
        self.Buttons_widget.setSizePolicy(sizePolicy)
        self.Buttons_widget.setMaximumSize(QtCore.QSize(1200, 400))
        self.Buttons_widget.setObjectName("Buttons_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Buttons_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.RedTeamButton = HoverButton('Red Team',self.Buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.RedTeamButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./img/hacker.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RedTeamButton.setIcon(icon)
        self.RedTeamButton.setIconSize(QtCore.QSize(48, 48))
        self.RedTeamButton.setObjectName("RedTeamButton")
        self.RedTeamButton.clicked.connect(self.show_red_team_tools)
        self.horizontalLayout.addWidget(self.RedTeamButton)
        self.BlueTeamButton = HoverButton('Blue Team',self.Buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.BlueTeamButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./img/defender.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BlueTeamButton.setIcon(icon1)
        self.BlueTeamButton.setIconSize(QtCore.QSize(48, 48))
        self.BlueTeamButton.setShortcut("")
        self.BlueTeamButton.setObjectName("BlueTeamButton")
        self.BlueTeamButton.clicked.connect(self.show_blue_team_tools)
        self.horizontalLayout.addWidget(self.BlueTeamButton)
        self.GeneralToolsButton = HoverButton('General Tools',self.Buttons_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.GeneralToolsButton.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./img/set.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.GeneralToolsButton.setIcon(icon2)
        self.GeneralToolsButton.setIconSize(QtCore.QSize(48, 48))
        self.GeneralToolsButton.setObjectName("GeneralToolsButton")
        self.GeneralToolsButton.clicked.connect(self.show_general_tools)
        self.horizontalLayout.addWidget(self.GeneralToolsButton)
        self.horizontalLayout_2.addWidget(self.Buttons_widget)
        self.verticalLayout_2.addWidget(self.widget)
        self.verticalLayout.addWidget(self.Mid)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.bottom = QtWidgets.QWidget(Main)
        self.bottom.setObjectName("bottom")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.bottom)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.widget_2 = QtWidgets.QWidget(self.bottom)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Help_Button = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Help_Button.sizePolicy().hasHeightForWidth())
        self.Help_Button.setSizePolicy(sizePolicy)
        self.Help_Button.setMinimumSize(QtCore.QSize(0, 0))
        self.Help_Button.setMaximumSize(QtCore.QSize(16777215, 1000000))
        self.Help_Button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./img/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Help_Button.setIcon(icon3)
        self.Help_Button.setIconSize(QtCore.QSize(48, 48))
        self.Help_Button.setObjectName("Help_Button")
        self.verticalLayout_4.addWidget(self.Help_Button)
        self.horizontalLayout_3.addWidget(self.widget_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.bottom, 0, QtCore.Qt.AlignBottom)
        self.stacked_widget.addWidget(Main)
        self.stacked_widget.setCurrentWidget(Main)
        


    def show_red_team_tools(self):
        self.show_team_tools(self.red_team_tools, "Red Team Tools","#e74c3c")

    def show_blue_team_tools(self):
        self.show_team_tools(self.blue_team_tools, "Blue Team Tools","#3498db")

    def show_general_tools(self):
        self.show_team_tools(self.general_team_tools, "General Tools","#95a5a6")

    def show_team_tools(self, tools, team_label,color):
        tool_widget = QtWidgets.QWidget(self)
        tool_widget.setObjectName("centralwidget")
        tool_widget.setStyleSheet("#centralwidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgb(173, 216, 230), stop:1 rgb(147, 112, 219))}")
        self.verticalLayout = QtWidgets.QVBoxLayout(tool_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.navbar = QtWidgets.QWidget(tool_widget)
        self.navbar.setStyleSheet(f"background-color:{color};\n"
"border-radius: 15px;")
        self.navbar.setObjectName("navbar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.navbar)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TeamBar = QtWidgets.QWidget(self.navbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TeamBar.sizePolicy().hasHeightForWidth())
        self.TeamBar.setSizePolicy(sizePolicy)
        self.TeamBar.setObjectName("TeamBar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.TeamBar)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(team_label,self.TeamBar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addWidget(self.TeamBar)
        self.TurnBack = QtWidgets.QWidget(self.navbar)
        self.TurnBack.setObjectName("TurnBack")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.TurnBack)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TurnBacButton = QtWidgets.QPushButton(self.TurnBack)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.TurnBacButton.setFont(font)
        self.TurnBacButton.setStyleSheet("padding: 5px 10px;")
        self.TurnBacButton.setText("")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./img/turn-back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TurnBacButton.setIcon(icon)
        self.TurnBacButton.setIconSize(QtCore.QSize(32, 32))
        self.TurnBacButton.setObjectName("TurnBacButton")
        self.TurnBacButton.clicked.connect(self.return_to_choice)
        self.verticalLayout_4.addWidget(self.TurnBacButton)
        self.horizontalLayout.addWidget(self.TurnBack, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.navbar, 0, QtCore.Qt.AlignTop)
        self.Body = QtWidgets.QWidget(tool_widget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Body.sizePolicy().hasHeightForWidth())
        self.Body.setSizePolicy(sizePolicy)
        self.Body.setStyleSheet("QPushButton{\n"
"    margin: 10px;\n"
"    border-radius: 10px;\n"
"    background-color: #ffffff;\n"
"    padding: 10px;\n"
"}")
        self.Body.setObjectName("Body")
        self.gridLayout = QtWidgets.QGridLayout(self.Body)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout.addWidget(self.Body)


        row, col = 0, 0
        for row_tools in tools:
            for tool in row_tools:
                tool_button = HoverButton(tool)
                tool_button.setStyleSheet("margin: 10px; padding: 20px;")
                tool_button.setFont(QtGui.QFont('Arial', 14))
                tool_button.setMinimumSize(200, 100)
                tool_button.setMaximumSize(700, 300)
                tool_button.clicked.connect(self.create_handler(tool))
                self.gridLayout.addWidget(tool_button, row, col)
                self.buttons.append(tool_button)
                col += 1
            row += 1
            col = 0

        # Adjust initial sizes and positions
        QtCore.QTimer.singleShot(0, self.adjust_initial_sizes)
        self.stacked_widget.addWidget(tool_widget)
        self.stacked_widget.setCurrentWidget(tool_widget)

    def on_tool_button_clicked(self, tool):
        print(f"Tool {tool} clicked")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for button in self.buttons:
            button.position = button.geometry().topLeft()
            button.sizes = button.geometry().size()

    def adjust_initial_sizes(self):
        for button in self.buttons:
            button.position = button.geometry().topLeft()
            button.sizes = button.geometry().size()

    def return_to_choice(self):
        self.stacked_widget.setCurrentIndex(0)

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
            if label_text == "Snort":
                self.show_snort_options()
            if label_text == "Volatility":
                self.show_volatility_options()
            if label_text == "Registry Editor":
                self.show_reg_options()
            if label_text == "Dcfldd":
                self.show_dcfldd_options()
            if label_text == "Zeek":
                self.show_zeek_options()
            if label_text == "TcpDump":
                self.show_tcpdump_options()
            if "Coming Soon" in label_text:
                self.show_coming_soon(label_text)
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

    def show_coming_soon(self, tool_name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(f"{tool_name}")
        msg.setText(f"{tool_name} functionality is coming soon!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

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
        scan_type_combo.addItems(["SYN Scan (-sS)", "UDP Scan (-sU)", "Script Scan (-sC)", "OS Detection (-O)", "Aggressive Scan (-A)", "Extra Verbosity (-vv)"])
        scan_type_layout.addWidget(scan_type_label)
        scan_type_layout.addWidget(scan_type_combo)
        layout.addLayout(scan_type_layout)

        version_scan_layout = QHBoxLayout()
        version_scan_label = QLabel("Version Scan:", dialog)
        version_scan_yes = QCheckBox("Yes", dialog)
        version_scan_layout.addWidget(version_scan_label)
        version_scan_layout.addWidget(version_scan_yes)
        layout.addLayout(version_scan_layout)

        skip_host_layout = QHBoxLayout()
        skip_host_label = QLabel("Scan without Ping:", dialog)
        skip_host_discovery_checkbox = QCheckBox("Yes",dialog)
        skip_host_layout.addWidget(skip_host_label)
        skip_host_layout.addWidget(skip_host_discovery_checkbox)
        layout.addLayout(skip_host_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_nmap():
            url = url_input.text()
            thread_count = thread_count_input.text()
            ip_address = ip_address_input.text()
            scan_type = scan_type_combo.currentText()
            scan = scan_type.split("(")[1].split(")")[0]
            command = "nmap"
    
            version_scan = "-sV" if version_scan_yes.isChecked() else ""
            not_ping = "-Pn" if skip_host_discovery_checkbox.isChecked() else ""
            
            if not_ping and url:
                command += f' -Pn {url}'

            if not_ping and ip_address:
                command += f' -Pn {ip_address}'

            if thread_count:
                command = f"nmap {scan} {version_scan} --min-rate={thread_count}"

            if url and ip_address:
                QMessageBox.warning(dialog,"Option Error","Domain and IP address doesn not together!")
                return ""
            
            if url:
                command += f" {url}" 

            if ip_address:
                command += f" {ip_address}"

            if not thread_count:
                if version_scan:
                    command = command.split("-min-rate")
                    if url:
                        command += version_scan,url
                        output_area.setText(str(command))
                    elif ip_address:
                        command += version_scan,ip_address
                        output_area.setText(str(command))
                    else:
                        QMessageBox.information(dialog,"Please check your inputs")
                        pass
                else:
                    command = command.split("-min-rate")

            output_area.setText(command)
            return command

        def run_nmap():
            command = generate_command_nmap()
            answer = QMessageBox.question(self, "Run Nmap", "Do you want to scan? (Y/N)", QMessageBox.Yes | QMessageBox.No)
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

    def show_volatility_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Volatility Options")
        dialog.setGeometry(100,100,600,500)
        
        layout = QVBoxLayout(dialog)
        
        python_layout = QHBoxLayout()
        python_label = QLabel("Domain:", dialog)
        python_input = QLineEdit(dialog)
        python_layout.addWidget(python_label)
        python_layout.addWidget(python_input)
        layout.addLayout(python_layout)

        volatility_path_layout = QHBoxLayout()
        volatility_path_label = QLabel("volatility path:", dialog)
        volatility_path_input = QLineEdit(dialog)
        volatility_path_layout.addWidget(volatility_path_label)
        volatility_path_layout.addWidget(volatility_path_input)

        layout.addLayout(volatility_path_layout)

        file_path_layout = QHBoxLayout()
        file_path_label = QLabel("IP Address:", dialog)
        file_path_input = QLineEdit(dialog)
        file_path_layout.addWidget(file_path_label)
        file_path_layout.addWidget(file_path_input)

        layout.addLayout(file_path_layout)

        volatility_options_layout = QHBoxLayout()
        volatility_options_label = QLabel("Scan Type:", dialog)
        volatility_options_combo = QComboBox(dialog)
        volatility_options_combo.addItems(["linux.pslist", " linux.pstree", "linux.lsmod", "linux.netstat", "linux.bash","windows.pslist","windows.pstree","windows.filescan","windows.cmdline","windows.netscan"])
        volatility_options_layout.addWidget(volatility_options_label)
        volatility_options_layout.addWidget(volatility_options_combo)
        layout.addLayout(volatility_options_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_volatility():
            domain = python_input.text()
            file_path = file_path_input.text()
            command = ""
            output_area.append(command)


        def run_volatility():
            command = generate_command_volatility()
            output_area.append(command)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_volatility)
        layout.addWidget(generate_button)

        run_button = QPushButton("Run Command", dialog)
        run_button.clicked.connect(run_volatility)
        layout.addWidget(run_button)

        dialog.exec_()

    def show_reg_options(self):
        os_type = platform.uname().system
        if os_type.lower() =="windows":
            dialog = QDialog(self)
            dialog.setWindowTitle("Registry Editor Options")
            dialog.setGeometry(100, 100, 600, 500)

            layout = QVBoxLayout()

            query_label = QLabel("Enter Registry Key or Path:", dialog)
            query_input = QLineEdit(dialog)
            layout.addWidget(query_label)
            layout.addWidget(query_input)

            operation_layout = QHBoxLayout()
            operation_label = QLabel("Operation:", dialog)
            operation_combo = QComboBox(dialog)
            operation_combo.addItems(["Query", "Add", "Save","Delete","Copy"])
            operation_layout.addWidget(operation_label)
            operation_layout.addWidget(operation_combo)
            layout.addLayout(operation_layout)

            priv_scan_layout = QHBoxLayout()
            priv_scan_label = QLabel("Run as admin:", dialog)
            priv_scan_checkbox = QCheckBox("Yes", dialog)
            priv_scan_layout.addWidget(priv_scan_label)
            priv_scan_layout.addWidget(priv_scan_checkbox)
            layout.addLayout(priv_scan_layout)

            output_area = QTextEdit(dialog)
            output_area.setReadOnly(True)
            layout.addWidget(output_area)

            instruction_label = QLabel("<b>Example:(Path or Registry)</b> HKCU\\Software\\MyApp", dialog)
            layout.addWidget(instruction_label)

            def generate_command():
                query = query_input.text()
                operation = operation_combo.currentText().split()[0].lower()
                global run_as_admin
                run_as_admin = priv_scan_checkbox.isChecked()

                if operation == "query":
                    command = f"reg query {query}"
                elif operation == "add":
                    # Example: reg add HKCU\\Software\\MyApp /v SomeValue /t REG_SZ /d "My Data"
                    command = f"reg add {query}"  # Replace with appropriate parameters
                elif operation == "edit":
                    # Example: reg edit HKCU\\Software\\MyApp /v SomeValue /t REG_SZ /d "Updated Data"
                    command = f"reg edit {query}"  # Replace with appropriate parameters
                elif operation == "copy":
                    command = f"reg copy {query}"
                elif operation == "save":
                    command = f"reg save {query}"
                elif operation == "delete":
                    command = f"reg delete {query}"
                else:
                    command = ""

                output_area.setText(command)

                return command

            def run_command(self):
                command = generate_command()
                run_as_admin = priv_scan_checkbox.isChecked()

                if command:
                    if run_as_admin:
                        command_list = command.split()
                        result = pyuac.runAsAdmin(command_list)
                        if isinstance(result, int):
                            output_area.append(f"\nCommand failed with status code: {result}")
                        else:
                            output_area.append("\n" + result)
                    else:
                        result = subprocess.getoutput(command)
                        output_area.append("\n" + result)

            generate_button = QPushButton("Generate Command", dialog)
            generate_button.clicked.connect(generate_command)
            layout.addWidget(generate_button)

            run_button = QPushButton("Run Command", dialog)
            run_button.clicked.connect(run_command)
            layout.addWidget(run_button)

            dialog.setLayout(layout)
            dialog.exec_()

        else:
            QMessageBox.information(dialog,"Your OS is not Windows!")

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
        server_label = QLabel("Enter Target Server:",dialog)
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
                command = f"hydra -l {username} -p {password} {server}://{server_ip}:{port} -V" 

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
        wordlist_layout.addWidget(wordlist_label)
        wordlist_layout.addWidget(wordlist_input)
        layout.addLayout(wordlist_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_gobuster():
            url = url_input.text()
            thread_count = thread_count_input.text()
            wordlist = wordlist_input.text()

            if os.path.exists(wordlist):
                command = f"gobuster dir -u {url} -w {wordlist} -t {thread_count}"
                return command
            else:
                QMessageBox.warning(dialog, "Wordlist Error", "Your wordlist path is incorrect. Please check again.")

        def run_gobuster():
            command = generate_command_gobuster()
            if command:
                answer = QMessageBox.question(dialog, "Run Gobuster", "Do you want to start Gobuster? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)

        gobuster_command_button = QPushButton("Generate Command", dialog)
        gobuster_command_button.clicked.connect(generate_command_gobuster)
        layout.addWidget(gobuster_command_button)

        start_gobuster_button = QPushButton("Start Gobuster", dialog)
        start_gobuster_button.clicked.connect(run_gobuster)
        layout.addWidget(start_gobuster_button)

        dialog.exec_()

    def show_rdp_options(self):
        global os_type
        rdp_dialog = QDialog(self)
        rdp_dialog.setWindowTitle("RDP Options")
        rdp_dialog.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout(rdp_dialog)

        ip_layout = QHBoxLayout()
        ip_label = QLabel("Enter IP address:", rdp_dialog)
        ip_input = QLineEdit(rdp_dialog)
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(ip_input)
        layout.addLayout(ip_layout)

        username_layout = QHBoxLayout()
        username_label = QLabel("Enter username:", rdp_dialog)
        username_input = QLineEdit(rdp_dialog)
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_input)
        layout.addLayout(username_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel("Enter password:", rdp_dialog)
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

            if not ip or not username or not password:
                QMessageBox.warning(rdp_dialog, "Warning", "Please fill in all fields.")
                return ""
            
            os_type = platform.uname().system
            if os_type == "Linux" or os_type == "Darwin":
                command = f"xfreerdp /v:{ip} /u:{username} /p:{password}"
            elif os_type == "Windows":
                command = f"mstsc /v:{ip}"
            else:
                QMessageBox.warning(rdp_dialog, "Unsupported OS", "RDP is not supported on this operating system.")
                return ""

            output_area.setText(command)
            return command

        def run_rdp():
            command = generate_command_rdp()
            if command:
                answer = QMessageBox.question(rdp_dialog, "Run RDP", "Do you want to start RDP? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", rdp_dialog)
        generate_button.clicked.connect(generate_command_rdp)
        layout.addWidget(generate_button)

        run_button = QPushButton("Run Command", rdp_dialog)
        run_button.clicked.connect(run_rdp)
        layout.addWidget(run_button)

        rdp_dialog.setLayout(layout)
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
                            command = f"curl -X PUT {url} -d {data} -H application/json"
                        if request_type == "OPTIONS":
                            command = f"curl -X OPTIONS {url} -H Access-Control-Request-Method:content-type {data}"
                        if request_type == "DELETE":
                            command = f"curl -X DELETE {url} {data}"
                else:
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
                            command = f"curl -X PUT {url} -d {data} -H application/json"
                        if request_type == "OPTIONS":
                            command = f"curl -X OPTIONS {url} -H Access-Control-Request-Method:content-type {data}"
                        if request_type == "DELETE":
                            command = f"curl -X DELETE {url} {data}"
                            
                server_info = "-IL" if server_info_yes.isChecked() else ""

                if server_info:
                    command = f"curl {url}"
                    command += "-IL"
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
        def perform_search():
            query = entry.get()
            results_text.delete(1.0, tk.END) 
            results_text.insert(tk.END, f"Searching for: {query}\n\n")
            
            try:
                num_results = int(count_entry.get())
                links = list(search(query, num_results=num_results))
                
                actual_num_results = len(links)
                if actual_num_results > 0:
                    results_text.insert(tk.END, f"Showing {min(num_results, actual_num_results)} out of {actual_num_results} results:\n\n")
                    for idx, link in enumerate(links):
                        if idx < num_results:
                            insert_link(link)
                else:
                    results_text.insert(tk.END, "No results found.\n")
                    
            except ValueError:
                results_text.insert(tk.END, "Please enter a valid number for the number of results.\n")
            except Exception as e:
                results_text.insert(tk.END, f"Error occurred: {e}")

        def insert_link(link):
            display_text = f"[+] Result: {link}\n"
            results_text.insert(tk.END, display_text)
            start_index = results_text.index(tk.END + f"-{len(display_text)}c")
            end_index = results_text.index(tk.END + "-1c")
            results_text.tag_add(link, start_index, end_index)
            results_text.tag_bind(link, "<Button-1>", lambda e, link=link: open_link(link))
            results_text.tag_config(link, foreground="blue", underline=True)

        def open_link(link):
            webbrowser.open(link)

        root = tk.Tk()
        root.title("OSINT-Tool")

        bold_font = ("Helvetica", 10, "bold")

        entry_label = tk.Label(root, text="Enter your search query:", font=bold_font)
        entry_label.pack(pady=15, padx=30)

        entry = tk.Entry(root, width=80)
        entry.pack(pady=5)

        count_label = tk.Label(root, text="How many results do you want to see:", font=bold_font)
        count_label.pack(pady=15, padx=30)

        count_entry = tk.Entry(root, width=10)
        count_entry.pack(pady=5)

        search_button = tk.Button(root, text="Search", command=perform_search)
        search_button.pack(pady=15, padx=10)

        results_text = scrolledtext.ScrolledText(root, width=100, height=20, bg="lightblue") 
        results_text.pack(pady=10)

        root.mainloop()

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

        listener_layout = QHBoxLayout()
        listener_label = QLabel("Listener Configuration:", dialog)
        listener_yes = QCheckBox("Yes", dialog)
        listener_layout.addWidget(listener_label)
        listener_layout.addWidget(listener_yes)
        layout.addLayout(listener_layout)

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
            shell = shell_input.text()
            listener = listener_yes.isChecked()

            if not ip or not port:
                QMessageBox.warning(dialog, "Input Error", "Please enter both IP address and port.")
                return ""
            
            command = f"ncat "
            if listener:
                if shell:
                    command += f"-l -v -p {port} -e {shell}"
                else:
                    command += f"-l -v -p {port}"
            else:
                command += f"{ip} {port}"

            output_area.setText(command)
            return command

        def run_ncat():
            command = generate_command_ncat()
            if command:
                answer = QMessageBox.question(dialog, "Connect Netcat", "Do you want to create connection? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    subprocess.run(command,shell=True)
                    #output_area.append("\n" + result)
            
        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(run_ncat)
        layout.addWidget(generate_button)

        dialog.exec_()

    def show_dcfldd_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("dcfldd Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        input_file_layout = QHBoxLayout()
        input_file_label = QLabel("Input File:", dialog)
        input_file_input = QLineEdit(dialog)
        input_file_layout.addWidget(input_file_label)
        input_file_layout.addWidget(input_file_input)
        layout.addLayout(input_file_layout)

        output_file_layout = QHBoxLayout()
        output_file_label = QLabel("Output File:", dialog)
        output_file_input = QLineEdit(dialog)
        output_file_layout.addWidget(output_file_label)
        output_file_layout.addWidget(output_file_input)
        layout.addLayout(output_file_layout)

        hash_type_layout = QHBoxLayout()
        hash_type_label = QLabel("Hash Type:", dialog)
        hash_type_combo = QComboBox(dialog)
        hash_type_combo.addItems(["md5", "sha1", "sha256", "sha512"])
        hash_type_layout.addWidget(hash_type_label)
        hash_type_layout.addWidget(hash_type_combo)
        layout.addLayout(hash_type_layout)

        hash_log_layout = QHBoxLayout()
        hash_log_label = QLabel("Hash Log File:", dialog)
        hash_log_input = QLineEdit(dialog)
        hash_log_layout.addWidget(hash_log_label)
        hash_log_layout.addWidget(hash_log_input)
        layout.addLayout(hash_log_layout)

        split_size_layout = QHBoxLayout()
        split_size_label = QLabel("Split Size (MB):", dialog)
        split_size_input = QLineEdit(dialog)
        split_size_layout.addWidget(split_size_label)
        split_size_layout.addWidget(split_size_input)
        layout.addLayout(split_size_layout)

        verify_layout = QHBoxLayout()
        verify_label = QLabel("Verify:", dialog)
        verify_yes = QCheckBox("Yes", dialog)
        verify_layout.addWidget(verify_label)
        verify_layout.addWidget(verify_yes)
        layout.addLayout(verify_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_dcfldd():
            input_file = input_file_input.text()
            output_file = output_file_input.text()
            hash_type = hash_type_combo.currentText()
            hash_log = hash_log_input.text()
            split_size = split_size_input.text()
            verify = verify_yes.isChecked()

            command = f"dcfldd if={input_file} of={output_file} hash={hash_type} hashlog={hash_log}"
            if split_size:
                command += f" split={split_size}M"
            if verify:
                command += " vf={output_file}"

            output_area.setText(command)
            return command

        def run_dcfldd():
            command = generate_command_dcfldd()
            if command:
                answer = QMessageBox.question(dialog, "Run dcfldd", "Do you want to run dcfldd? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_dcfldd)
        layout.addWidget(generate_button)

        start_button = QPushButton("Start dcfldd", dialog)
        start_button.clicked.connect(run_dcfldd)
        layout.addWidget(start_button)

        dialog.exec_()

    def show_zeek_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Zeek Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        interface_layout = QHBoxLayout()
        interface_label = QLabel("Interface:", dialog)
        interface_input = QLineEdit(dialog)
        interface_layout.addWidget(interface_label)
        interface_layout.addWidget(interface_input)
        layout.addLayout(interface_layout)

        scripts_layout = QHBoxLayout()
        scripts_label = QLabel("Scripts (comma-separated):", dialog)
        scripts_input = QLineEdit(dialog)
        scripts_layout.addWidget(scripts_label)
        scripts_layout.addWidget(scripts_input)
        layout.addLayout(scripts_layout)

        output_dir_layout = QHBoxLayout()
        output_dir_label = QLabel("Output Directory:", dialog)
        output_dir_input = QLineEdit(dialog)
        output_dir_layout.addWidget(output_dir_label)
        output_dir_layout.addWidget(output_dir_input)
        layout.addLayout(output_dir_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_zeek():
            interface = interface_input.text()
            scripts = scripts_input.text()
            output_dir = output_dir_input.text()

            command = f"zeek -i {interface}"
            if scripts:
                command += f" {scripts}"
            if output_dir:
                command += f" Log::default_writer=ASCII::Writer path={output_dir}"

            output_area.setText(command)
            return command

        def run_zeek():
            command = generate_command_zeek()
            if command:
                answer = QMessageBox.question(dialog, "Run Zeek", "Do you want to run Zeek? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_zeek)
        layout.addWidget(generate_button)

        start_button = QPushButton("Start Zeek", dialog)
        start_button.clicked.connect(run_zeek)
        layout.addWidget(start_button)

        dialog.exec_()

    def show_snort_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Snort Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        interface_layout = QHBoxLayout()
        interface_label = QLabel("Interface:", dialog)
        interface_input = QLineEdit(dialog)
        interface_layout.addWidget(interface_label)
        interface_layout.addWidget(interface_input)
        layout.addLayout(interface_layout)

        config_layout = QHBoxLayout()
        config_label = QLabel("Configuration File:", dialog)
        config_input = QLineEdit(dialog)
        config_layout.addWidget(config_label)
        config_layout.addWidget(config_input)
        layout.addLayout(config_layout)

        rule_file_layout = QHBoxLayout()
        rule_file_label = QLabel("Rule File:", dialog)
        rule_file_input = QLineEdit(dialog)
        rule_file_layout.addWidget(rule_file_label)
        rule_file_layout.addWidget(rule_file_input)
        layout.addLayout(rule_file_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_snort():
            interface = interface_input.text()
            config_file = config_input.text()
            rule_file = rule_file_input.text()

            command = f"snort -i {interface}"
            if config_file:
                command += f" -c {config_file}"
            if rule_file:
                command += f" -r {rule_file}"

            output_area.setText(command)
            return command

        def run_snort():
            command = generate_command_snort()
            if command:
                answer = QMessageBox.question(dialog, "Run Snort", "Do you want to run Snort? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_snort)
        layout.addWidget(generate_button)

        start_button = QPushButton("Start Snort", dialog)
        start_button.clicked.connect(run_snort)
        layout.addWidget(start_button)

        dialog.exec_()

    def show_tcpdump_options(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("TcpDump Options")
        dialog.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout(dialog)

        interface_layout = QHBoxLayout()
        interface_label = QLabel("Interface:", dialog)
        interface_input = QLineEdit(dialog)
        interface_layout.addWidget(interface_label)
        interface_layout.addWidget(interface_input)
        layout.addLayout(interface_layout)

        count_layout = QHBoxLayout()
        count_label = QLabel("Packet Count:", dialog)
        count_input = QLineEdit(dialog)
        count_layout.addWidget(count_label)
        count_layout.addWidget(count_input)
        layout.addLayout(count_layout)

        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter Expression:", dialog)
        filter_input = QLineEdit(dialog)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(filter_input)
        layout.addLayout(filter_layout)

        output_area = QTextEdit(dialog)
        output_area.setReadOnly(True)
        layout.addWidget(output_area)

        def generate_command_tcpdump():
            interface = interface_input.text()
            packet_count = count_input.text()
            filter_expression = filter_input.text()

            command = f"tcpdump -i {interface}"
            if packet_count:
                command += f" -c {packet_count}"
            if filter_expression:
                command += f" {filter_expression}"

            output_area.setText(command)
            return command

        def run_tcpdump():
            command = generate_command_tcpdump()
            if command:
                answer = QMessageBox.question(dialog, "Run TcpDump", "Do you want to run TcpDump? (Y/N)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    result = subprocess.getoutput(command)
                    output_area.append("\n" + result)

        generate_button = QPushButton("Generate Command", dialog)
        generate_button.clicked.connect(generate_command_tcpdump)
        layout.addWidget(generate_button)

        start_button = QPushButton("Start TcpDump", dialog)
        start_button.clicked.connect(run_tcpdump)
        layout.addWidget(start_button)

        dialog.exec_()

def main():
    time.sleep(1.1)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
