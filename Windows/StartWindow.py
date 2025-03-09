from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import ( 
    QStackedWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, 
    QLabel, QLineEdit, QListWidget, QMessageBox, QListWidgetItem
)

class StartWindow(QWidget):
    # def load_for_e(self):
    #     current_item = self.project_list.currentItem()
    #     if current_item:
    #         name = current_item.text()
    #         description = current_item.data(Qt.ItemDataRole.UserRole)

    #     self.project_window_e.name_input.setPlainText(name)
    #     self.project_window_e.description_input.setPlainText(description)

    def on_item_double_clicked(self, item):
        if item.text().startswith(""):
            self.switch_to_main()
        else:
            QMessageBox.information(self, "Информация", f"Вы выбрали: {item.text()}")

    def __init__(self, switch_to_main, switch_to_auth, switch_to_start, switch_to_project_c, switch_to_project_e):
        super().__init__()
        self.switch_to_main = switch_to_main
        self.switch_to_start = switch_to_start
        self.switch_to_project_c = switch_to_project_c
        self.switch_to_project_e = switch_to_project_e
        self.initUI(switch_to_auth)

    def initUI(self, switch_to_auth):
        self.setWindowTitle('Testing Studio')
        self.setFixedSize(QSize(700, 550))

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout_1 = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20,20,20,20)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(20,20,20,20)

        main_layout_1.addLayout(left_layout)
        main_layout_1.addLayout(right_layout)

        # Заголовок
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20,20,0,0)
        font = QFont("Arial", 20)
        title = QLabel("Testing studio")
        title.setFont(font)
        header_layout.addWidget(title)

        # Поле поиска
        search_box = QLineEdit()
        search_box.setPlaceholderText('Поиск')
        search_box.setFixedSize(QSize(250, 25))
        header_layout.addWidget(search_box)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(main_layout_1)

        # Список проектов
        self.project_list = QListWidget()
        item = QListWidgetItem("Проект 1")
        item.setData(Qt.ItemDataRole.UserRole,"Описание 1")
        item2 = QListWidgetItem("Проект 2")
        item2.setData(Qt.ItemDataRole.UserRole,"Описание 2")
        self.project_list.addItem(item2)
        self.project_list.addItem(item)
        # self.project_list.itemClicked.connect(self.load_for_e)
        self.project_list.itemDoubleClicked.connect(self.on_item_double_clicked)

        left_layout.addWidget(self.project_list)

        # Кнопки
        create_project_button = QPushButton('Создать проект')
        edit_project_button = QPushButton('Изменить проект')
        delete_project_button = QPushButton('Удалить проект')
        login_button = QPushButton('Войти в аккаунт')
        login_button.clicked.connect(switch_to_auth)

        create_project_button.clicked.connect(self.switch_to_project_c)
        # edit_project_button.clicked.connect(self.switch_to_project_e)
        # delete_project_button.clicked.connect(self.d_project_clicked)

        right_layout.addWidget(create_project_button)
        right_layout.addWidget(edit_project_button)
        right_layout.addWidget(delete_project_button)
        right_layout.addWidget(login_button)

        self.setLayout(main_layout)