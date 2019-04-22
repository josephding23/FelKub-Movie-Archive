# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QLabel, QLayout, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont, QCursor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from math import ceil
from src.database.DataQuery import *
from src.detail.DirectorDetailed import DirectorDetailedInfo

class DirectorInfoGridWidget(QFrame):
    def __init__(self, info, choice):

        self.num = -1
        self.info = info
        self.choice = choice
        super().__init__()
        self.initUI()

    def set_num(self, num):
        self.num = num

    def set_info(self, info):
        self.info = info

    # (title, pic_name, rating, nation, year, length)
    def initUI(self):
        self.lblSheet = 'QLabel{font-family:"微软雅黑";}'
        self.title = self.info['FullName']
        if len(self.title) > 7:
            self.title = self.title[:7] + '...'
        self.nameLable = QPushButton(self.title)
        self.nameLable.clicked[bool].connect(self.directorInfoResponse)
        self.nameLable.setCursor(QCursor(Qt.PointingHandCursor))
        self.nameLable.setStyleSheet(
            'QPushButton{font-size: 14px; color: #ffffff; font-weight: bold; font-family:"微软雅黑";}'
            'QPushButton:hover{font-size: 14px; color: #C0FF3E; font-weight: bold; font-family:"微软雅黑";}'
        )

        self.birthDateStr = self.info['BirthDate']
        if len(self.birthDateStr) > 7:
            self.birthDateStr = self.birthDateStr[:7] + '...'
        self.birthDate = QLabel("出生日期：" + self.birthDateStr)
        self.birthDate.setStyleSheet(self.lblSheet)


        self.birthPlaceStr = self.info['BirthPlace']
        if len(self.birthPlaceStr) > 7:
            self.birthPlaceStr = self.birthPlaceStr[:7] + '...'
        self.birthPlace = QLabel("出生地：" + self.birthPlaceStr)
        self.birthPlace.setStyleSheet(self.lblSheet)


        self.aveRating = QLabel('平均评分：' + str(self.info['AverageRating']))
        self.aveRating.setStyleSheet(self.lblSheet)

        self.aveVotes = QLabel('平均观看数：' + str(self.info['AverageVotes']))
        self.aveVotes.setStyleSheet(self.lblSheet)

        self.totalVotes = QLabel('总观看数：' + str(self.info['TotalVotes']))
        self.totalVotes.setStyleSheet(self.lblSheet)

        self.aveActivity = QLabel('平均活跃年：' + str(self.info['AverageActiveYear']))
        self.aveActivity.setStyleSheet(self.lblSheet)

        self.otherInfoLayout = QVBoxLayout()
        self.otherInfoLayout.addWidget(self.birthDate)
        self.otherInfoLayout.addWidget(self.birthPlace)
        if self.choice == 1:
            self.otherInfoLayout.addWidget(self.aveRating)
            self.otherInfoLayout.addWidget(self.aveVotes)
        elif self.choice == 2:
            self.otherInfoLayout.addWidget(self.totalVotes)
            self.otherInfoLayout.addWidget(self.aveActivity)

        self.picLable = QLabel()
        self.pixmap = QPixmap()
        picUrl = 'pic/directors/small/' + self.info['PicName']
        self.pixmap.load(picUrl)
        self.pixmap = self.pixmap.scaled(105, 150)
        self.picLable.setScaledContents(True)
        self.picLable.setPixmap(self.pixmap)

        # self.detailedBtn = QPushButton("Detailed")
        # self.detailedBtn.clicked[bool].connect(self.movieInfoResponse)

        self.movieLayout = QVBoxLayout()
        self.movieLayout.addWidget(self.nameLable)
        # self.movieLayout.addWidget(self.detailedBtn)
        self.movieLayout.addLayout(self.otherInfoLayout)
        self.movieLayout.addWidget(self.picLable)
        self.movieLayout.setContentsMargins(8, 5, 8, 5)

        self.setLayout(self.movieLayout)
        self.resize(120, 200)

    def directorInfoResponse(self):
        self.detailed = DirectorDetailedInfo(self.info, get_movies_directed_by(self.info['ShortName']))
        self.detailed.show()
        # self.detailed.exec_()


