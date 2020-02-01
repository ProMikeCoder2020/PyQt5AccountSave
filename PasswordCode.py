import random
from PyQt5.QtWidgets import QMessageBox
import Encryption_System


class MyAccount(object):
    currentAccount = None

    def __init__(self, password, username, account_save_filename, key):
        self.password = password
        self.username = username
        self.account_save_file = account_save_filename
        self.key = key

    @classmethod
    def login(cls, username, password):
        msg = QMessageBox()
        with open("Accounts", "a+") as accounts_file:
            accounts_file.seek(0)
            accounts_list = accounts_file.readlines()
        username_list = []
        password_list = []
        file_name_list = []
        key_list = []
        for line in accounts_list:
            username_list.append(Encryption_System.decode_string(line.split("/")[0], 4))
            password_list.append(Encryption_System.decode_string(line.split("/")[1], 4))
            file_name_list.append(int(Encryption_System.decode_string(line.split("/")[2], 4)))
            key_list.append(int(Encryption_System.decode_string(line.split("/")[3], 4)))

        msg.setWindowTitle("Login")
        try:
            if username_list.index(username) == password_list.index(password) and username in \
                    username_list and password in password_list:
                if username_list.count(username) == 1:
                    cls.currentAccount = MyAccount(password, username, file_name_list[username_list.index(username)], key_list[username_list.index(username)])
                    cls.change_current_account_file_text(username, password)
                    msg.setText("You have open your account!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    return True
            else:
                msg.setText("Please choose another username.")
                msg.setIcon(QMessageBox.Warning)
                msg.setDetailedText("You need to change your username, "
                                    "because another account that uses this computer already has this username.")
                msg.exec_()
                return False

        except ValueError as e:
            msg.setText("There was an error during login!")
            msg.setInformativeText("Please retry!")
            msg.setIcon(QMessageBox.Warning)
            msg.setDetailedText("You are either not typing the corresponding password to the username "
                                "you typed or this account does not even exist.")
            print(e)
            msg.exec_()
            return False
        cls.currentAccount.account_save_file = str(cls.currentAccount.account_save_file) + ".txt"

    @classmethod
    def sign_in(cls, new_username, new_password):
        with open("Accounts", "a+") as accounts_file:
            try:
                accounts_file.write(f"{Encryption_System.encode_string(new_username, 4)}/{Encryption_System.encode_string(new_password, 4)}/{Encryption_System.encode_string(str(random.randint(6789, 109670)) , 4)}/{Encryption_System.encode_string(str(random.randint(0, 10000000000000)), 4)}")
                accounts_file.write("\n")
            except ValueError as e:
                return False
        return cls.login(new_username, new_password)

    @classmethod
    def get_current_account(cls):
        try:
            with open("current_account.txt", "x"):
                return False
        except FileExistsError:
            with open("current_account.txt", "r") as current_account_file:
                current_account_file.seek(0)
                text = current_account_file.readline()
                if len(text) > 0:
                    cls.login(Encryption_System.decode_string(text.split("///")[0], 4), Encryption_System.decode_string(text.split("///")[1], 4))
                    return True
                else:
                    return False

    @classmethod
    def change_current_account_file_text(cls, username, password):
        with open("current_account.txt", "w") as current_account_file:
            current_account_file.write(f"{Encryption_System.encode_string(username, 4)}///{Encryption_System.encode_string(password, 4)}")


class AccountSave(object):
    """"
    :parameter: Account Password, Account name, Account username
    :action:None
    """""
    filter = "Web App"

    def __init__(self, win,  web_app,  password, username, account_type):
        with open(str(MyAccount.currentAccount.account_save_file).strip("\n"), "a+") as password_file:
            try:
                encrypted_account_name = Encryption_System.encode_string(web_app, MyAccount.currentAccount.key)
                encrypted_password = Encryption_System.encode_string(password, MyAccount.currentAccount.key)
                encrypted_username = Encryption_System.encode_string(username, MyAccount.currentAccount.key)
                button_reply = QMessageBox.question(win, "Information", "Do you want to store this account info?", QMessageBox.Yes|QMessageBox.No)
                if button_reply == QMessageBox.Yes:
                    password_file.write(
                        f"{encrypted_account_name}///{encrypted_password}///{encrypted_username}///{Encryption_System.encode_string(account_type, MyAccount.currentAccount.key)}///\n")
                else:
                    self.aborted_action()
            except ValueError:
                pass

    @classmethod
    def get_accounts(cls):
        list_of_accounts = []
        with open(str(MyAccount.currentAccount.account_save_file).strip("\n"), "a+") as password_file:
            password_file.seek(0)
            for line in password_file.readlines():
                if Encryption_System.decode_string(line.split("///")[3], MyAccount.currentAccount.key).strip("\n") \
                        == cls.filter or cls.filter == "All":
                    new_line = []
                    for atr in line.split("///"):
                        new_line.append(Encryption_System.decode_string(atr, MyAccount.currentAccount.key))
                    list_of_accounts.append(new_line)
        return list_of_accounts

    @classmethod
    def change_account_info(cls, win, account_name, new_line):
        with open(str(MyAccount.currentAccount.account_save_file).strip("\n"), "r") as account_info_file:
            account_info_file.seek(0)
            text = account_info_file.readlines()
            account_info_file.seek(0)
            button_reply = QMessageBox.question(win, "Information", "Do you want to apply changes to  this account info?",
                                                QMessageBox.Yes | QMessageBox.No)
            if button_reply == QMessageBox.Yes:
                for line_number, line in enumerate(account_info_file.readlines()):
                    try:
                        if Encryption_System.encode_string(account_name, MyAccount.currentAccount.key) == line.split("///")[0]:
                            text[line_number] = "///".join(new_line + [line.split("///")[3]] + ["\n"])
                    except IndexError:
                        pass
            else:
                cls.aborted_action()
        with open(str(MyAccount.currentAccount.account_save_file).strip("\n"), "w") as account_info_filew:
            account_info_filew.writelines(text)

    @classmethod
    def aborted_action(cls):
        msg = QMessageBox()
        msg.setText("Action aborted!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()









