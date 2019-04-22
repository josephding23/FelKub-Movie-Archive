# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QFrame, QWidget, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QSize
from src.pages.MoviesPage import MoviesDisplay
from src.database.DataQuery import get_movies_of_genre, get_traits_of_genre
from math import ceil
from src.recommender.TraitsEdit import GenreEditPage

class GenresInfoGridWidget(QFrame):
    def __init__(self, info):
        self.num = -1
        self.info = info
        super().__init__()
        self.initUI()

    def set_num(self, num):
        self.num = num

    def set_info(self, info):
        self.info = info

    def initUI(self):
        self.btnSheet = 'QPushButton{font-size:16px; background-color:#483D8B; color:#BBFFFF; width:26px;height:26px; border-radius: 10px;}' \
                        'QPushButton:hover{font-size:16px; background-color:#C6E2FF; color:#002e5c; width:26px;height:26px; border-radius: 10px;}'

        self.genreBtn = QPushButton(self.info['Name'])
        self.genreBtn.setFont(QFont('黑体'))
        self.genreBtn.setStyleSheet(self.btnSheet)
        self.genreBtn.setMinimumHeight(60)
        self.genreBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.genreBtn.clicked[bool].connect(self.genreResponse)

        self.numLabel = QLabel('共' + str(self.info['Times']) + '部')
        self.numLabel.setFont(QFont('黑体'))
        self.setStyleSheet('QLabel{font-size: 15px;}')

        self.editBtn = QPushButton('编辑特征值')
        self.editBtn.setMinimumHeight(30)
        self.editBtn.setStyleSheet('QPushButton{font-size:14px; background-color:#90EE90; color:#006400}'
                                   'QPushButton:hover{font-size:14px; background-color:#8B0A50; color:#FFF8DC}'
                                   'QToolTip{background-color:#FFFFF0; color:#000000; font-size: 13px}')
        self.tootipStr = str()
        for key in get_traits_of_genre(self.info['Name']).keys():
            self.tootipStr = self.tootipStr + key + ': ' + str(self.info['Traits'][key]) + '\n'
        self.tootipStr = self.tootipStr[:-1]
        self.editBtn.setToolTip(self.tootipStr)
        self.editBtn.clicked[bool].connect(self.editGenreResponse)

        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.numLabel)
        self.hLayout.addWidget(self.editBtn)

        self.gridLayout = QVBoxLayout()
        self.gridLayout.addWidget(self.genreBtn)
        self.gridLayout.addLayout(self.hLayout)

        self.setLayout(self.gridLayout)

    def genreResponse(self, pressed):
        source = self.sender()
        genre = source.text()

        self.newFrame = QMainWindow()
        self.newFrame.setCentralWidget(MoviesDisplay(1, get_movies_of_genre(genre)))

        self.newWindowLayout = QHBoxLayout()
        self.newWindowLayout.addWidget(self.newFrame)

        self.newWindow = QWidget()
        self.newWindow.setLayout(self.newWindowLayout)
        self.newWindow.setWindowIcon(QIcon('icon/1-Movies-icon.png'))
        self.newWindow.setWindowTitle("'" + genre + "'" + '类电影 - FelKub Movies Archive')
        self.newWindow.resize(560, 680)
        self.newWindow.move(30, 14)
        self.newWindow.show()

    def editGenreResponse(self):
        self.detailed = GenreEditPage(self.info)
        self.detailed.show()


class GenresPageWidget(QWidget):
    def __init__(self, page, genres_info):
        super().__init__()
        self.page = page
        self.genres_info = genres_info
        self.initUI()

    def initUI(self):
        self.row = 5
        self.column = 3

        self.itemPerPage = self.column * self.row

        self.startNum = (self.page - 1) * self.itemPerPage
        self.endNum = self.page * self.itemPerPage

        if len(self.genres_info) < self.endNum:
            self.endNum = len(self.genres_info)
            self.itemPerPage = self.endNum - self.startNum

        self.genresGrid = QGridLayout()
        self.genres_list = self.genres_info[self.startNum: self.endNum]
        for i in range(self.row):
            for j in range(self.column):
                if i * self.column + j < self.itemPerPage:
                    genreWidget = GenresInfoGridWidget(self.genres_list[i * self.column + j])
                    genreWidget.setStyleSheet(
                        'background-color: gray;' +
                        'border: 10px black'
                    )
                    self.genresGrid.addWidget(genreWidget, i, j)
        self.setLayout(self.genresGrid)
        self.setFixedWidth(800)

