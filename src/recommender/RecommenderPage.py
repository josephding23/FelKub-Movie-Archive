from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
from src.database.DataQuery import *
from math import ceil
from src.detail import MovieDetailed


class RecommenderMovieInfoGrid(QFrame):
    def __init__(self, info, long_describe, short_describe):

        self.info = info
        self.long_describe = long_describe

        '''
        if len(self.describe) > 16:
            self.describe = self.describe[0:16] + '\n   ' + self.describe[16:]
        if len(self.describe) > 32:
            self.describe = self.describe[:32] + '...'
        '''

        self.short_describe = short_describe
        super().__init__()
        self.initUI()

    # (title, pic_name, rating, nation, year, length)
    def initUI(self):
        self.lblSheet = 'QLabel{font-family:"微软雅黑";}'
        self.title = self.info['Title']
        if len(self.title) > 11:
            self.title = self.title[:11] + '...'
        self.titleLable = QPushButton(self.title)
        self.titleLable.clicked[bool].connect(self.movieInfoResponse)
        self.titleLable.setCursor(QCursor(Qt.PointingHandCursor))
        self.titleLable.setStyleSheet(
            'QPushButton{font-size: 14px; color: #1C1C1C; font-weight: bold; font-family:"微软雅黑"; background-color: #FFFFF0}'
            'QPushButton:hover{font-size: 14px; color: #1C1C1C; font-weight: bold; font-family:"微软雅黑"; background-color: #A9A9A9}'
        )

        self.describeLable = QLabel(self.short_describe)
        self.describeLable.setStyleSheet(
            'QLabel{font-size: 16px; font-family: "楷体";}'
        )
        self.describeLable.setAlignment(Qt.AlignCenter)

        self.infoLayout = QVBoxLayout()
        self.infoLayout.addWidget(self.titleLable)
        self.infoLayout.addWidget(self.describeLable)

        self.picLable = QLabel()
        self.pixmap = QPixmap()
        picUrl = 'pic/movies/mini/' + self.info['PicName']
        self.pixmap.load(picUrl)
        self.pixmap = self.pixmap.scaled(54, 80)
        self.picLable.setScaledContents(True)
        self.picLable.setPixmap(self.pixmap)
        self.picLable.setFixedWidth(80)

        self.movieLayout = QHBoxLayout()
        self.movieLayout.addWidget(self.picLable)
        self.movieLayout.addLayout(self.infoLayout)
        self.movieLayout.setContentsMargins(0, 0, 0, 0)

        self.setToolTip(self.long_describe)
        self.setStyleSheet('QFrame{background-color: #CDC673;}')
        # self.movieLayout.addWidget(self.detailedBtn)
        # self.movieLayout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.movieLayout)
        self.setFixedWidth(255)
        self.setFixedHeight(100)


    def movieInfoResponse(self):
        self.detailed = MovieDetailed.MovieDetailedInfo(self.info)
        self.detailed.show()
        # self.detailed.exec_()


class DisplayPage(QWidget):
    def __init__(self, page, movies_info, long_describes, short_describes):

        super().__init__()
        self.page = page
        self.movies_info = movies_info
        self.long_describes = long_describes
        self.short_describes = short_describes
        self.initUI()

    def initUI(self):
        self.itemPerPage = 4

        self.startNum = (self.page - 1) * self.itemPerPage
        self.endNum = self.page * self.itemPerPage
        if len(self.movies_info) < self.endNum:
            self.endNum = len(self.movies_info)
            self.itemPerPage = self.endNum - self.startNum

        self.moviesLayout = QHBoxLayout()
        self.movies_list = self.movies_info[self.startNum: self.endNum]
        self.long_describe_list = self.long_describes[self.startNum: self.endNum]
        self.short_describe_list = self.short_describes[self.startNum: self.endNum]

        for i in range(self.itemPerPage):
            movieWidget = RecommenderMovieInfoGrid(self.movies_list[i], self.long_describe_list[i], self.short_describe_list[i])
            self.moviesLayout.addWidget(movieWidget)

        self.moviesLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.moviesLayout)
        self.setContentsMargins(0, 0, 0, 0)


class MoviesDisplay(QWidget):
    def __init__(self, page, movies_info, long_describes, short_describes):
        super().__init__()
        self.page = page
        self.movies_info = movies_info
        self.long_describes = long_describes
        self.short_describes = short_describes
        self.max_page = ceil(len(self.movies_info) / 4)
        if self.max_page == 0:
            self.max_page = 1
        self.initUI()

    def initUI(self):

        self.pageSheet = 'QPushButton{background-color:#B4EEB4;}' \
                         'QPushButton:hover{background-color:#8470FF;}' \
                         'QPushButton:pressed{background-color:#E0FFFF;}'
        self.previousPageBtn = QPushButton(self)
        self.previousPageBtn.setIcon(QIcon('icon/Actions-go-previous-icon.png'))
        self.previousPageBtn.setStyleSheet(self.pageSheet)
        self.previousPageBtn.setMaximumWidth(64)
        self.previousPageBtn.setIconSize(QSize(32, 32))
        self.previousPageBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)

        self.itemBox = QMainWindow()
        self.itemBox.setCentralWidget(DisplayPage(self.page, self.movies_info, self.long_describes, self.short_describes))
        self.itemBox.setContentsMargins(0, 0, 0, 0)

        self.nextPageBtn = QPushButton(self)
        self.nextPageBtn.setIcon(QIcon('icon/Actions-go-next-icon.png'))
        self.nextPageBtn.setStyleSheet(self.pageSheet)
        self.nextPageBtn.setMaximumWidth(40)
        self.nextPageBtn.setIconSize(QSize(32, 32))
        self.nextPageBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)

        self.previousPageBtn.clicked[bool].connect(self.previousPageResponse)
        self.nextPageBtn.clicked[bool].connect(self.nextPageResponse)

        self.wholeLayout = QHBoxLayout()
        self.wholeLayout.addWidget(self.previousPageBtn)
        self.wholeLayout.addWidget(self.itemBox)
        self.wholeLayout.addWidget(self.nextPageBtn)
        self.wholeLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.wholeLayout)
        self.setContentsMargins(10, 0, 0, 10)

    def previousPageResponse(self):
        self.page = self.page - 1
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)
        else:
            self.previousPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)
        else:
            self.nextPageBtn.setDisabled(False)
        self.itemBox.setCentralWidget(DisplayPage(self.page, self.movies_info, self.long_describes, self.short_describes))


    def nextPageResponse(self):
        self.page = self.page + 1
        if self.page == 1:
            self.previousPageBtn.setDisabled(True)
        else:
            self.previousPageBtn.setDisabled(False)
        if self.page == self.max_page:
            self.nextPageBtn.setDisabled(True)
        else:
            self.nextPageBtn.setDisabled(False)
        self.itemBox.setCentralWidget(DisplayPage(self.page, self.movies_info, self.long_describes, self.short_describes))


