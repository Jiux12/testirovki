# 

# 
# print(response.choices[0].message.content)

import sys

from Windows.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())