class DirectorsInfoPageWidget(QWidget):
    def __init__(self, page, directors_info, choice=1):
        super().__init__()
        self.page = page
        self.orderRating = 1
        self.orderVotes = 1
        self.directors_info = directors_info
        self.choice = choice
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
        if len(self.directors_info) < self.endNum:
            self.endNum = len(self.directors_info)
            self.itemPerPage = self.endNum - self.startNum

        self.directorsInfoLayout = QGridLayout()
        self.directorsInfoLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.directorsInfoLayout.setContentsMargins(0, 10, 0, 15)
        self.directorsInfoLayout.setSpacing(5)
        self.directors_list = self.directors_info[self.startNum: self.endNum]

        # (title, pic_name, rating, nation, year, length)
        for i in range(self.row):
            for j in range(self.column):
                if i * self.column + j < self.itemPerPage:
                    directorWidget = DirectorInfoGridWidget(self.directors_list[i * self.column + j], self.choice)
                    directorWidget.setStyleSheet(
                        'background-color: gray;'+
                        'border: 10px black'
                    )
                    # movieWidget.set_info(movies_list[i * self.column + j])
                    self.directorsInfoLayout.addWidget(directorWidget, i, j)

        self.setLayout(self.directorsInfoLayout)
        self.setContentsMargins(0, 0, 0, 0)

