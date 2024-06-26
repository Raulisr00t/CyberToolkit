import sys
import subprocess
import sqlite3
import json
from colorama import Fore,Style

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
