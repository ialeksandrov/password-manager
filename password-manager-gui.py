import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")

        generate_button = QPushButton("Generate", self)
        generate_button.resize(100, 32)
        generate_button.move(170, 300)

        save_button = QPushButton("Save", self)
        save_button.resize(100, 32)
        save_button.move(290, 300)

        list_saved_button = QPushButton("List saved", self)
        list_saved_button.resize(100, 32)
        list_saved_button.move(410, 300)

        list_all_button = QPushButton("List all", self)
        list_all_button.resize(100, 32)
        list_all_button.move(530, 300)

        remove_button = QPushButton("Remove", self)
        remove_button.resize(100, 32)
        remove_button.move(650, 300)

        add_custom_button = QPushButton("Add", self)
        add_custom_button.resize(100, 32)
        add_custom_button.move(50, 300)

        self.textbox = QLineEdit(self)
        self.textbox.move(50, 350)
        self.textbox.resize(700, 200)

        self.setFixedSize(QSize(800, 600))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()