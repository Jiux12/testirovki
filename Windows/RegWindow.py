import pyodbc
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
)

class RegWindow(QWidget):
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.mail_input.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        if not username or not password or not email:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        if self.add_user_to_db(username, password, email):
            QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы!")
            self.switch_to_main()  # Переход на главную страницу
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось зарегистрировать пользователя.")

    def add_user_to_db(self, username, password, email):
        server = 'WIN-FIKHFSKV01H\SQLEXPRESS'  
        database = 'testirovki'  
        db_username = 'user1'  
        db_password = 'your_password'

        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={db_username};PWD={db_password}'

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Проверка, существует ли уже пользователь с таким именем
            cursor.execute("SELECT COUNT(*) FROM [User ] WHERE login = ?", (username,))
            result = cursor.fetchone()

            if result[0] > 0:
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует.")
                cursor.close()
                connection.close()
                return False

            # Вставка нового пользователя
            cursor.execute("INSERT INTO [User] (login, password, email) VALUES (?, ?, ?)", (username, password, email))
            connection.commit()  # Сохраняем изменения

            cursor.close()
            connection.close()
            return True  # Успешная регистрация
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", str(e))
            print(str(e))
            return False

    def __init__(self, switch_to_auth, switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main
        self.initUI(switch_to_auth)

    def initUI(self, switch_to_auth):
        layout = QVBoxLayout()

        back_button = QPushButton("Назад", self)
        back_button.setFixedSize(QSize(100, 25))
        back_button.clicked.connect(self.switch_to_main)
        layout.addWidget(back_button)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setFixedSize(QSize(300, 30))
        self.username_input.setMaxLength(50)
        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setFixedSize(QSize(300, 30))
        self.password_input.setMaxLength(50)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setFixedSize(QSize(300, 30))
        self.confirm_password_input.setMaxLength(50)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mail_input = QLineEdit(self)
        self.mail_input.setPlaceholderText("Почта")
        self.mail_input.setFixedSize(QSize(300, 30))
        self.mail_input.setMaxLength(100)
        layout.addWidget(self.mail_input, alignment=Qt.AlignmentFlag.AlignCenter)

        register_button = QPushButton("Зарегистрироваться", self)
        register_button.setFixedSize(QSize(200, 25))
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        auth_button = QPushButton("Войти", self)
        auth_button.setFixedSize(QSize(200, 25))
        auth_button.clicked.connect(switch_to_auth)
        layout.addWidget(auth_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    