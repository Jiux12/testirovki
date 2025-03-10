import pyodbc
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
)

class AuthWindow(QWidget):
    def __init__(self, switch_to_register, switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main
        self.initUI(switch_to_register)

    def initUI(self, switch_to_register):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад", self)
        back_button.setFixedSize(QSize(100, 25))
        back_button.clicked.connect(self.switch_to_main)
        layout.addWidget(back_button)

        self.username_input = QLineEdit(self)
        self.username_input.setFixedSize(QSize(300, 30))
        self.username_input.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setFixedSize(QSize(300, 30))
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        login_button = QPushButton("Войти", self)
        login_button.setFixedSize(QSize(200, 25))
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        register_button = QPushButton("Регистрация", self)
        register_button.setFixedSize(QSize(200, 25))
        register_button.clicked.connect(switch_to_register)
        layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username != "" and password != "":
            if self.verify_user(username, password):
                QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                self.switch_to_main()  # Переход на главную страницу
            else:
                QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")
        else:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

    def verify_user(self, username1, password1):
        server = 'WIN-FIKHFSKV01H\SQLEXPRESS'  
        database = 'testirovki'  
        username = 'user1'  
        password = 'your_password'

        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM [User] WHERE login = ? AND password = ?", (username1, password1))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return result[0] > 0  # Возвращаем True, если пользователь найден
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", str(e))
            print(str(e))
            return False