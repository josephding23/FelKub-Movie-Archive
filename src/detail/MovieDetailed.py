# coding=utf-8
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
from src.recommender.RecommenderPage import RecommenderPage
from src.pages import MoviesPage
from src.detail import DirectorDetailed, StarDetailed
from src.recommender.TraitsEdit import MovieTraitsEditPage
from src.database.DataQuery import get_movies_of_genre, get_movies_directed_by, get_movies_starred_by, \
    get_director_info_of_name, get_star_info_of_name, get_movies_of_nation

class MovieDetailedInfo(QMainWindow):

    def __init__(self, info):
        super().__init__()
        self.info = info
        self.initUI()

    def initUI(self):
        self.title = self.info['Title']
        self.titleLabel = QLabel(self.title)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet(
            'QLabel{font-family:"华文行楷";color: #1C1C1C; font-size:28px;}'
        )

        self.recommendBtn = QPushButton('相关\n推荐')
        self.recommendBtn.setFixedSize(QSize(80, 90))
        self.recommendBtn.setStyleSheet(
            'QPushButton{font-size:24px; font-family:"华文行楷"; background-color: #FFD39B; color: #8B4513; border:1px solid #EEC591; border-radius: 20px 30px;}'
            'QPushButton:hover{font-size: 24px; background-color: #EE2C2C; color: #FFD700; border:1px solid #8B3A3A; border-radius: 20px 30px}'
            'QPushButton:pressed{font-size: 27px; background-color: #000080; color: #7FFF00; border:1px solid #000000; border-radius: 20px 30px; width: 90px; height: 80px; border-color: #000000; border-width: 2px;}')
        self.recommendBtn.clicked[bool].connect(self.recommendPageResponse)
        self.recommendBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.traitsBtn = QPushButton('特征\n编辑')
        self.traitsBtn.setFixedSize(QSize(80, 90))
        self.traitsBtn.setStyleSheet('QPushButton{font-size: 24px; font-family:"华文行楷"; background-color: #9AFF9A; color: #556B2F; border:1px solid #CAFF70; border-radius: 20px 30px}'
                                     'QPushButton:hover{font-size:24px; background-color: #006400; color: #7FFF00; border:1px solid #00FF00; border-radius: 20px 30px;}'
                                     'QPushButton:pressed{font-size: 27px; background-color: #DA70D6; color: #B03060; border:1px solid #191970; border-radius: 20px 30px; width: 90px; height: 80px; border-color: #000000; border-width: 2px;}')
        self.traitsBtn.clicked[bool].connect(self.editTraitsResponse)
        self.traitsBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.returnBtn = QPushButton()
        self.returnBtn.setIcon(QIcon('icon/Actions-edit-undo-icon.png'))
        self.returnBtn.setIconSize(QSize(40, 40))
        self.returnBtn.clicked[bool].connect(self.close)
        self.returnBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.recommendBtn, 1)
        self.headerLayout.addWidget(self.traitsBtn, 1)
        self.headerLayout.addWidget(self.titleLabel, 5)
        self.headerLayout.addWidget(self.returnBtn, 1)
        self.headerLayout.setContentsMargins(0, 4, 8, 0)
        self.headerLayout.setSpacing(16)

        self.picUrl = 'pic/movies/large/' + self.info['PicName']
        self.picLabel = QLabel()
        self.pixmap = QPixmap()
        self.pixmap.load(self.picUrl)
        self.pixmap = self.pixmap.scaled(270, 400)
        self.picLabel.setPixmap(self.pixmap)
        self.picLabel.setFixedHeight(400)

        self.rightHeaderSheet = 'QLabel{font-family:"黑体";color:black;font-size:16px;font-style:italic;}'
        self.rightLabelSheet = 'QLabel{font-family:"黑体";color:black;font-size:18px;}'
        self.rightFrame = QFrame()

        self.genresInfo = '类型: ' + ', '.join(self.info['Genres'])

        self.genresLabel = QLabel('类型: ')
        self.genresBox = QHBoxLayout()
        self.genresBox.setAlignment(Qt.AlignLeft)
        for genre in self.info['Genres']:
            genreBtn = QPushButton(genre)
            genreBtn.setStyleSheet('QPushButton{background-color:#191970; color:#D3D3D3; font-family:"隶书"; font-size: 17px;}'
                                   'QPushButton:hover{background-color:#87CEFA; color:#0000CD; font-family:"隶书"; font-size: 17px;}')
            genreBtn.clicked[bool].connect(self.genreResponse)
            genreBtn.setCursor(QCursor(Qt.PointingHandCursor))
            genreBtn.setMaximumWidth(60)
            # genreBtn.setStyleSheet('')
            self.genresBox.addWidget(genreBtn)
        self.genresLabel.setStyleSheet(self.rightHeaderSheet)

        self.genresLayout = QHBoxLayout()
        self.genresLayout.addWidget(self.genresLabel, 1)
        self.genresLayout.addLayout(self.genresBox, 5)

        self.ratingHeader = QLabel('评分: ')
        self.ratingHeader.setStyleSheet(self.rightHeaderSheet)
        self.ratingLabel = QLabel(str(self.info['Rating']) + ' (' + str(self.info['VotingNum']) + '人评)')
        self.ratingLabel.setStyleSheet(self.rightLabelSheet)
        self.ratingLayout = QHBoxLayout()
        self.ratingLayout.addWidget(self.ratingHeader, 1)
        self.ratingLayout.addWidget(self.ratingLabel, 4)

        self.yearHeader = QLabel('年份: ')
        self.yearLabel = QLabel(str(self.info['Year']))
        self.yearHeader.setStyleSheet(self.rightHeaderSheet)
        self.yearLabel.setStyleSheet(self.rightLabelSheet)
        self.yearLayout = QHBoxLayout()
        self.yearLayout.addWidget(self.yearHeader, 1)
        self.yearLayout.addWidget(self.yearLabel, 4)

        self.nationHeader = QLabel('国家: ')
        self.nationHeader.setStyleSheet(self.rightHeaderSheet)

        self.nations = self.info['Nation']
        if len(self.nations) > 4:
            self.nations = self.nations[:4]
        self.nationBox = QGridLayout()
        self.nationBox.setAlignment(Qt.AlignLeft)
        self.nationNum = len(self.nations)
        for i in range(self.nationNum):
            row = i // 2
            column = i % 2
            nationBtn = QPushButton(self.info['Nation'][i])
            nationBtn.setStyleSheet(
                'QPushButton{background-color:#8B6914; color:#FFD700; font-family:"隶书"; font-size: 17px;}'
                'QPushButton:hover{background-color:#FFFF00; color:#8B814C; font-family:"隶书"; font-size: 17px;}')
            nationBtn.clicked[bool].connect(self.nationResponse)
            nationBtn.setCursor(QCursor(Qt.PointingHandCursor))
            # genreBtn.setStyleSheet('')
            self.nationBox.addWidget(nationBtn, row, column)

        self.nationLayout = QHBoxLayout()
        self.nationLayout.addWidget(self.nationHeader, 1)
        self.nationLayout.addLayout(self.nationBox, 5)

        self.lengthHeader = QLabel('时长: ')
        self.lengthHeader.setStyleSheet(self.rightHeaderSheet)
        self.lengthLabel = QLabel(str(self.info['Length']) + '分钟')
        self.lengthLabel.setStyleSheet(self.rightLabelSheet)
        self.lengthLayout = QHBoxLayout()
        self.lengthLayout.addWidget(self.lengthHeader, 1)
        self.lengthLayout.addWidget(self.lengthLabel, 4)

        self.directorsLabel = QLabel('导演: ')
        self.directorsLabel.setStyleSheet(self.rightHeaderSheet)

        self.directorsBox = QGridLayout()
        self.directorsBox.setContentsMargins(0, 0, 0, 0)
        self.directorsBox.setAlignment(Qt.AlignLeading)

        self.directorsList = self.info['Directors']
        if len(self.directorsList) > 4:
            self.directorsList = self.directorsList[:4]
        self.directorsNum = len(self.directorsList)

        for i in range(self.directorsNum):
            row = i // 2
            column = i % 2
            directorBtn = QPushButton(self.directorsList[i])

            directorBtn.setStyleSheet('QPushButton{background-color:#548B54; color:#C1FFC1; font-family:"楷体"; font-size: 19px;}'
                                      'QPushButton:hover{background-color:#7CFC00; color:#6B8E23; font-family:"楷体"; font-size: 19px;}')
            directorBtn.setCursor(QCursor(Qt.PointingHandCursor))
            directorBtn.clicked[bool].connect(self.directorInfoResponse)

            if self.directorsList[i] not in self.info['ValidDirectors']:
                directorBtn.setCursor(QCursor(Qt.CrossCursor))
                directorBtn.setDisabled(True)
                directorBtn.setStyleSheet(
                    'QPushButton{background-color:#556B2F; color:#C0FF3E; font-family:"楷体"; font-size: 19px;}')

            self.directorsBox.addWidget(directorBtn, row, column)

        self.directorsLayout = QHBoxLayout()
        self.directorsLayout.addWidget(self.directorsLabel, 1)
        self.directorsLayout.addLayout(self.directorsBox, 5)

        self.starringList = self.info['Starring']
        if len(self.starringList) > 8:
            self.starringList = self.starringList[:8]
        self.starringNum = len(self.starringList)

        self.starringHeader = QLabel('主演: ')
        self.starringHeader.setStyleSheet(self.rightHeaderSheet)

        self.starringBox = QGridLayout()
        self.starringBox.setAlignment(Qt.AlignLeading)
        self.starringBox.setContentsMargins(0, 0, 0, 0)

        for i in range(self.starringNum):
            row = i // 2
            column = i % 2
            starBtn = QPushButton(self.starringList[i])

            if self.starringList[i] not in self.info['ValidStarring']:
                starBtn.setCursor(QCursor(Qt.ForbiddenCursor))
                # starBtn.setDisabled(True)
                starBtn.setStyleSheet(
                    'QPushButton{background-color:#8B7355; color:#FFE7BA; font-family:"楷体"; font-size: 19px;}')
            else:
                starBtn.setCursor(QCursor(Qt.PointingHandCursor))
                starBtn.setStyleSheet(
                    'QPushButton{background-color:#FAEBD7; color:#8B4726; font-family:"楷体"; font-size: 19px;}'
                    'QPushButton:hover{background-color:#FF4500; color:#F5DEB3; font-family:"楷体"; font-size: 19px;}')
                starBtn.clicked[bool].connect(self.starInfoResponse)

            self.starringBox.addWidget(starBtn, row, column)

        self.starringLayout = QHBoxLayout()
        self.starringLayout.addWidget(self.starringHeader, 1)
        self.starringLayout.addLayout(self.starringBox, 5)

        self.picLeftLayout = QVBoxLayout()
        self.picLeftLayout.addLayout(self.genresLayout)
        self.picLeftLayout.addLayout(self.ratingLayout)
        self.picLeftLayout.addLayout(self.yearLayout)
        self.picLeftLayout.addLayout(self.nationLayout)
        self.picLeftLayout.addLayout(self.lengthLayout)
        self.picLeftLayout.addLayout(self.directorsLayout)
        self.picLeftLayout.addLayout(self.starringLayout)
        self.picLeftLayout.setSpacing(14)

        self.rightFrame.setLayout(self.picLeftLayout)
        self.rightFrame.setContentsMargins(12, 0, 8, 0)
        self.rightFrame.setStyleSheet('QFrame{background-color: #BEBEBE; border-style: groove;}')
        self.rightFrame.setFixedHeight(400)

        self.InfoLayout = QHBoxLayout()
        self.InfoLayout.addWidget(self.picLabel)
        self.InfoLayout.addWidget(self.rightFrame)
        self.InfoLayout.setContentsMargins(20, 0, 20, 0)
        self.InfoLayout.setSpacing(20)

        self.InfoFrame = QFrame()
        self.InfoFrame.setLayout(self.InfoLayout)
        self.InfoFrame.setFixedHeight(400)

        #self.summary = self.info['Summary']
        self.summary = self.info['Summary']
        if len(self.summary) > 300:
            self.summary = self.summary[:300] + '...'
        self.summaryLabel = QLabel('    ' + self.summary)
        self.summaryLabel.setWordWrap(True)
        self.summaryLabel.setAlignment(Qt.AlignCenter)
        self.summaryLabel.setFont(QFont('华文楷体'))
        self.summaryLabel.setStyleSheet('QLabel{font-size:15px;}')

        self.moviesInfoLayout = QVBoxLayout()
        self.moviesInfoLayout.addLayout(self.headerLayout)
        self.moviesInfoLayout.addWidget(self.InfoFrame)
        self.moviesInfoLayout.addWidget(self.summaryLabel)
        self.moviesInfoLayout.setStretch(0, 20)
        self.moviesInfoLayout.setStretch(1, 90)
        self.moviesInfoLayout.setStretch(2, 90)
        self.moviesInfoLayout.setSpacing(20)

        self.moviesWidget = QWidget()
        self.moviesWidget.setLayout(self.moviesInfoLayout)

        self.setContentsMargins(10, 0, 10, 10)
        self.setCentralWidget(self.moviesWidget)
        self.setWindowTitle(self.info['Title'] + ' - FelKub Movies Archive')
        self.setWindowIcon(QIcon('icon/Movie-icon.png'))
        self.resize(560, 720)

    def genreResponse(self):
        source = self.sender()
        genre = source.text()

        self.newFrame = QMainWindow()
        self.newFrame.setCentralWidget(MoviesPage.MoviesDisplay(1, get_movies_of_genre(genre)))

        self.newWindowLayout = QHBoxLayout()
        self.newWindowLayout.addWidget(self.newFrame)

        self.newWindow = QWidget()
        self.newWindow.setLayout(self.newWindowLayout)
        self.newWindow.resize(560, 680)
        self.newWindow.move(30, 14)
        self.newWindow.show()

    def nationResponse(self):
        source = self.sender()
        nation = source.text()

        self.newFrame = QMainWindow()
        self.newFrame.setCentralWidget(MoviesPage.MoviesDisplay(1, get_movies_of_nation(nation)))

        self.newWindowLayout = QHBoxLayout()
        self.newWindowLayout.addWidget(self.newFrame)

        self.newWindow = QWidget()
        self.newWindow.setLayout(self.newWindowLayout)
        self.newWindow.resize(560, 680)
        self.newWindow.move(30, 14)
        self.newWindow.show()

    def recommendPageResponse(self):
        self.recommender = RecommenderPage(self.info)
        self.recommender.show()

    def directorInfoResponse(self):
        print(1)
        source = self.sender()
        director = source.text()
        director_info = get_director_info_of_name(director)
        movies_info = get_movies_directed_by(director)
        print(director_info, movies_info)
        self.detailed = DirectorDetailed.DirectorDetailedInfo(director_info, movies_info)
        print(2)
        self.detailed.show()

    def starInfoResponse(self):
        source = self.sender()
        star = source.text()
        star_info = get_star_info_of_name(star)
        self.detailed = StarDetailed.StarDetailedInfo(star_info, get_movies_starred_by(star))
        self.detailed.show()

    def editTraitsResponse(self):
        self.detailed = MovieTraitsEditPage(self.info)
        self.detailed.show()