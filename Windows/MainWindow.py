import pyodbc
import time
from Windows.RegWindow import RegWindow
from Windows.AuthWindow import AuthWindow
from Windows.StartWindow import StartWindow
from Windows.ProjectWindow import ProjectWindow
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal, QEvent
from g4f.client import Client
from PyQt6.QtWidgets import ( 
    QStackedWidget, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QListWidget, QMessageBox,
    QSpacerItem, QSizePolicy, QListWidgetItem
)

server = 'WIN-FIKHFSKV01H\SQLEXPRESS'  
database = 'testirovki'  
username = 'user1'  
password = 'your_password'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

system_prompt="""
    Ты используешься в приложении для написания тестовых сценариев и автоматизации тестирования. 
    В завимости от запроса пользователя прописывай тесты, тестовые сценарии, тестовые данные, отчеты о выполнении тестирования и тд.
    """
 

class Worker(QThread):
    response_received = pyqtSignal(str, float)

    def __init__(self, message, us_promt):
        super().__init__()
        self.message = message
        self.us_promt = us_promt

    def run(self):
        client = Client()
        start_time = time.time()
        response = client.chat.completions.create(
            stream=False,
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": self.us_promt},
                {"role": "user", "content": self.message}
            ],
            web_search=False
        )
        end_time = time.time()
        delay = end_time - start_time
        rec_msg = response.choices[0].message.content
        self.response_received.emit(rec_msg, delay)
        print(rec_msg)

