import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap
import requests

SCREEN_SIZE = [500, 500]


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        server = 'http://static-maps.yandex.ru/v1'
        coords = '54.35432,67.45624'
        size = '5'
        params = {
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
            'll': f'{coords}',
            'lang': 'ru_RU',
            'size': '450,450',
            'z': f'{size}'
        }
        response = requests.get(server, params=params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(0, -20)
        self.image.resize(500, 500)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())