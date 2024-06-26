import sys
import subprocess
import sqlite3
import json
import platform
import requests
from colorama import Fore,Style

db_path = r"/tmp/commands.db"
'''
with open(db_path,"w") as file:
    file.write()
file.close()
'''
if platform.uname().system == "Linux":
    def download_tool(tool_name):
        url = "http://192.168.1.1" #writev your server_ip for tool downloading
        response = requests.get(url=url,allow_redirects=True)
        if response.status_code < 400:
            print("Tool Downloaded!")

    try:
        while True:
            user = input(Fore.RED+"Please enter a tool name: "+Style.RESET_ALL)

            tools = ["nmap","hydra","feroxbuster","enumlinux","wpscan","curl","ldapsearch","osintagram","sherlock","bettercap"]
            try:
                if user in tools:
                    if user.lower():
                        print(f"{user} options\n")
                        command = subprocess.Popen([f"{user}", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        out, err = command.communicate()
                        print(out.decode())
                        print(err.decode())
                        if "is not recognized" in err:
                            print(Fore.LIGHTYELLOW_EX + f"You can download it from https://serverip/{user}\n")
                            agreement = input(r'Do you wnat to download this tool into your system:(Y\N)')

                            if user.lower() == "Y" or "user".lower():
                                download_tool(f"{user}")
                    
                    if not user:
                        continue

                elif user.lower() == "exit":
                    print("Program finished by user!\n")
                    sys.exit(0)
                    
                else:
                    print("Try again!\n")

            except Exception as e:
                print("Your Error-->",e)
                break

    except KeyboardInterrupt:
        print("\nUser terminate the program!\n")

else:
    error = "Operating system is not Linux!"
    print(Fore.RED+error+Style.RESET_ALL)
    exit(0)