class MainWindow(QMainWindow):
    def send_message(self):
        us_message = self.input_text.toPlainText()
        us_promt = self.input_promt.toPlainText()
        
        if not us_message.strip():
            QMessageBox.information(self, "Ошибка", f"Отправленный текст пуст")
            return

        self.chat_list.append(f"Вы: {us_message}\n")
        # item = QListWidgetItem()
        # self.chat_list.addItem(item)
        
        # label = QLabel(us_message)
        # label.setWordWrap(True)  
        # label.adjustSize()
        # user_height = max(15, label.height() + 15) 
        # item.setSizeHint(QSize(300, user_height))
        # label.setStyleSheet("""
        #     background-color: #EEEEEE;
        #     padding: 10;
        #     """)
        # self.chat_list.setItemWidget(item, label)
        self.input_text.setEnabled(False)
        self.input_text.clear()

        # Запускаем асинхронный процесс
        self.worker = Worker(us_message, us_promt)
        self.worker.response_received.connect(self.handle_response)
        self.worker.start()

    def eventFilter(self, source, event):
        if source is self.input_text and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.send_message()  # Вызываем метод отправки сообщения
                return True  # Указываем, что событие обработано
        return super().eventFilter(source, event)

    def handle_response(self, response, delay):
        self.time_ms_label.setText(f"Время отклика: {delay:.3f}")

        self.chat_list.append(f"ИИ: {response}\n")
        # ai_item = QListWidgetItem()
        # self.chat_list.addItem(ai_item)
        
        # ai_label = QLabel(response)
        # ai_label.setWordWrap(True)  # Включаем перенос слов
        # ai_label.adjustSize()
        # ai_height = max(15, ai_label.sizeHint().height() + 15)
        # ai_item.setSizeHint(QSize(300, ai_height))
        # ai_label.setStyleSheet("""
        #     background-color: #D6D6D6;
        #     padding: 10;
        #     """)
        # self.chat_list.setItemWidget(ai_item, ai_label)

        self.input_text.setEnabled(True)
        # self.chat_list.scrollToBottom()

    def switch_to_main(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def switch_to_register(self):
        self.stacked_widget.setCurrentWidget(self.register_window)

    def switch_to_auth(self):
        self.stacked_widget.setCurrentWidget(self.auth_window)

    def switch_to_start(self):
        self.stacked_widget.setCurrentWidget(self.start_window)

    def switch_to_project_c(self):
        self.stacked_widget.setCurrentWidget(self.project_window_c)

    def switch_to_project_e(self):
        self.stacked_widget.setCurrentWidget(self.project_window_e)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Window')
        self.setMinimumSize(QSize(700, 550))

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.start_window = StartWindow(self.switch_to_main, self.switch_to_auth, self.switch_to_start, self.switch_to_project_c, self.switch_to_project_e)
        self.stacked_widget.addWidget(self.start_window)

        # Главный макет
        self.main_page = QWidget()
        self.main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        main_layout_1 = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Верхний горизонтальный макет
        header_layout = QHBoxLayout()
        header_layout.setDirection(QHBoxLayout.Direction.RightToLeft)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.switch_to_start)
        header_layout.addWidget(back_button)
        profile_button = QPushButton("Профиль")
        profile_button.clicked.connect(self.switch_to_auth)

        header_layout.addWidget(profile_button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        header_layout.addItem(spacer)

        # Левый вертикальный макет для списка
        left_layout = QVBoxLayout()
        font1 = QFont("Arial", 16)
        font2 = QFont("Arial", 12)
        text_nazv = QLabel("Проект 1")
        text_nazv.setFont(font1)
        left_layout.addWidget(text_nazv)
        text_opis = QLabel("Описание проекта")
        text_opis.setFont(font2)
        left_layout.addWidget(text_opis)

        text_promt = QLabel("Конфигурация")
        text_promt.setFont(font2)
        text_promt.setContentsMargins(0,15,0,0)
        left_layout.addWidget(text_promt)

        self.input_promt = QTextEdit("""Формат вводных данных:\n
        Параметр 1: \n
        Параметр 2: \n
        \n  
        Продолжай вводные данные в таком же формате
        """)
        self.input_promt.setFixedWidth(250)
        self.input_promt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        left_layout.addWidget(self.input_promt)

        spacer_vertical = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        left_layout.addItem(spacer_vertical)

        right_layout = QVBoxLayout()
        # self.chat_list = QListWidget()
        self.chat_list = QTextEdit()
        self.chat_list.setReadOnly(True)
        self.chat_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        right_layout.addWidget(self.chat_list)

        # Основной снизу горизонтальный макет для ввода и кнопки
        input_layout = QHBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(40)
        self.input_text.installEventFilter(self)
        # load_button = QPushButton("Загрузить файл")
        # load_button.setFixedHeight(40)
        send_button = QPushButton("Отправить")
        send_button.setFixedHeight(40)
        send_button.clicked.connect(self.send_message)

        # input_layout.addWidget(load_button)
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(send_button)

        right_layout.addLayout(input_layout)

        # Основной макет
        main_layout_1.addLayout(left_layout)
        main_layout_1.addLayout(right_layout)

        font = QFont("Arial", 8, 10, 1)
        self.time_ms_label = QLabel("Время отклика")
        self.time_ms_label.setFont(font)
        self.time_ms_label.setContentsMargins(5,0,10,0)
        online_label = QLabel("Онлайн")
        online_label.setFont(font)
        online_label.setContentsMargins(0,0,10,0)
        bottom_layout.addWidget(self.time_ms_label)
        bottom_layout.addWidget(online_label)

        spacer_horizontal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        bottom_layout.addItem(spacer_horizontal)

        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(main_layout_1)
        self.main_layout.addLayout(bottom_layout)

        self.main_page.setLayout(self.main_layout)

        self.auth_window = AuthWindow(self.switch_to_register, self.switch_to_main)
        self.register_window = RegWindow(self.switch_to_auth, self.switch_to_main)

        self.project_window_c = ProjectWindow(self.switch_to_start, False)
        self.project_window_e = ProjectWindow(self.switch_to_start, True)

        self.stacked_widget.addWidget(self.auth_window)
        self.stacked_widget.addWidget(self.register_window)
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.project_window_c)
        self.stacked_widget.addWidget(self.project_window_e)