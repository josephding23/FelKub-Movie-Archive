from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QComboBox, QPushButton, QMainWindow
from PyQt5.Qt import QHBoxLayout, QVBoxLayout, Qt, QSize
from src.database.DataQuery import advanced_search_movies
from src.pages.MoviesPage import MoviesDisplay

class AdvancedSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sheet = 'QLineEdit{font-family: "楷体"; font-size:25px; background-color: #FFDAB9;} ' \
                     'QLineEdit:hover{font-family: "楷体"; font-size:25px; background-color: #FFF68F;} ' \
                     'QComboBox{font-family: "楷体"; font-size:18px; background-color:#8B4C39; color:#FFDEAD;} ' \
                     'QLabel{font-family: "华文行楷"; font-size: 22px; color: #A0522D;}' \
                     'QPushButton{font-family: "幼圆"; font-size: 24px; background-color: #0000CD; color: #7FFF00}' \
                     'QPushButton:hover{font-family: "幼圆"; font-size: 24px; background-color: #87CEEB; color: #556B2F}'

        self.titleLabel = QLabel('输入标题：')
        self.titleField = QLineEdit()
        self.titleBox = QHBoxLayout()
        self.titleBox.addWidget(self.titleLabel)
        self.titleBox.addWidget(self.titleField)
        self.titleBox.setContentsMargins(0, 30, 0, 0)

        self.yearLabel = QLabel('选择起始年：')
        self.yearLists = list()

        self.yearFromLabel = QLabel('从')
        self.yearFromField = QComboBox()
        self.yearFromField.setMinimumHeight(40)

        self.yearToLabel = QLabel('至')
        self.yearToField = QComboBox()
        self.yearToField.setMinimumHeight(40)

        for i in range(1898, 2019):
            self.yearFromField.addItem(str(i))
            self.yearToField.addItem(str(2019 - (i - 1899)))

        self.yearFromBox = QHBoxLayout()
        self.yearFromBox.addWidget(self.yearFromLabel)
        self.yearFromBox.addWidget(self.yearFromField)
        self.yearFromBox.setAlignment(Qt.AlignLeading)
        self.yearFromBox.setSpacing(10)


        self.yearToBox = QHBoxLayout()
        self.yearToBox.addWidget(self.yearToLabel)
        self.yearToBox.addWidget(self.yearToField)
        self.yearToBox.setAlignment(Qt.AlignLeading)
        self.yearToBox.setSpacing(10)

        self.yearSearchHBox = QHBoxLayout()
        self.yearSearchHBox.addLayout(self.yearFromBox)
        self.yearSearchHBox.addLayout(self.yearToBox)
        self.yearSearchHBox.setAlignment(Qt.AlignCenter)
        self.yearSearchHBox.setSpacing(80)

        self.yearSearchBox = QVBoxLayout()
        self.yearSearchBox.addWidget(self.yearLabel)
        self.yearSearchBox.addLayout(self.yearSearchHBox)
        self.yearSearchBox.setSpacing(10)

        self.ratingLabel = QLabel('选择评分区间：')

        self.ratingFromField = QComboBox()
        self.ratingFromField.setMinimumWidth(100)
        self.ratingFromField.setMinimumHeight(40)

        self.ratingToLabel = QLabel('~')

        self.ratingToField = QComboBox()
        self.ratingToField.setMinimumWidth(100)
        self.ratingToField.setMinimumHeight(40)

        for i in range(1, 11):
            self.ratingFromField.addItem(str(i))
            self.ratingToField.addItem(str(11 - i))

        self.ratingSearchHBox = QHBoxLayout()
        self.ratingSearchHBox.addWidget(self.ratingFromField)
        self.ratingSearchHBox.addWidget(self.ratingToLabel)
        self.ratingSearchHBox.addWidget(self.ratingToField)
        self.ratingSearchHBox.setAlignment(Qt.AlignCenter)
        self.ratingSearchHBox.setSpacing(40)

        self.ratingSearchBox = QVBoxLayout()
        self.ratingSearchBox.addWidget(self.ratingLabel)
        self.ratingSearchBox.addLayout(self.ratingSearchHBox)
        self.ratingSearchBox.setSpacing(10)

        self.lengthLabel = QLabel('请选择长度区间：')

        self.lengthFromField = QLineEdit()
        self.lengthFromField.setMaximumWidth(300)
        self.lengthToLabel = QLabel('~')
        self.lengthToField = QLineEdit()
        self.lengthToField.setMaximumWidth(300)

        self.lengthHBox = QHBoxLayout()
        self.lengthHBox.addWidget(self.lengthFromField)
        self.lengthHBox.addWidget(self.lengthToLabel)
        self.lengthHBox.addWidget(self.lengthToField)
        self.lengthHBox.setAlignment(Qt.AlignCenter)
        self.lengthHBox.setContentsMargins(100, 0, 100, 0)
        self.lengthHBox.setSpacing(10)

        self.lengthBox = QVBoxLayout()
        self.lengthBox.addWidget(self.lengthLabel)
        self.lengthBox.addLayout(self.lengthHBox)
        self.lengthBox.setSpacing(10)

        self.searchBtn = QPushButton('检索电影')
        self.searchBtn.setFixedSize(QSize(200, 50))
        self.searchBtn.setCursor(Qt.PointingHandCursor)
        self.searchBtn.clicked[bool].connect(self.advancedSearch)
        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.searchBtn)
        self.searchLayout.setContentsMargins(0, 0, 0, 40)
        self.searchLayout.setAlignment(Qt.AlignRight)

        self.wholeLayout = QVBoxLayout()
        self.wholeLayout.addLayout(self.titleBox)
        self.wholeLayout.addLayout(self.yearSearchBox)
        self.wholeLayout.addLayout(self.ratingSearchBox)
        self.wholeLayout.addLayout(self.lengthBox)
        self.wholeLayout.addLayout(self.searchLayout)
        self.wholeLayout.setSpacing(80)

        self.advancedWidget = QWidget()
        self.advancedWidget.setLayout(self.wholeLayout)
        self.advancedWidget.setStyleSheet(self.sheet)

        self.centralWindow = QMainWindow()
        self.centralWindow.setCentralWidget(self.advancedWidget)
        self.centralWindow.setContentsMargins(5, 0, 0, 0)

        self.advancedLayout = QVBoxLayout()
        self.advancedLayout.addWidget(self.centralWindow)
        self.advancedLayout.setSpacing(0)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.advancedLayout)
        self.setFixedWidth(800)

    def advancedSearch(self, pressed):

        title = self.titleField.text()

        yearFrom = int(self.yearFromField.currentText())
        yearTo = int(self.yearToField.currentText())

        ratingFrom = float(self.ratingFromField.currentText())
        ratingTo = float(self.ratingToField.currentText())

        lengthFrom = 0
        if self.lengthFromField.text() != '':
            lengthFrom = int(self.lengthFromField.text())
        lengthTo = 1000
        if self.lengthToField.text() != '':
            lengthTo = int(self.lengthToField.text())

        self.centralWindow.setCentralWidget(MoviesDisplay(1, advanced_search_movies(title,
                                                                                    yearFrom, yearTo,
                                                                                    ratingFrom, ratingTo,
                                                                                    lengthFrom, lengthTo)))
