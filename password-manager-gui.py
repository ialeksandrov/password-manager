import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Manager")

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.resize(100, 32)
        self.generate_button.move(170, 50)

        self.save_button = QPushButton("Save", self)
        self.save_button.resize(100, 32)
        self.save_button.move(290, 50)

        self.list_saved_button = QPushButton("List saved", self)
        self.list_saved_button.resize(100, 32)
        self.list_saved_button.move(410, 50)

        self.list_all_button = QPushButton("List all", self)
        self.list_all_button.resize(100, 32)
        self.list_all_button.move(530, 50)

        self.remove_button = QPushButton("Remove", self)
        self.remove_button.resize(100, 32)
        self.remove_button.move(650, 50)

        self.add_custom_button = QPushButton("Add", self)
        self.add_custom_button.resize(100, 32)
        self.add_custom_button.move(50, 50)

        self.textbox = QLineEdit(self)
        self.textbox.move(50,   100)
        self.textbox.resize(700, 200)

        self.setFixedSize(QSize(800, 350))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()