# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QWidget, QLayout, QFrame, QVBoxLayout, \
    QHBoxLayout, QPushButton, QLabel, QGridLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
from math import ceil
from MovieDetailed import MovieDetailedInfo
from DataQuery import *

class MovieInfoGridWidget(QFrame):
    def __init__(self, info):

        self.num = -1
        self.info = info
        self.translation = get_traits_translation()
        self.traitsList = get_traits_order()
        super().__init__()
        self.initUI()

    def set_num(self, num):
        self.num = num

    def set_info(self, info):
        self.info = info

    # (title, pic_name, rating, nation, year, length)
    def initUI(self):
        self.lblSheet = 'QLabel{font-family:"微软雅黑";}'
        self.title = self.info['Title']
        if len(self.title) > 7:
            self.title = self.title[:7] + '...'
        self.titleLable = QPushButton(self.title)
        self.titleLable.clicked[bool].connect(self.movieInfoResponse)
        self.titleLable.setCursor(QCursor(Qt.PointingHandCursor))

        self.ratingLabel = QLabel('评分：' + str(self.info['Rating']))
        self.ratingLabel.setStyleSheet(self.lblSheet)

        self.votesLabel = QLabel('人数：' + str(self.info['VotingNum']))
        self.votesLabel.setStyleSheet(self.lblSheet)
        self.votesLabel.setWordWrap(True)
        self.votesLabel.setAlignment(Qt.AlignCenter)
        self.votesLabel.setOpenExternalLinks(True)

        self.lengthLabel = QLabel('长度：' + str(self.info['Length']) + '分钟')
        self.lengthLabel.setStyleSheet(self.lblSheet)
        self.lengthLabel.setWordWrap(True)
        self.lengthLabel.setAlignment(Qt.AlignCenter)

        self.yearLabel = QLabel('年份：' + str(self.info['Year']) + '年')
        self.yearLabel.setStyleSheet(self.lblSheet)
        self.yearLabel.setWordWrap(True)
        self.yearLabel.setAlignment(Qt.AlignCenter)

        self.nations = str(', '.join(self.info['Nation']))
        if len(self.nations) > 8:
            self.nations = self.nations[:8] + '...'
        self.nationLabel = QLabel('国家：' + self.nations)
        self.nationLabel.setStyleSheet(self.lblSheet)
        self.nationLabel.setWordWrap(True)
        self.nationLabel.setAlignment(Qt.AlignCenter)
        self.nationLabel.setOpenExternalLinks(True)

        self.otherInfoSubLayout = QHBoxLayout()
        self.otherInfoSubLayout.addWidget(self.ratingLabel)
        self.otherInfoSubLayout.addWidget(self.votesLabel)

        self.otherInfoLayout = QVBoxLayout()

        self.otherInfoLayout.addLayout(self.otherInfoSubLayout)
        self.otherInfoLayout.addWidget(self.lengthLabel)
        self.otherInfoLayout.addWidget(self.yearLabel)
        self.otherInfoLayout.addWidget(self.nationLabel)


        self.picLable = QLabel()
        self.pixmap = QPixmap()
        picUrl = 'pic/movies/small/' + self.info['PicName']
        self.pixmap.load(picUrl)
        self.pixmap = self.pixmap.scaled(108, 160)
        self.picLable.setScaledContents(True)
        self.picLable.setPixmap(self.pixmap)

        # self.detailedBtn = QPushButton("Detailed")
        # self.detailedBtn.clicked[bool].connect(self.movieInfoResponse)
        self.tootipStr = str()
        for key in self.traitsList:
            self.tootipStr = self.tootipStr + self.translation[key] + ': ' + str(self.info['Traits'][key]) + '\n'
        self.tootipStr = self.tootipStr[:-1]

        self.setToolTip(self.tootipStr)
        self.setStyleSheet('QFrame{background-color: gray;border: 10px black}'
                           'QToolTip{background-color:#FFFFF0; color:#000000; font-size: 13px}'
                           'QPushButton{font-size: 14px; color: #ffffff; border: none; background-color: gray; font-weight: bold; font-family:"微软雅黑";}'
                           'QPushButton:hover{font-size: 14px; color: #97FFFF; background-color: gray; font-weight: bold; font-family:"微软雅黑";}')
        self.movieLayout = QVBoxLayout()
        self.movieLayout.addWidget(self.titleLable)
        # self.movieLayout.addWidget(self.detailedBtn)
        self.movieLayout.addLayout(self.otherInfoLayout)
        self.movieLayout.addWidget(self.picLable)
        self.movieLayout.setStretch(1, 3)
        self.movieLayout.setContentsMargins(5, 5, 5, 5)

        self.setLayout(self.movieLayout)
        self.resize(120, 200)

    def movieInfoResponse(self):
        self.detailed = MovieDetailedInfo(self.info)
        self.detailed.show()
        # self.detailed.exec_()


