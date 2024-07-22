from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("key.key"):
        generate_key()
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

def view(fernet):
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            user, pw = data.split(",")
            try:
                decrypted_pw = fernet.decrypt(pw.encode()).decode()
                print('Account name:', user, "Password:", decrypted_pw)
            except Exception as e:
                print('Failed to decrypt password for', user, 'Error:', str(e))

def add(fernet):
    account_name = input("What is the account name? ")
    account_pwd = input("What is the account password? ")
    with open("passwords.txt", "a") as f:
        f.write(account_name + "," + fernet.encrypt(account_pwd.encode()).decode() + "\n")

key = load_key()
fernet = Fernet(key)

master_pwd = input("What is the master password? ")

while True:
    menu = input("Add, view, or quit (view, add, quit): ").lower()

    if menu == "view":
        view(fernet)
    elif menu == "add":
        add(fernet)
    elif menu == "quit":
        print("Password manager aborted.")
        break
    else:
        print("Invalid menu selection. Please try again.")
        continue

print("Goodbye!")