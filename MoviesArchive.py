# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QDesktopWidget
from PyQt5.QtGui import QFont, QIcon, QCursor
from PyQt5.QtCore import Qt
from DataQuery import get_movies_info, get_directors_info, get_sorted_genres_info, get_starring_info
from MoviesPage import MoviesDisplay
from GenresPage import GenresDisplay
from DirectorsPage import DirectorsDisplay
from StarringPage import StarsDisplay
from AdvancedSearch import AdvancedSearch
import sys

class MoviesArchive(QWidget):

    def __init__(self):
        self.movies_info = get_movies_info()
        super().__init__()
        self.initUI()

    def initUI(self):
        self.allSheet = 'QPushButton{background-color:#1C1C1C; color:#E8E8E8; font-size:20px; height: 64px; width: 80px;}' \
                        'QPushButton:hover{background-color:#CDC5BF; color:#4F4F4F; font-size:20px; height: 64px; width: 80px;}' \
                        'QPushButton:pressed{font-weight:bold;background-color:#C0FF3E; color:#458B00; font-size:20px; height: 64px; width: 80px;}'

        self.advancedSheet = 'QPushButton{background-color:#1C1C1C; color:#E8E8E8; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:hover{background-color:#CDC5BF; color:#4F4F4F; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:pressed{font-weight:bold;background-color:#DA70D6; color:#8B0A50; font-size:20px; height: 64px; width: 80px;}'

        self.categorySheet = 'QPushButton{background-color:#1C1C1C; color:#E8E8E8; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:hover{background-color:#CDC5BF; color:#4F4F4F; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:pressed{font-weight:bold;background-color:#CD2626; color:#FFC0CB; font-size:20px; height: 64px; width: 80px;}'

        self.directorSheet = 'QPushButton{background-color:#1C1C1C; color:#E8E8E8; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:hover{background-color:#CDC5BF; color:#4F4F4F; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:pressed{font-weight:bold;background-color:#9A32CD; color:#B0E2FF; font-size:20px; height: 64px; width: 80px;}'

        self.starringSheet = 'QPushButton{background-color:#1C1C1C; color:#E8E8E8; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:hover{background-color:#CDC5BF; color:#4F4F4F; font-size:20px; height: 64px; width: 80px;}' \
                             'QPushButton:pressed{font-weight:bold;background-color:#FFFF00; color:#556B2F; font-size:20px; height: 64px; width: 80px;}'

        self.allButton = QPushButton('所有电影', self)
        self.allButton.setStyleSheet(self.allSheet)
        self.allButton.setFont(QFont('幼圆'))
        self.allButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.allButton.clicked[bool].connect(self.LbResponse)

        self.advancedSearchBtn = QPushButton('高级搜索', self)
        self.advancedSearchBtn.setStyleSheet(self.advancedSheet)
        self.advancedSearchBtn.setFont(QFont('幼圆'))
        self.advancedSearchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.advancedSearchBtn.clicked[bool].connect(self.LbResponse)

        self.categoryButton = QPushButton('分类', self)
        self.categoryButton.setFont(QFont('幼圆'))
        self.categoryButton.setStyleSheet(self.categorySheet)
        self.categoryButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.categoryButton.clicked[bool].connect(self.LbResponse)

        self.directorButton = QPushButton('导演', self)
        self.directorButton.setFont(QFont('幼圆'))
        self.directorButton.setStyleSheet(self.directorSheet)
        self.directorButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.directorButton.clicked[bool].connect(self.LbResponse)

        self.celebButton = QPushButton('主演', self)
        self.celebButton.setFont(QFont('幼圆'))
        self.celebButton.setStyleSheet(self.starringSheet)
        self.celebButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.celebButton.clicked[bool].connect(self.LbResponse)

        self.btnBox = QVBoxLayout()
        self.btnBox.addWidget(self.allButton)
        self.btnBox.addWidget(self.advancedSearchBtn)
        self.btnBox.addWidget(self.categoryButton)
        self.btnBox.addWidget(self.directorButton)
        self.btnBox.addWidget(self.celebButton)
        self.btnBox.setSpacing(20)

        self.lFrame = QFrame()
        self.lFrame.setLayout(self.btnBox)
        self.lFrame.setStyleSheet('QFrame{background-color: #CDCDB4}')

        self.rightBox = QMainWindow()
        self.rightBox.setCentralWidget(MoviesDisplay(1, self.movies_info))
        self.rightBox.setContentsMargins(0, 0, 0, 0)
        self.rightBox.setFixedWidth(840)

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.lFrame)
        self.hBox.addWidget(self.rightBox)
        self.hBox.setContentsMargins(0, 0, 0, 0)
        self.hBox.setStretch(0, 8)
        self.hBox.setStretch(1, 28)

        self.setLayout(self.hBox)
        self.setStyleSheet(
            'background-color: white;'
        )


    def LbResponse(self, pressed):
        source = self.sender()
        if source.text() == '所有电影':
            self.rightBox.setCentralWidget(MoviesDisplay(1, get_movies_info()))
            self.hBox.setContentsMargins(0, 0, 0, 0)
            self.hBox.setStretch(0, 8)
            self.hBox.setStretch(1, 32)

        elif source.text() == '高级搜索':
            self.rightBox.setCentralWidget(AdvancedSearch())
            self.hBox.setContentsMargins(0, 0, 0, 0)
            self.hBox.setStretch(0, 8)
            self.hBox.setStretch(1, 32)

        elif source.text() == '分类':
            self.rightBox.setCentralWidget(GenresDisplay(1, get_sorted_genres_info()))
            self.hBox.setContentsMargins(0, 0, 0, 0)
            self.hBox.setStretch(0, 8)
            self.hBox.setStretch(1, 32)

        elif source.text() == '导演':
            self.rightBox.setCentralWidget(DirectorsDisplay(1, get_directors_info()))
            self.hBox.setContentsMargins(0, 0, 0, 0)
            self.hBox.setStretch(0, 8)
            self.hBox.setStretch(1, 32)

        elif source.text() == '主演':
            self.rightBox.setCentralWidget(StarsDisplay(1, get_starring_info()))
            self.hBox.setContentsMargins(0, 0, 0, 0)
            self.hBox.setStretch(0, 8)
            self.hBox.setStretch(1, 32)
        else:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MoviesArchive()
    ex.setWindowOpacity(0.95)
    sys.exit(app.exec_())