class GenresDisplay(QWidget):
    def __init__(self, page, genres_info):
        super().__init__()
        self.page = page
        self.genres_info = genres_info
        self.max_page = ceil(len(self.genres_info) / 15)
        if self.max_page == 0:
            self.max_page = 1
        self.initUI()

    def initUI(self):

        self.itemBox = QMainWindow()
        self.itemBox.setCentralWidget(GenresPageWidget(self.page, self.genres_info))
        self.itemBox.setContentsMargins(0, 0, 0, 0)

        self.pageSheet = 'QPushButton{background-color:#B4EEB4;}' \
                         'QPushButton:hover{background-color:#8470FF;}' \
                         'QPushButton:pressed{background-color:#E0FFFF;}'

        self.firstPageBtn = QPushButton(self)
        self.firstPageBtn.setIcon(QIcon('icon/Actions-go-first-view-icon.png'))
        self.firstPageBtn.setStyleSheet(self.pageSheet)
        self.firstPageBtn.setMaximumWidth(64)
        self.firstPageBtn.setIconSize(QSize(32, 32))
        self.firstPageBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.page == 1:
            self.firstPageBtn.setDisabled(True)

        self.previousPageBtn = QPushButton(self)
        self.previousPageBtn.setIcon(QIcon('icon/Actions-go-previous-icon.png'))
        self.previousPageBtn.setStyleSheet(self.pageSheet)
        self.previousPageBtn.setMaximumWidth(64)
        self.previousPageBtn.setIconSize(QSize(32, 32))
        self.previousPageBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)

        self.nextPageBtn = QPushButton(self)
        self.nextPageBtn.setIcon(QIcon('icon/Actions-go-next-icon.png'))
        self.nextPageBtn.setStyleSheet(self.pageSheet)
        self.nextPageBtn.setMaximumWidth(64)
        self.nextPageBtn.setIconSize(QSize(32, 32))
        self.nextPageBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)

        self.lastPageBtn = QPushButton(self)
        self.lastPageBtn.setIcon(QIcon('icon/Actions-go-last-view-icon.png'))
        self.lastPageBtn.setStyleSheet(self.pageSheet)
        self.lastPageBtn.setMaximumWidth(64)
        self.lastPageBtn.setIconSize(QSize(32, 32))
        self.lastPageBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.page == self.max_page:
            self.lastPageBtn.setDisabled(True)

        self.pageInfoLabel = QLabel('1 / ' + str(self.max_page))
        self.pageInfoLabel.setAlignment(Qt.AlignCenter)
        self.pageInfoLabel.setStyleSheet('QLabel{font-size:20px; color:#104E8B; font-weight:bold}')
        self.pageInfoLabel.setMaximumWidth(160)

        self.firstPageBtn.clicked[bool].connect(self.firstPageResponse)
        self.previousPageBtn.clicked[bool].connect(self.previousPageResponse)
        self.nextPageBtn.clicked[bool].connect(self.nextPageResponse)
        self.lastPageBtn.clicked[bool].connect(self.lastPageResponse)

        self.pageBox = QHBoxLayout()
        self.pageBox.addWidget(self.firstPageBtn)
        self.pageBox.addWidget(self.previousPageBtn)
        self.pageBox.addWidget(self.pageInfoLabel)
        self.pageBox.addWidget(self.nextPageBtn)
        self.pageBox.addWidget(self.lastPageBtn)
        self.pageBox.setContentsMargins(160, 0, 160, 40)

        self.wholeLayout = QVBoxLayout()
        self.wholeLayout.addWidget(self.itemBox)
        self.wholeLayout.addLayout(self.pageBox)

        self.setFixedWidth(840)
        self.setLayout(self.wholeLayout)
        self.setStyleSheet('QMainWindow{background-color: #F0FFFF;}')

    def firstPageResponse(self):
        self.page = 1
        if self.page == 1:
            self.firstPageBtn.setDisabled(True)
        else:
            self.firstPageBtn.setDisabled(False)
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)
        else:
            self.previousPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)
        else:
            self.nextPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.lastPageBtn.setDisabled(True)
        else:
            self.lastPageBtn.setDisabled(False)
        self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
        self.itemBox.setCentralWidget(GenresPageWidget(self.page, self.genres_info))

    def previousPageResponse(self):
        self.page = self.page - 1
        if self.page == 1:
            self.firstPageBtn.setDisabled(True)
        else:
            self.firstPageBtn.setDisabled(False)
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)
        else:
            self.previousPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)
        else:
            self.nextPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.lastPageBtn.setDisabled(True)
        else:
            self.lastPageBtn.setDisabled(False)
        self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
        self.itemBox.setCentralWidget(GenresPageWidget(self.page, self.genres_info))

    def nextPageResponse(self):
        self.page = self.page + 1
        if self.page == 1:
            self.firstPageBtn.setDisabled(True)
        else:
            self.firstPageBtn.setDisabled(False)
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)
        else:
            self.previousPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)
        else:
            self.nextPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.lastPageBtn.setDisabled(True)
        else:
            self.lastPageBtn.setDisabled(False)
        self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
        self.itemBox.setCentralWidget(GenresPageWidget(self.page, self.genres_info))

    def lastPageResponse(self):
        self.page = self.max_page
        if self.page == 1:
            self.firstPageBtn.setDisabled(True)
        else:
            self.firstPageBtn.setDisabled(False)
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)
        else:
            self.previousPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)
        else:
            self.nextPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.lastPageBtn.setDisabled(True)
        else:
            self.lastPageBtn.setDisabled(False)
        self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
        self.itemBox.setCentralWidget(GenresPageWidget(self.page, self.genres_info))

