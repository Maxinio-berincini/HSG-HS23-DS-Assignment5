import os
import subprocess
import requests

def start_servers_windows():
    os.chdir("bin")
    for i in range(3):
        subprocess.Popen(f"start cmd /c .\\create_server{i}.bat", shell=True)
    os.chdir("..")

# bi mer nöd sicher öb das so au funktioniert für mac und linux
def start_servers_mac_linux():
    os.chdir("bin")
    for i in range(3):
        subprocess.Popen([f"chmod", "+x", "create_server{i}.sh"])
        subprocess.Popen([f"./create_server{i}.sh"], shell=True)
    os.chdir("..")


def put_operation():
    url = 'http://localhost:8080/keys/a'
    data = {
        "type": "PUT",
        "value": ["cat", "dog"]
    }
    response = requests.post(url, json=data)
    return response.text


def append_operation():
    url = 'http://localhost:8080/keys/a'
    data = {
        "type": "APPEND",
        "value": "mouse"
    }
    response = requests.post(url, json=data)
    return response.text


def get_operation():
    url = 'http://localhost:8080/keys/a'
    response = requests.get(url)
    return response.text


def get_status():
    url = 'http://localhost:8080/admin/status'
    response = requests.get(url)
    return response.text


def main():
    print("Select your OS: 1. Windows 2. Mac/Linux")
    os = input("Enter your OS 1/2: ")
    if os == "1":
        start_servers_windows()
    elif os == "2":
        start_servers_mac_linux()

    print("PUT Response:", put_operation())
    print("Append Response:", append_operation())
    print("GET Response:", get_operation())
    print("Status:", get_status())


if __name__ == '__main__':
    main()
