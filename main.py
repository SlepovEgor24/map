import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
import requests
from PyQt6.QtCore import Qt

SCREEN_SIZE = [500, 500]
STEP = 0.01


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.dark_theme = False
        self.button = QPushButton('Тёмная тема', self)
        self.button.resize(100, 20)
        self.button.move(220, 460)
        self.button.clicked.connect(self.changing_theme)
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 450)
        self.map_size = 8
        self.server = 'http://static-maps.yandex.ru/v1'
        self.coords = '37.3712,55.4515'
        self.map()
        self.setFocus()

    def changing_theme(self):
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            self.button.setText('Светлая тема')
        else:
            self.button.setText('Тёмная тема')
        self.map()

    def map(self):
        params = {
            'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
            'll': self.coords,
            'lang': 'ru_RU',
            'size': '450,450',
            'z': str(self.map_size),
            'theme': 'dark' if self.dark_theme else 'light'
        }
        response = requests.get(self.server, params=params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(response.content)
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
        elif event.key() == Qt.Key.Key_Up:
            self.move_map(0, STEP)
        elif event.key() == Qt.Key.Key_Down:
            self.move_map(0, -STEP)
        elif event.key() == Qt.Key.Key_Left:
            self.move_map(-STEP, 0)
        elif event.key() == Qt.Key.Key_Right:
            self.move_map(STEP, 0)

    def move_map(self, dx, dy):
        lon, lat = map(float, self.coords.split(','))
        lon += dx
        lat += dy
        lon = max(min(lon, 180), -180)
        lat = max(min(lat, 85), -85)
        self.coords = f'{lon},{lat}'
        self.map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