class RecommenderPage(QMainWindow):

    def __init__(self, info):
        super().__init__()
        self.id = info['IMDB']
        self.title = info['Title']
        (self.common_genres_movies, self.common_tags_movies) = \
            get_movies_with_related_tags_and_genres(self.id)
        (self.common_directors_movies, self.common_starring_movies, self.common_casts_movies) = \
            get_movies_with_related_casts(self.id)
        self.similar_traits_movies = get_movies_with_similar_traits(self.id)
        self.traitsOrder = get_traits_order()
        self.translation = get_traits_translation()
        self.initUI()

    def initUI(self):

        self.recommenderLayout = QVBoxLayout()

        self.recommenderLayout.addWidget(QLabel('特征属性相似度最高的电影: '), 2)
        long_describes = list()
        short_describes = list()
        for movie in self.similar_traits_movies:
            long_describe = str()
            for key in self.traitsOrder:
                long_describe = long_describe + self.translation[key] + ': ' + str(movie['Traits'][key]) + '\n'
            long_describe = long_describe[:-1]
            long_describes.append(long_describe)
            short_describes.append('相似度: ' + str(movie['Distance']))
        self.recommenderLayout.addWidget(MoviesDisplay(1, self.similar_traits_movies, long_describes, short_describes), 3)

        self.recommenderLayout.addWidget(QLabel('包含相同导演的电影: '), 2)
        long_describes = list()
        short_describes = list()
        for movie in self.common_directors_movies:
            long_describes.append(str(movie['CommonDirectorsNum']) + '名相同导演: ' + ', '.join(movie['CommonDirectors']))
            short_describes.append(str(movie['CommonDirectorsNum']) + '导演')
        self.recommenderLayout.addWidget(MoviesDisplay(1, self.common_directors_movies, long_describes, short_describes), 3)

        self.recommenderLayout.addWidget(QLabel('包含相同演员的电影: '), 2)
        long_describes = list()
        short_describes = list()
        for movie in self.common_starring_movies:
            long_describes.append(str(movie['CommonStarringNum']) + '名相同演员: ' + ', '.join(movie['CommonStarring']))
            short_describes.append(str(movie['CommonStarringNum']) + '演员')
        self.recommenderLayout.addWidget(MoviesDisplay(1, self.common_starring_movies, long_describes, short_describes), 3)

        self.recommenderLayout.addWidget(QLabel('类别相同的电影: '), 2)
        long_describes = list()
        short_describes = list()
        for movie in self.common_genres_movies:
            long_describes.append(str(movie['CommonGenresNum']) + '相同类别: ' + ', '.join(movie['CommonGenres']))
            short_describes.append(str(movie['CommonGenresNum']) + '类别')
        self.recommenderLayout.addWidget(MoviesDisplay(1, self.common_genres_movies, long_describes, short_describes), 3)

        self.recommenderLayout.addWidget(QLabel('包含相同标签的电影: '), 2)
        long_describes = list()
        short_describes = list()
        for movie in self.common_tags_movies:
            long_describes.append(str(movie['CommonTagsNum']) + '相同标签: ' + ', '.join(movie['CommonTags']))
            short_describes.append(str(movie['CommonTagsNum']) + '标签')
            # self.sameTags.addWidget(RecommenderMovieInfoGrid(movie))
        self.recommenderLayout.addWidget(MoviesDisplay(1, self.common_tags_movies, long_describes, short_describes), 3)

        self.recommenderWidget = QWidget()
        self.recommenderWidget.setLayout(self.recommenderLayout)
        self.recommenderWidget.setStyleSheet('QFrame{background-color: #CDC673;}'
                                             'QLabel{font-size: 16px; font-family: "楷体"; background-color: #CFCFCF}')

        self.wholeLayout = QVBoxLayout()
        # self.wholeLayout.addLayout(self.headerLayout)
        self.wholeLayout.addWidget(self.recommenderWidget)

        self.wholeWidget = QWidget()
        self.wholeWidget.setLayout(self.wholeLayout)

        self.setCentralWidget(self.wholeWidget)
        self.setWindowTitle(self.title + ' 的相关推荐 - FelKub Movies Archive')
        self.setWindowIcon(QIcon('icon/star-icon.png'))
        self.setMaximumWidth(1080)
        self.setMaximumHeight(800)
        self.move(10, 30)
        #self.resize(1080, 700)
