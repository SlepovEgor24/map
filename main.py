import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap
import requests
from PyQt6.QtCore import Qt

SCREEN_SIZE = [500, 500]


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(0, -20)
        self.image.resize(500, 500)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)
        self.map_size = 8
        self.server = 'http://static-maps.yandex.ru/v1'
        self.coords = '37.3712,55.4515'
        self.map()

    def map(self):
        params = {
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
            'll': f'{self.coords}',
            'lang': 'ru_RU',
            'size': '450,450',
            'z': f'{self.map_size}'
        }
        response = requests.get(self.server, params=params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            if self.map_size != 0:
                self.map_size -= 1
                self.map()
            else:
                print('Достигнут предел по размеру')
        elif event.key() == Qt.Key.Key_PageUp:
            if self.map_size != 21:
                self.map_size += 1
                self.map()
            else:
                print('Достигнут предел по размеру')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())