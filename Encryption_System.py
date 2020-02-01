import PyQt5
from PyQt5.QtWidgets import QMessageBox
import sys

sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook
"""""
This file stores functions
for encoding and decoding
a string in Python.
"""
constant_shift_amount = 23

"""""
The function that encodes the strings.
:param-string to be encrypted(only letters);the shift amount(int)
:return-string encoded
"""


def encode_string(string, shift_amount):
    new_string = "" #the variable that stores the resulting string and thus the output
    for letter in string:#each letter will be encoded separetely
        if letter not in ["/", "#", "$"]:
            new_string += str((ord(letter) + shift_amount) * constant_shift_amount)
            new_string += "#$#"
        else:
            messagebox = QMessageBox()
            messagebox.setText("You are using an invalid symbol such as \, # or $.")
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.exec_()
            raise ValueError("Invalid Symbol")
    return new_string

def decode_string(string, shift_amount):#this function decodes a string encoded by the previous function
    new_string = ""
    for letter_encoded in string.split("#$#"):
        try:
            new_string += chr(int(int(letter_encoded) / constant_shift_amount - shift_amount))
        except ValueError:
            pass
    return new_string

