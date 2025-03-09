import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QStackedWidget, QMessageBox
)

class ProjectWindow(QWidget):
    def __init__(self, switch_to_start, is_editing=False):
        super().__init__()
        self.is_editing = is_editing
        self.switch_to_start = switch_to_start
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад", self)
        back_button.setFixedSize(QSize(100, 25))
        back_button.clicked.connect(self.switch_to_start)
        layout.addWidget(back_button)

        self.name_input = QTextEdit()
        self.name_input.setFixedSize(QSize(300, 30))
        self.name_input.setPlaceholderText("Название")
        layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Описание проекта
        self.description_input = QTextEdit()
        self.description_input.setFixedSize(QSize(300, 30))
        self.description_input.setPlaceholderText("Описание")
        layout.addWidget(self.description_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка для сохранения
        self.save_button = QPushButton("Сохранить")
        self.save_button.setFixedSize(QSize(300, 30))
        self.save_button.clicked.connect(self.save_project)
        layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def save_project(self):
        name = self.name_input.toPlainText().strip()
        description = self.description_input.toPlainText().strip()

        if not name or not description:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        if self.is_editing:
            # Логика для изменения проекта
            QMessageBox.information(self, "Успех", f"Проект '{name}' изменен.")
        else:
            # Логика для создания нового проекта
            QMessageBox.information(self, "Успех", f"Проект '{name}' создан.")