class MoviesInfoPageWidget(QWidget):
    def __init__(self, page, movies_info):

        super().__init__()
        self.page = page
        self.movies_info = movies_info
        self.initUI()

    def get_page(self):
        return self.page

    def set_page(self, page):
        self.page = page
        self.initUI()

    def initUI(self):
        self.row = 2
        self.column = 5

        self.itemPerPage = self.column * self.row

        self.startNum = (self.page - 1) * self.itemPerPage
        self.endNum = self.page * self.itemPerPage
        if len(self.movies_info) < self.endNum:
            self.endNum = len(self.movies_info)
            self.itemPerPage = self.endNum - self.startNum

        self.movieInfoLayout = QGridLayout()
        self.movieInfoLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.movieInfoLayout.setContentsMargins(0, 10, 0, 15)
        self.movieInfoLayout.setSpacing(5)
        self.movies_list = self.movies_info[self.startNum: self.endNum]
        # print(movies_list)

        # (title, pic_name, rating, nation, year, length)
        for i in range(self.row):
            for j in range(self.column):
                if i * self.column + j < self.itemPerPage:
                    movieWidget = MovieInfoGridWidget(self.movies_list[i * self.column + j])
                    # movieWidget.set_info(movies_list[i * self.column + j])
                    self.movieInfoLayout.addWidget(movieWidget, i, j)

        self.setLayout(self.movieInfoLayout)


