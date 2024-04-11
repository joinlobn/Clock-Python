from os import system
from math import (sin, cos, pi)
import sys
from playsound import playsound
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    """
        application main window;
    """

    WIDTH = 380
    HEIGHT = 450
    STYLESHEET = """
        background-color: #282828;
    """
    TITLE = "Analog Clock"

    OPACITY = 0.98

    CANVAS_BACKGROUND_COLOR = QColor(247, 247, 247, 255)
    LABEL_STYLESHEET = """
        background-color: #9e91e8;
        border-radius: 10px;
    """

    CONTEXT_MENU_STYLESHEET = """

        QMenu{
            background-color: #282828;
            border-radius: 5px;
        }

    """

    RADIUS = 300

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(MainWindow.WIDTH, MainWindow.HEIGHT)
        self.setWindowTitle(MainWindow.TITLE)
        self.setStyleSheet(MainWindow.STYLESHEET)
        self.setWindowOpacity(MainWindow.OPACITY)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.canvas = QPixmap(MainWindow.WIDTH - 20, MainWindow.HEIGHT - 100)
        self.canvas.fill(MainWindow.CANVAS_BACKGROUND_COLOR)

        self.label = QLabel(parent=self)
        self.label.setPixmap(self.canvas)
        self.label.setFixedSize(MainWindow.WIDTH, MainWindow.HEIGHT - 50)
        self.label.setStyleSheet(MainWindow.LABEL_STYLESHEET)

        self.label.move(0, 10)

        self.__seconds_angle = 0
        self.__minutes_angle = 0
        self.__hours_angle = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        self.timer.start(970)

        self.tick()

    def paintEvent(self, e):
        """
            draw the circle frame and the numbers;
            and draw the center dot of the clock;

            return None;
        """

        NUMBER_RADIUS = MainWindow.RADIUS - 30

        pen = QPen()
        pen.setWidth(4)
        painter = QPainter(self.label.pixmap())
        painter.setPen(pen)
        painter.drawEllipse((self.canvas.width() - MainWindow.RADIUS) // 2,
                            (self.canvas.height() - MainWindow.RADIUS) // 2, MainWindow.RADIUS, MainWindow.RADIUS)

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        painter.setFont(font)

        angle = 0
        hour = 3

        for _ in range(12):

            if hour > 12:
                hour = 1

            painter.drawText(int(NUMBER_RADIUS//2 * cos(angle * pi / 180)) + (NUMBER_RADIUS + 75) // 2,
                             int(NUMBER_RADIUS//2 * sin(angle * pi / 180)
                                 ) + (NUMBER_RADIUS + 100) // 2,
                             f"{hour}")
            angle += 30
            hour += 1

        center_pen = QPen()
        center_pen.setWidth(8)
        center_pen.setColor(Qt.red)
        painter.setPen(center_pen)
        painter.drawEllipse((self.canvas.width() - MainWindow.RADIUS) // 2 + MainWindow.RADIUS//2,
                            (self.canvas.height() - MainWindow.RADIUS) // 2 +
                            MainWindow.RADIUS//2,
                            5,
                            5)

        painter.end()

    def contextMenuEvent(self, e):
        """
            context menu event;

            return None;
        """

        menu = QMenu(self)

        menu.setStyleSheet(MainWindow.CONTEXT_MENU_STYLESHEET)
        menu.setCursor(QCursor(Qt.PointingHandCursor))

        edit_action = menu.addAction("Edit")
        quit_action = menu.addAction("Quit")

        action = menu.exec(self.mapToGlobal(e.pos()))

        if action == quit_action:
            sys.exit(0)

    def draw_clock_hand(self, degree: int, hand_length: int = 0):
        """
            draw the line for clock hands.

            return None;
        """

        degree *= (pi / 180)

        MAX_HAND_LENGTH = 150

        hand_length %= MAX_HAND_LENGTH

        circle_center_x = self.canvas.width() // 2
        circle_center_y = self.canvas.height() // 2

        pen = QPen()
        pen.setWidth(4)
        painter = QPainter(self.label.pixmap())
        painter.setPen(pen)

        x1 = circle_center_x + 3
        y1 = circle_center_y + 3
        x2 = circle_center_x - int(hand_length * cos(degree))
        y2 = circle_center_y - int(hand_length * sin(degree))

        painter.drawLine(x1, y1, x2, y2)

        painter.end()

        return None

    def clear_canvas(self):
        """
            clear the canvas and fill it with the basic color;

            return None;
        """

        self.label.pixmap().fill(MainWindow.CANVAS_BACKGROUND_COLOR)

        return None

    def tick(self):
        """
            timeout event when the timer get 1 second;

            return None;
        """

        self.clear_canvas()

        self.draw_clock_hand(self.__seconds_angle, hand_length=135)
        self.draw_clock_hand(self.__minutes_angle, hand_length=110)
        self.draw_clock_hand(self.__hours_angle, hand_length=80)

        self.__seconds_angle += 6

        if self.__seconds_angle > 360:
            self.__seconds_angle = 0
            self.__minutes_angle += 6

        if self.__minutes_angle > 360:
            self.__minutes_angle = 0
            self.__hours_angle += 30

        self.update()

        playsound(r"./assets/tick.mp3")

        return None


def main():
    app = QApplication(sys.argv)

    root = MainWindow()

    root.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
