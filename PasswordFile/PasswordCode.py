import time
import random
import os
from PyQt5.QtWidgets import QMessageBox

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'Accounts')


class MyAccount(object):
    currentAccount = None

    def __init__(self, password, username, account_save_filename):
        self.password = password
        self.username = username
        self.account_save_file = account_save_filename

    @classmethod
    def login(cls, username, password):
        with open(filename, "r+") as accounts_file:
            accounts_list = accounts_file.readlines()[1:]
        username_list = []
        password_list = []
        file_name_list = []
        for line in accounts_list:
            username_list.append(line.split("/")[0])
            password_list.append(line.split("/")[1])
            file_name_list.append(line.split("/")[2])

        msg = QMessageBox()
        msg.setWindowTitle("Login")
        try:
            if username_list.index(username) == password_list.index(password) and username in \
                    username_list and password in password_list:
                cls.currentAccount = MyAccount(password, username, file_name_list[username_list.index(username)])
                msg.setText("You have open your account!")
                msg.setIcon(QMessageBox.Information)

                msg.exec_()
                return True
            else:
                raise ValueError()
        except ValueError:
            msg.setText("There was an error during login!")
            msg.setInformativeText("Please retry!")
            msg.setIcon(QMessageBox.Warning)
            msg.setDetailedText("You are either not typing the corresponding password to the username "
                                "you typed or this account does not even exist.")
            msg.exec_()
            return False

    @classmethod
    def sign_in(cls, new_username, new_password):
        with open(filename, "a+") as accounts_file:
            accounts_file.write("\n")
            accounts_file.write(f"{new_username}/{new_password}/{(random.randint(6789, 109670))}.txt")
        return cls.login(new_username, new_password)


class AccountSave(object):
    """"
    :parameter: Account Password, Account, Account username
    :action:None
    """""
    filter = "Web App"

    def __init__(self, web_app,  password, username, account_type):
        self.password = password
        self.web_app = web_app
        self.username = username
        self.info = [self.web_app, self.username, self.password, account_type]
        with open(MyAccount.currentAccount.account_save_file.strip("\n"), "a+") as password_file:
            password_file.write("\n")
            for atr in self.info:
                password_file.write(atr + "///")

    @classmethod
    def get_accounts(cls):
        list_of_accounts = []
        with open(MyAccount.currentAccount.account_save_file.strip("\n"), "a+") as password_file:
            password_file.seek(0)
            for line in password_file.readlines()[1:]:
                if line.split("///")[3] == cls.filter or cls.filter == "All":
                    list_of_accounts.append(line.split("///"))
        return list_of_accounts

    @classmethod
    def change_account_info(cls, account_name, new_line):
        with open(MyAccount.currentAccount.account_save_file.strip("\n"), "r+") as account_info_file:
            for line_number, line in enumerate(account_info_file.readlines()):
                if account_name == line.split("///")[0]:
                    account_info_file.seek(0)
                    text = account_info_file.readlines()
                    print(f"line_number {line_number}")
                    print(str("///".join(new_line)) + "new_line")
                    text[line_number] = "///".join(new_line)
                    print(f"line_number {text}")
                    account_info_file.writelines(text)
                    break