class MoviesDisplay(QWidget):
    def __init__(self, page, movies_info):
        super().__init__()
        self.page = page
        self.movies_info = movies_info
        self.max_page = ceil(len(self.movies_info) / 10)
        if self.max_page == 0:
            self.max_page = 1
        self.yearSort = '年份降序↓'
        self.yearOrder = -1
        self.ratingSort = '评分降序↓'
        self.ratingOrder = -1
        self.votesSort = '观看人数降序↓'
        self.votesOrder = -1
        self.lengthSort = '长度降序↓'
        self.lengthOrder = -1
        self.initUI()

    def initUI(self):
        self.searchField = QLineEdit()
        self.searchField.setMaximumWidth(480)
        self.searchField.setFixedHeight(21)
        self.searchField.setFont(QFont('楷体'))
        self.searchField.setAlignment(Qt.AlignCenter)
        self.searchField.setCursor(QCursor(Qt.IBeamCursor))
        self.searchField.setStyleSheet('QLineEdit{background-color: #E0EEE0; font-size:16px}')

        self.searchBtn = QPushButton('电影名搜索')
        self.searchBtn.setMaximumWidth(120)
        self.searchBtn.setFixedHeight(24)
        self.searchBtn.setFont(QFont('华文琥珀'))
        self.searchBtn.setStyleSheet('QPushButton{background-color: #F0FFFF; color: #104E8B; font-size: 16px}'
                                     'QPushButton:hover{background-color: #5F9EA0; color: #104E8B; font-size: 16px}')
        self.searchBtn.resize(100, 50)
        self.searchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.searchBtn.clicked[bool].connect(self.searchResponse)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.setContentsMargins(40, 8, 50, 4)
        self.searchLayout.setSpacing(12)
        self.searchLayout.addWidget(self.searchField)
        self.searchLayout.addWidget(self.searchBtn)

        self.orderBtnSheet = 'QPushButton{font-size: 16px; border:1px solid #000000; background-color: #191970; height:20px; width:40px; color: #D3D3D3}' \
                             'QPushButton:hover{font-size: 16px; border:1px solid #000000; background-color:#CDC8B1; height:20px; width:40px; color: #483D8B}' \
                             'QPushButton:checked{border:1px solid #000000; font-size: 16px; border-color:#708090; background-color: #191970; height:20px; width:40px; color: #D3D3D3}'


        self.yearBtn = QPushButton()
        self.yearBtn.setText(self.yearSort)
        self.yearBtn.setMaximumWidth(150)
        self.yearBtn.setFont(QFont('黑体'))
        self.yearBtn.setStyleSheet(self.orderBtnSheet)
        self.yearBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.yearBtn.setCheckable(True)
        self.yearBtn.clicked.connect(lambda:self.sortResponse('YearSort'))

        self.ratingBtn = QPushButton()
        self.ratingBtn.setText(self.ratingSort)
        self.ratingBtn.setMaximumWidth(150)
        self.ratingBtn.setFont(QFont('黑体'))
        self.ratingBtn.setStyleSheet(self.orderBtnSheet)
        self.ratingBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.ratingBtn.setCheckable(True)
        self.ratingBtn.clicked.connect(lambda:self.sortResponse('RatingSort'))

        self.votesBtn = QPushButton()
        self.votesBtn.setText(self.votesSort)
        self.votesBtn.setMaximumWidth(150)
        self.votesBtn.setFont(QFont('黑体'))
        self.votesBtn.setStyleSheet(self.orderBtnSheet)
        self.votesBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.votesBtn.setCheckable(True)
        self.votesBtn.clicked.connect(lambda:self.sortResponse('VotesSort'))

        self.lengthBtn = QPushButton()
        self.lengthBtn.setText(self.lengthSort)
        self.lengthBtn.setMaximumWidth(150)
        self.lengthBtn.setFont(QFont('黑体'))
        self.lengthBtn.setStyleSheet(self.orderBtnSheet)
        self.lengthBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.lengthBtn.setCheckable(True)
        self.lengthBtn.clicked.connect(lambda: self.sortResponse('LengthSort'))

        self.sortBtnBox = QHBoxLayout()
        '''
        self.sortBtnBox.addWidget(self.yearDescBtn)
        self.sortBtnBox.addWidget(self.yearAscBtn)
        '''
        self.sortBtnBox.addWidget(self.yearBtn)
        self.sortBtnBox.addWidget(self.ratingBtn)
        self.sortBtnBox.addWidget(self.votesBtn)
        self.sortBtnBox.addWidget(self.lengthBtn)
        self.sortBtnBox.setSpacing(25)

        self.sortBtnBox.setContentsMargins(0, 0, 35, 0)

        self.itemBox = QMainWindow()
        self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))
        self.itemBox.setContentsMargins(15, 0, 0, 0)

        self.pageSheet = 'QPushButton{background-color:#AEEEEE;}' \
                         'QPushButton:hover{background-color:#8470FF;}' \
                         'QPushButton:pressed{background-color:#E0FFFF;}'

        self.pageBtnSheet = 'QPushButton{}'
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

        self.layoutBox = QVBoxLayout()
        self.layoutBox.addLayout(self.searchLayout)
        self.layoutBox.addLayout(self.sortBtnBox)
        self.layoutBox.addWidget(self.itemBox)
        self.layoutBox.addLayout(self.pageBox)
        self.layoutBox.setContentsMargins(20, 0, 0, 0)

        self.setFixedWidth(820)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutBox)
        self.setStyleSheet('QMainWindow{background-color: #F0FFFF;}')

    def searchResponse(self, pressed):
        source = self.searchField
        searchStr = source.text()
        self.movies_info = search_movie_title(searchStr)
        self.page = 1
        self.max_page = ceil(len(self.movies_info) / 10)
        if self.max_page == 0:
            self.max_page = 1
        self.pageInfoLabel.setText(str(self.page) + ' OF ' + str(self.max_page))
        self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))
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
        self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))


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
        self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))


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
        self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))


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
        self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))


    def sortResponse(self, info):
        if info == 'YearSort' and self.yearBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('Year', self.movies_info, self.yearOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.yearOrder = -self.yearOrder
            self.yearSort = '年份升序↑'
            self.yearBtn.setText(self.yearSort)


        if info == 'YearSort' and not self.yearBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('Year', self.movies_info, self.yearOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.yearOrder = -self.yearOrder
            self.yearSort = '年份降序↓'
            self.yearBtn.setText(self.yearSort)


        if info == 'RatingSort' and self.ratingBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('Rating', self.movies_info, self.ratingOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.ratingOrder = -self.ratingOrder
            self.ratingSort = '评分升序↑'
            self.ratingBtn.setText(self.ratingSort)

        if info == 'RatingSort' and not self.ratingBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('Rating', self.movies_info, self.ratingOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.ratingOrder = -self.ratingOrder
            self.ratingSort = '评分降序↓'
            self.ratingBtn.setText(self.ratingSort)


        if info == 'VotesSort' and self.votesBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('VotingNum', self.movies_info, self.votesOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.votesOrder = -self.votesOrder
            self.votesSort = '观看人数升序↑'
            self.votesBtn.setText(self.votesSort)

        if info == 'VotesSort' and not self.votesBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('VotingNum', self.movies_info, self.votesOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.votesOrder = -self.votesOrder
            self.votesSort = '观看人数降序↓'
            self.votesBtn.setText(self.votesSort)


        if info == 'LengthSort' and self.lengthBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('Length', self.movies_info, self.lengthOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.lengthOrder = -self.lengthOrder
            self.lengthSort = '长度升序↑'
            self.lengthBtn.setText(self.lengthSort)

        if info == 'LengthSort' and not self.lengthBtn.isChecked():
            self.movies_info = get_movies_info_in_some_order('Length', self.movies_info, self.lengthOrder)
            self.page = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(MoviesInfoPageWidget(self.page, self.movies_info))

            self.lengthOrder = -self.lengthOrder
            self.lengthSort = '长度降序↓'
            self.lengthBtn.setText(self.lengthSort)