class DirectorsDisplay(QWidget):
    def __init__(self, page, directors_info):
        super().__init__()
        self.page = page
        self.directors_info = directors_info
        self.max_page = ceil(len(self.directors_info) / 10)
        if self.max_page == 0:
            self.max_page = 1
        self.ratingSort = '平均评分降序↓'
        self.ratingOrder = -1
        self.aveVotesSort = '平均观看人数降序↓'
        self.aveVotesOrder = -1
        self.totalVotesSort = '总观看人数降序↓'
        self.totalVotesOrder = -1
        self.aveActivitySort = '平均活跃时期降序↓'
        self.aveActivityOrder = -1
        self.choice = 1
        self.initUI()

    def initUI(self):
        self.searchField = QLineEdit()
        self.searchField.setMaximumWidth(480)
        self.searchField.setFixedHeight(21)
        self.searchField.setFont(QFont('楷体'))
        self.searchField.setAlignment(Qt.AlignCenter)
        self.searchField.setCursor(QCursor(Qt.IBeamCursor))
        self.searchField.setStyleSheet('QLineEdit{background-color: #B4EEB4; font-size:20px}')

        self.searchBtn = QPushButton('导演名搜索')
        self.searchBtn.setMaximumWidth(120)
        self.searchBtn.setFixedHeight(24)
        self.searchBtn.setFont(QFont('华文琥珀'))
        self.searchBtn.setStyleSheet('QPushButton{background-color: #2E8B57; color: #C1FFC1; font-size: 16px}'
                                     'QPushButton:hover{background-color: #98FB98; color: #2E8B57; font-size: 16px}')
        self.searchBtn.resize(100, 50)
        self.searchBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.searchBtn.clicked[bool].connect(self.searchResponse)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.setContentsMargins(40, 8, 50, 4)
        self.searchLayout.setSpacing(12)
        self.searchLayout.addWidget(self.searchField)
        self.searchLayout.addWidget(self.searchBtn)

        self.orderBtnSheet = 'QPushButton{font-size: 16px; border:1px solid #458B00; background-color: #A2CD5A; height:20px; width:40px; color: #008B45}' \
                             'QPushButton:checked{font-size: 16px; border:1px solid #458B00; background-color: #A2CD5A; height:20px; width:40px; color: #008B45}' \
                             'QPushButton:hover{font-size: 16px; border:1px solid #458B00; background-color: #698B22; height:20px; width:40px; color: #C0FF3E}'


        self.ratingSortBtn = QPushButton()
        self.ratingSortBtn.setText(self.ratingSort)
        self.ratingSortBtn.setMaximumWidth(150)
        self.ratingSortBtn.setFont(QFont('黑体'))
        self.ratingSortBtn.setStyleSheet(self.orderBtnSheet)
        self.ratingSortBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.ratingSortBtn.setCheckable(True)
        self.ratingSortBtn.clicked.connect(lambda:self.sortResponse('RatingSort'))

        self.aveVotesSortBtn = QPushButton()
        self.aveVotesSortBtn.setText(self.aveVotesSort)
        self.aveVotesSortBtn.setMaximumWidth(150)
        self.aveVotesSortBtn.setFont(QFont('黑体'))
        self.aveVotesSortBtn.setStyleSheet(self.orderBtnSheet)
        self.aveVotesSortBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.aveVotesSortBtn.setCheckable(True)
        self.aveVotesSortBtn.clicked.connect(lambda: self.sortResponse('AveVotesSort'))

        self.totalVotesSortBtn = QPushButton()
        self.totalVotesSortBtn.setText(self.totalVotesSort)
        self.totalVotesSortBtn.setMaximumWidth(150)
        self.totalVotesSortBtn.setFont(QFont('黑体'))
        self.totalVotesSortBtn.setStyleSheet(self.orderBtnSheet)
        self.totalVotesSortBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.totalVotesSortBtn.setCheckable(True)
        self.totalVotesSortBtn.clicked.connect(lambda: self.sortResponse('TotalVotesSort'))

        self.aveActivitySortBtn = QPushButton()
        self.aveActivitySortBtn.setText(self.aveActivitySort)
        self.aveActivitySortBtn.setMaximumWidth(150)
        self.aveActivitySortBtn.setFont(QFont('黑体'))
        self.aveActivitySortBtn.setStyleSheet(self.orderBtnSheet)
        self.aveActivitySortBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.aveActivitySortBtn.setCheckable(True)
        self.aveActivitySortBtn.clicked.connect(lambda: self.sortResponse('AveActivitySort'))


        self.sortBtnBox = QHBoxLayout()
        self.sortBtnBox.addWidget(self.ratingSortBtn)
        self.sortBtnBox.addWidget(self.aveVotesSortBtn)
        self.sortBtnBox.addWidget(self.totalVotesSortBtn)
        self.sortBtnBox.addWidget(self.aveActivitySortBtn)
        self.sortBtnBox.setSpacing(25)

        self.sortBtnBox.setContentsMargins(0, 0, 35, 0)

        self.itemBox = QMainWindow()
        self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info))
        self.itemBox.setContentsMargins(15, 0, 0, 0)

        self.pageSheet = 'QPushButton{background-color: #B4EEB4;}' \
                         'QPushButton:hover{background-color:#3CB371;}' \
                         'QPushButton:pressed{background-color:#00FF00;}'

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
        self.pageInfoLabel.setStyleSheet('QLabel{font-size:20px; color:#698B22; font-weight:bold}')
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
        self.layoutBox.setContentsMargins(10, 0, 0, 0)

        self.setFixedWidth(820)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layoutBox)
        self.setStyleSheet('QMainWindow{background-color: #C1FFC1;}')

    def sortResponse(self, info):
        if info == 'RatingSort':
            self.directors_info = get_directors_info_in_some_order('AverageRating', self.directors_info, self.ratingOrder)
            self.page = 1
            self.choice = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))

            self.ratingOrder = -self.ratingOrder
            if self.ratingSortBtn.isChecked():
                self.ratingSort = '平均评分升序↑'
            elif not self.ratingSortBtn.isChecked():
                self.ratingSort = '平均评分降序↓'
            self.ratingSortBtn.setText(self.ratingSort)


        if info == 'AveVotesSort':
            self.directors_info = get_directors_info_in_some_order('AverageVotes', self.directors_info, self.aveVotesOrder)
            self.page = 1
            self.choice = 1
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))

            self.aveVotesOrder = -self.aveVotesOrder
            if self.aveVotesSortBtn.isChecked():
                self.aveVotesSort = '平均观看人数升序↑'
            elif not self.aveVotesSortBtn.isChecked():
                self.aveVotesSort = '平均观看人数降序↓'
            self.aveVotesSortBtn.setText(self.aveVotesSort)


        if info == 'TotalVotesSort':
            self.directors_info = get_directors_info_in_some_order('TotalVotes', self.directors_info, self.totalVotesOrder)
            self.page = 1
            self.choice = 2
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))

            self.totalVotesOrder = -self.totalVotesOrder
            if self.totalVotesSortBtn.isChecked():
                self.totalVotesSort = '总观看人数升序↑'
            elif not self.totalVotesSortBtn.isChecked():
                self.totalVotesSort = '总观看人数降序↓'
            self.totalVotesSortBtn.setText(self.totalVotesSort)

        if info == 'AveActivitySort':
            self.directors_info = get_directors_info_in_some_order('AverageActiveYear', self.directors_info, self.aveActivityOrder)
            self.page = 1
            self.choice = 2
            self.pageInfoLabel.setText(str(self.page) + ' / ' + str(self.max_page))
            self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))

            self.aveActivityOrder = -self.aveActivityOrder
            if self.aveActivitySortBtn.isChecked():
                self.aveActivitySort = '平均活跃时期升序↑'
            elif not self.aveActivitySortBtn.isChecked():
                self.aveActivitySort = '平均活跃时期降序↓'
            self.aveActivitySortBtn.setText(self.aveActivitySort)


    def searchResponse(self, pressed):
        source = self.searchField
        searchStr = source.text()
        self.directors_info = search_directors_name(searchStr)
        self.page = 1
        self.max_page = ceil(len(self.directors_info) / 10)
        if self.max_page == 0:
            self.max_page = 1
        self.pageInfoLabel.setText(str(self.page) + ' OF ' + str(self.max_page))
        self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))
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
        self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))


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
        self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))


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
        self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))


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
        self.itemBox.setCentralWidget(DirectorsInfoPageWidget(self.page, self.directors_info, self.choice))

    '''
    def directorResponse(self, pressed):
        source = self.sender()
        director = source.text()
        self.centralWindow.setCentralWidget(MoviesDisplay(1, get_movies_directed_by(director)))
    '''