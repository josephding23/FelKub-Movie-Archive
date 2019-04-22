from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
from src.pages import MoviesPage


class DirectorDetailedInfo(QMainWindow):

    def __init__(self, info, movies):
        super().__init__()
        self.info = info
        self.movies = movies
        self.initUI()

    def initUI(self):
        self.fullName = self.info['FullName']
        self.nameLabel = QLabel(self.fullName)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setStyleSheet(
            'QLabel{font-family:"华文行楷";color: brown;font-weight:bold;font-size:28px;}'
        )

        self.returnBtn = QPushButton()
        self.returnBtn.setIcon(QIcon('icon/Actions-edit-undo-icon.png'))
        self.returnBtn.setIconSize(QSize(40, 40))
        self.returnBtn.clicked[bool].connect(self.close)
        self.returnBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.nameLabel)
        self.headerLayout.addWidget(self.returnBtn)
        self.headerLayout.setContentsMargins(0, 4, 8, 0)
        self.headerLayout.setStretch(0, 10)
        self.headerLayout.setStretch(1, 2)
        self.headerLayout.setSpacing(24)

        self.picUrl = 'pic/directors/large/' + self.info['PicName']
        self.picLabel = QLabel()
        self.pixmap = QPixmap()
        self.pixmap.load(self.picUrl)
        self.pixmap = self.pixmap.scaled(210, 300)
        self.picLabel.setPixmap(self.pixmap)
        self.picLabel.setFixedHeight(300)

        self.rightLabelSheet = 'QLabel{font-family:"黑体";color:black;font-size:16px;font-style:italic;}'
        self.rightInfoSheet = 'QLabel{font-family:"黑体";color:black;font-size:16px;}'
        self.rightFrame = QFrame()

        self.averageRatingLabel = QLabel('平均评分:')
        self.averageRatingLabel.setStyleSheet(self.rightLabelSheet)
        self.averageRatingInfo = QLabel(str(self.info['AverageRating']))
        self.averageRatingInfo.setStyleSheet(self.rightInfoSheet)
        self.averageRatingBox = QHBoxLayout()
        self.averageRatingBox.addWidget(self.averageRatingLabel, 1)
        self.averageRatingBox.addWidget(self.averageRatingInfo, 5)

        self.averageVotesLabel = QLabel('平均观看人数:')
        self.averageVotesLabel.setStyleSheet(self.rightLabelSheet)
        self.averageVotesInfo = QLabel(str(self.info['AverageVotes']))
        self.averageVotesInfo.setStyleSheet(self.rightInfoSheet)
        self.averageVotesBox = QHBoxLayout()
        self.averageVotesBox.addWidget(self.averageVotesLabel, 1)
        self.averageVotesBox.addWidget(self.averageVotesInfo, 5)

        self.totalVotesLabel = QLabel('总观看数:')
        self.totalVotesLabel.setStyleSheet(self.rightLabelSheet)
        self.totalVotesInfo = QLabel(str(self.info['TotalVotes']))
        self.totalVotesInfo.setStyleSheet(self.rightInfoSheet)
        self.totalVotesBox = QHBoxLayout()
        self.totalVotesBox.addWidget(self.totalVotesLabel, 1)
        self.totalVotesBox.addWidget(self.totalVotesInfo, 5)

        self.aveActivityLabel = QLabel('平均活跃年:')
        self.aveActivityLabel.setStyleSheet(self.rightLabelSheet)
        self.aveActivityInfo = QLabel(str(self.info['AverageActiveYear']))
        self.aveActivityInfo.setStyleSheet(self.rightInfoSheet)
        self.aveActivityBox = QHBoxLayout()
        self.aveActivityBox.addWidget(self.aveActivityLabel, 1)
        self.aveActivityBox.addWidget(self.aveActivityInfo, 5)

        self.birthDate = '出生日期:'
        self.birthDateLabel = QLabel(self.birthDate)
        self.birthDateLabel.setStyleSheet(self.rightLabelSheet)
        self.birthDateInfo = QLabel(self.info['BirthDate'])
        self.birthDateInfo.setStyleSheet(self.rightInfoSheet)
        self.birthDateBox = QHBoxLayout()
        self.birthDateBox.addWidget(self.birthDateLabel, 1)
        self.birthDateBox.addWidget(self.birthDateInfo, 5)

        self.birthPlace = '出生地:'
        self.birthPlaceLabel = QLabel(self.birthPlace)
        self.birthPlaceLabel.setStyleSheet(self.rightLabelSheet)
        self.birthPlaceInfo = QLabel(self.info['BirthPlace'])
        self.birthPlaceInfo.setStyleSheet(self.rightInfoSheet)
        self.birthPlaceBox = QHBoxLayout()
        self.birthPlaceBox.addWidget(self.birthPlaceLabel, 1)
        self.birthPlaceBox.addWidget(self.birthPlaceInfo, 5)

        self.occupation = '职业:'
        self.occupationLabel = QLabel(self.occupation)
        self.occupationLabel.setStyleSheet(self.rightLabelSheet)
        self.occupationInfo = QLabel(','.join(self.info['Occupation']))
        self.occupationInfo.setStyleSheet(self.rightInfoSheet)
        self.occupationBox = QHBoxLayout()
        self.occupationBox.addWidget(self.occupationLabel, 1)
        self.occupationBox.addWidget(self.occupationInfo, 5)

        self.picLeftLayout = QVBoxLayout()
        self.picLeftLayout.addLayout(self.averageRatingBox)
        self.picLeftLayout.addLayout(self.averageVotesBox)
        self.picLeftLayout.addLayout(self.totalVotesBox)
        self.picLeftLayout.addLayout(self.aveActivityBox)
        self.picLeftLayout.addLayout(self.birthDateBox)
        self.picLeftLayout.addLayout(self.birthPlaceBox)
        self.picLeftLayout.addLayout(self.occupationBox)
        self.picLeftLayout.setSpacing(14)

        self.rightFrame.setLayout(self.picLeftLayout)
        self.rightFrame.setContentsMargins(0, 0, 0, 0)
        self.rightFrame.setStyleSheet('QFrame{background-color: #BEBEBE; border-style: groove;}')
        self.rightFrame.setFixedHeight(300)

        self.InfoLayout = QHBoxLayout()
        self.InfoLayout.addWidget(self.picLabel)
        self.InfoLayout.addWidget(self.rightFrame)
        self.InfoLayout.setContentsMargins(0, 0, 0, 0)
        self.InfoLayout.setSpacing(20)

        self.InfoFrame = QFrame()
        self.InfoFrame.setLayout(self.InfoLayout)
        self.InfoFrame.setFixedHeight(300)

        self.summary = '    ' + self.info['Summary']
        if len(self.summary) > 400:
            self.summary = self.summary[:400] + '...'
        self.summaryLabel = QLabel(self.summary)
        self.summaryLabel.setWordWrap(True)
        self.summaryLabel.setAlignment(Qt.AlignCenter)
        self.summaryLabel.setFont(QFont('华文楷体'))
        self.summaryLabel.setStyleSheet('QLabel{font-size:15px;}')

        self.directorInfoLayout = QVBoxLayout()
        self.directorInfoLayout.addLayout(self.headerLayout)
        self.directorInfoLayout.addWidget(self.InfoFrame)
        self.directorInfoLayout.addWidget(self.summaryLabel)
        self.directorInfoLayout.setStretch(0, 20)
        self.directorInfoLayout.setStretch(1, 100)
        self.directorInfoLayout.setStretch(2, 60)
        self.directorInfoLayout.setSpacing(20)

        self.rightBox = QMainWindow()
        self.rightBox.setCentralWidget(MoviesPage.MoviesDisplay(1, self.movies))
        self.rightBox.setContentsMargins(0, 0, 0, 0)
        self.wholeLayout = QHBoxLayout()
        self.wholeLayout.addLayout(self.directorInfoLayout)
        self.wholeLayout.addWidget(self.rightBox)

        self.directorWidget = QWidget()
        self.directorWidget.setLayout(self.wholeLayout)
        self.setContentsMargins(10, 0, 10, 10)
        self.setCentralWidget(self.directorWidget)
        self.setWindowTitle(self.info['FullName'] + ' - FelKub Movies Archive')
        self.setWindowIcon(QIcon('icon/Movie-icon.png'))
        self.resize(1000, 720)