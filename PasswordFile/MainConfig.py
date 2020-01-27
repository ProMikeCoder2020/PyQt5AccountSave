import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QComboBox
import sys
import time
import PasswordCode
from PasswordCode import MyAccount, AccountSave

sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook


class Window(QMainWindow):

    def __init__(self):  # initialize the window and set its basic properties
        super(Window, self).__init__()
        self.account_type = ""
        self.base_layout_index = 0
        self.setWindowTitle("Account Save System")
        self.account_action = None
        self.real_password = ""
        self.timer = QtCore.QTimer()
        self.central_frame = QtWidgets.QFrame(self)
        self.main_layout = QtWidgets.QStackedWidget(self.central_frame)
        self.main_layout.move(50, 50)
        self.init_ui()
        self.setCentralWidget(self.central_frame)

    def init_ui(self):  # initalize the homepage Ui and set its basic properties
        self.create_top_buttons()
        self.empty_widget = QWidget()
        self.login_system_widget = QWidget()
        self.account_actions_info_widget = QWidget()
        self.store_new_account_info_widget = QWidget()
        self.get_account_widget = QWidget()
        self.create_login_sign_system()
        self.create_account_info()
        self.new_account_info_web_app_system()
        self.get_account_info_widget()
        self.main_layout.addWidget(self.empty_widget)
        self.main_layout.addWidget(self.login_system_widget)
        self.main_layout.addWidget(self.account_actions_info_widget)
        self.main_layout.addWidget(self.store_new_account_info_widget)
        self.main_layout.addWidget(self.get_account_widget)
        self.main_layout.setCurrentIndex(self.base_layout_index)

    def create_top_buttons(self):  # creates the login and sign in buttons and set its basic properties such as text and function to be run when clicked
        self.horizontal_layout = QtWidgets.QFrame(self)
        self.horizontal_layout.setGeometry(QtCore.QRect(310, 0, 50, 50))
        self.login_buttons_layout = QtWidgets.QHBoxLayout()

        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setText("LOGIN")
        self.login_button.clicked.connect(lambda: self.login_widget_setup("login"))

        self.sign_in_button = QtWidgets.QPushButton(self)
        self.sign_in_button.setText("SIGN IN")
        self.sign_in_button.clicked.connect(lambda: self.login_widget_setup("sign_in"))

        self.login_buttons_layout.addWidget(self.login_button)
        self.login_buttons_layout.addWidget(self.sign_in_button)
        self.horizontal_layout.setLayout(self.login_buttons_layout)
        self.horizontal_layout.adjustSize()

    def create_login_sign_system(self):  # creates the system(labels and line edit[text box]) that lets the player type its password and username so it can either create an account or sign in
        self.login_layout = QtWidgets.QGridLayout()

        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setText("USERNAME:")
        self.username_type = QtWidgets.QLineEdit(self)

        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText("PASSWORD:")
        self.password_type = QtWidgets.QLineEdit(self)
        self.password_type.textChanged.connect(lambda: self.time_delay(200, self.dotted_text))

        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.clicked.connect(self.submit)

        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        self.login_layout.addWidget(self.username_label, 0, 0)
        self.login_layout.addWidget(self.password_label, 1, 0)
        self.login_layout.addWidget(self.username_type, 0, 1)
        self.login_layout.addWidget(self.password_type, 1, 1)
        self.login_layout.addWidget(self.submit_button, 2, 0)
        self.login_layout.addWidget(self.cancel_button, 2, 2)
        self.login_layout.setVerticalSpacing(50)
        self.login_system_widget.setLayout(self.login_layout)

    def create_account_info(self):
        self.account_info_action_buttons_layout = QtWidgets.QHBoxLayout()
        self.account_info_action_buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.button_new_account = QtWidgets.QPushButton("Create new account info.", self)
        self.button_new_account.clicked.connect(lambda: self.main_layout.setCurrentIndex(3))

        self.button_change_get_account_info = QtWidgets.QPushButton("Change/get account info.", self)
        self.button_change_get_account_info.clicked.connect(self.get_account_info)

        self.buttons_accounts_action = [self.button_new_account, self.button_change_get_account_info]

        self.account_info_action_buttons_layout.addWidget(self.button_new_account)
        self.account_info_action_buttons_layout.addWidget(self.button_change_get_account_info)
        self.account_info_action_buttons_layout.setSpacing(100)
        self.account_info_action_buttons_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.account_actions_info_widget.setLayout(self.account_info_action_buttons_layout)

    def new_account_info_web_app_system(self):
        layout = QtWidgets.QGridLayout()
        widget = QWidget()

        self.account_name_label = QtWidgets.QLabel()
        self.account_name_label.setText("Account Name")
        self.account_name = QtWidgets.QLineEdit()

        self.account_username_label = QtWidgets.QLabel()
        self.account_username_label.setText("Username")
        self.account_username = QtWidgets.QLineEdit()

        self.account_password_label = QtWidgets.QLabel()
        self.account_password_label.setText("Password")
        self.account_password = QtWidgets.QLineEdit()

        self.cancel__new_account = QtWidgets.QPushButton()
        self.cancel__new_account.setText("Cancel")
        self.cancel__new_account.clicked.connect(self.cancel)

        self.submit_new_account = QtWidgets.QPushButton()
        self.submit_new_account.setText("Store account info.")
        self.submit_new_account.clicked.connect(self.store_new_account_info)

        self.choose_account_type = QComboBox()
        for item in ["Web App", "Padlock"]:
            self.choose_account_type.addItem(item)
        self.choose_account_type.currentTextChanged.connect(self.change_account_type)

        layout.addWidget(self.choose_account_type, 0, 1)
        layout.addWidget(self.account_name_label, 1, 0)
        layout.addWidget(self.account_username_label, 2, 0)
        layout.addWidget(self.account_password_label, 3, 0)
        layout.addWidget(self.account_name, 1, 1)
        layout.addWidget(self.account_username, 2, 1)
        layout.addWidget(self.account_password, 3, 1)
        layout.addWidget(self.cancel__new_account, 4, 2)
        layout.addWidget(self.submit_new_account, 4, 0)
        layout.setVerticalSpacing(50)
        widget.setLayout(layout)
        self.store_new_account_info_widget.setLayout(layout)

    def get_account_info_widget(self):
        layout = QtWidgets.QGridLayout()

        self.choose_account = QComboBox()
        self.choose_account.currentTextChanged.connect(lambda:
                                                       self.update_account_get(self.choose_account.currentText()))

        self.choose_account_type_to_view = QComboBox()
        self.choose_account_type_to_view.addItem("Padlock")
        self.choose_account_type_to_view.addItem("Web App")
        self.choose_account_type_to_view.addItem("All")
        self.choose_account_type_to_view.currentTextChanged.connect(lambda: self.update_filter(self.choose_account_type_to_view.currentText()))

        self.account_name_label_get = QtWidgets.QLabel()
        self.account_name_label_get.setText("Account Name:")
        self.account_name_get = QtWidgets.QLineEdit()

        self.account_username_label_get = QtWidgets.QLabel()
        self.account_username_label_get.setText("Username:")
        self.account_username_get = QtWidgets.QLineEdit()

        self.account_password_label_get = QtWidgets.QLabel()
        self.account_password_label_get.setText("Password:")
        self.account_password_get = QtWidgets.QLineEdit()

        self.ok = QtWidgets.QPushButton()
        self.ok.setText("OK")
        self.ok.clicked.connect(self.cancel)

        self.apply_changes = QtWidgets.QPushButton()
        self.apply_changes.setText("Apply Changes")
        self.apply_changes.clicked.connect(self.change_account_info)

        layout.addWidget(self.choose_account, 0, 0)
        layout.addWidget(self.choose_account_type_to_view, 0, 1)
        layout.addWidget(self.account_name_label_get, 1, 0)
        layout.addWidget(self.account_username_label_get, 2, 0)
        layout.addWidget(self.account_password_label_get, 3, 0)
        layout.addWidget(self.account_name_get, 1, 2)
        layout.addWidget(self.account_username_get, 2, 2)
        layout.addWidget(self.account_password_get, 3, 2)
        layout.addWidget(self.ok, 4, 0)
        layout.addWidget(self.apply_changes, 4, 2)
        layout.setVerticalSpacing(50)
        self.get_account_widget.setLayout(layout)

    def login_widget_setup(self, account_action):  # changes the UI when the login button is clicked
        self.cancel()
        self.main_layout.setCurrentIndex(1)
        if account_action == "sign_in":
            self.account_action = "sign_in"
            self.submit_button.setText("Create Account")
        elif account_action == "login":
            self.account_action = "login"
            self.submit_button.setText("Open Account")

    def submit(self):  # the method run when the player logins or signs in
        if self.account_action == "login":
            if MyAccount.login(self.username_type.text(), self.real_password):
                self.login()
            else:
                self.real_password = ""
        elif self.account_action == "sign_in":
            if MyAccount.sign_in(self.username_type.text(), self.real_password):
                self.login()
            else:
                self.real_password = ""
        self.username_type.setText("")
        self.password_type.setText("")
        self.real_password = ""

    def dotted_text(self):
        if len(self.real_password) <= len(self.password_type.text()):
            self.real_password += self.password_type.text().strip(".")
        else:
            self.real_password = self.real_password[:-1]
        self.password_type.setText("." * len(self.password_type.text()))

    def time_delay(self, delay, func_name):
        self.timer.timeout.connect(func_name)
        self.timer.start(delay)

    def login(self):
        self.main_layout.setCurrentIndex(2)
        self.login_button.setText("LOG OUT")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.log_out)
        self.base_layout_index = 2

    def log_out(self):
        self.base_layout_index = 0
        self.main_layout.setCurrentIndex(0)
        self.login_button.setText("LOGIN")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(lambda: self.login_widget_setup("login"))

    def cancel(self):
        self.real_password = ""
        self.main_layout.setCurrentIndex(self.base_layout_index)
        for widget in [self.password_type, self.username_type,
                       self.account_name, self.account_password, self.account_username]:
            widget.setText("")

    def store_new_account_info(self):
        AccountSave(self.account_name.text(), self.account_password.text(), self.account_username.text(),
                    "Padlock" if self.account_type == "locker" else "Web App")
        self.cancel()

    def change_account_type(self, account_type):
        if account_type == "Web App":
            self.choose_account_type.setCurrentIndex(self.choose_account_type.findText("Web App", QtCore.Qt.MatchFixedString))
            self.account_name_label.setText("Account Name")
            self.account_username_label.setText("Username")
            self.account_password_label.setText("Password")
            self.submit_new_account.setText("Store account info")
            self.account_type = "web_app"
        elif account_type == "Padlock":
            self.choose_account_type.setCurrentIndex(self.choose_account_type.findText("Padlock", QtCore.Qt.MatchFixedString))
            self.account_name_label.setText("Locker Localization")
            self.account_username_label.setText("Locker Number")
            self.account_password_label.setText("Padlock code")
            self.submit_new_account.setText("Store padlock info")
            self.account_type = "locker"

    def get_account_info(self):
        self.main_layout.setCurrentIndex(4)
        self.choose_account.clear()
        AccountSave.filter = "All"
        self.update_filter()
        self.choose_account_type_to_view.setCurrentIndex(self.choose_account_type_to_view.findText("All", QtCore.Qt.MatchFixedString))
        self.reset_choose_account_list()

    def update_account_get(self, account_name):
        account_list = AccountSave.get_accounts()
        account_system_widgets = [self.account_username_get, self.account_password_get, self.account_name_get]

        for account in account_list:
            if account[0] == account_name:
                self.account_username_get.setText(account[2])
                self.account_password_get.setText(account[1])
                self.account_name_get.setText(account[0])

                if account[3] == "Web App":
                    self.account_username_label_get.setText("Username")
                    self.account_password_label_get.setText("Password")
                    self.account_name_label_get.setText("Account Name")
                elif account[3] == "Padlock":
                    self.account_username_label_get.setText("Locker Number")
                    self.account_password_label_get.setText("Padlock Code")
                    self.account_name_label_get.setText("Locker Localization")
            for widget in account_system_widgets:
                widget.setReadOnly(False)

        if not account_list:
            for widget in account_system_widgets:
                widget.setText("")
                widget.setReadOnly(True)
            if AccountSave.filter == "Web App":
                self.account_username_label_get.setText("Username")
                self.account_password_label_get.setText("Password")
                self.account_name_label_get.setText("Account Name")
            elif AccountSave.filter == "Padlock":
                self.account_username_label_get.setText("Locker Number")
                self.account_password_label_get.setText("Padlock Code")
                self.account_name_label_get.setText("Locker Localization")

    def update_filter(self, new_filter="Web App"):
        AccountSave.filter = new_filter
        self.reset_choose_account_list()

    def change_account_info(self):
        AccountSave.change_account_info(self.choose_account.currentText(),
                                        [self.account_name_get.text(), self.account_password_get.text(), self.account_username_get.text()])
        self.reset_choose_account_list()

    def reset_choose_account_list(self):
        self.choose_account.clear()
        for account in AccountSave.get_accounts():
            self.choose_account.addItem(account[0])

def setup_window():
    app = QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    MainWindow.setFixedSize(500, 400)
    sys.exit(app.exec_())


setup_window()


