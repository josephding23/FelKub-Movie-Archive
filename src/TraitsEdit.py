from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QGridLayout, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
from src import MoviesPage
from src.DataQuery import *


class EditColumn(QWidget):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        self.translation = get_traits_translation()
        self.initUI()

    def initUI(self):
        self.genreLabel = QLabel(self.translation[self.name] + ':')
        self.genreLabel.setFont(QFont('黑体'))
        self.genreLabel.setStyleSheet('QLabel{font-size:16px}')

        self.genreField = QLineEdit()
        # self.genreField.setMaximumWidth(480)
        # self.genreField.setFixedHeight(21)
        self.genreField.setFont(QFont('楷体'))
        self.genreField.setText(str(self.value))
        self.genreField.setAlignment(Qt.AlignCenter)
        self.genreField.setCursor(QCursor(Qt.IBeamCursor))
        self.genreField.setFixedWidth(150)
        self.genreField.setFixedHeight(25)
        self.genreField.setStyleSheet('QLineEdit{font-size:16px;}')

        self.genreLayout = QHBoxLayout()
        self.genreLayout.addWidget(self.genreLabel, 2)
        self.genreLayout.addWidget(self.genreField, 3)

        self.genreLayout.setStretch(0, 3)
        self.genreLayout.setStretch(1, 5)
        self.setLayout(self.genreLayout)

    def getValue(self):
        return (self.name, self.genreField.text())

class GenreEditPage(QMainWindow):
    def __init__(self, info):
        super().__init__()
        self.info = info
        self.traitsOrder = get_traits_order()
        self.initUI()

    def initUI(self):
        self.name = self.info['Name']
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setStyleSheet(
            'QLabel{font-family:"华文行楷";color: brown;font-weight:bold;font-size:36px;}'
        )

        self.returnBtn = QPushButton()
        self.returnBtn.setIcon(QIcon('icon/Actions-edit-undo-icon.png'))
        self.returnBtn.setIconSize(QSize(32, 32))
        self.returnBtn.clicked[bool].connect(self.close)
        self.returnBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.nameLabel)
        self.headerLayout.addWidget(self.returnBtn)
        self.headerLayout.setStretch(0, 6)
        self.headerLayout.setStretch(1, 4)

        self.traitsLayout = QGridLayout()
        self.traitsLayout.setSpacing(8)

        self.btnSet = list()
        self.traits = get_traits_of_genre(self.name)
        for key in self.traitsOrder:
            self.btnSet.append(EditColumn(key, self.traits[key]))

        num = 0
        for btn in self.btnSet:
            # value = self.traits[key]
            row = num / 2
            column = num % 2

            self.traitsLayout.addWidget(btn, row, column)
            num = num + 1

        self.ackBtn = QPushButton('修改')
        self.ackBtn.clicked[bool].connect(self.editValues)

        self.wholeLayout = QVBoxLayout()
        self.wholeLayout.addLayout(self.headerLayout)
        self.wholeLayout.addLayout(self.traitsLayout)
        self.wholeLayout.addWidget(self.ackBtn)

        self.wholeWidget = QWidget()
        self.wholeWidget.setLayout(self.wholeLayout)
        self.setCentralWidget(self.wholeWidget)
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon('icon/Movie-icon.png'))
        self.resize(500, 300)

    def editValues(self):
        value_dict = dict()
        for btn in self.btnSet:
            value = btn.getValue()
            value_dict[value[0]] = float(value[1])

        change_genres_traits(self.name, value_dict)


class MovieTraitsEditPage(QMainWindow):
    def __init__(self, info):
        super().__init__()
        self.info = info
        self.traitsOrder = get_traits_order()
        self.translation = get_traits_translation()
        self.initUI()

    def initUI(self):
        self.name = self.info['Title']
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setStyleSheet(
            'QLabel{font-family:"华文行楷";color: brown;font-weight:bold;font-size:28px;}'
        )

        self.returnBtn = QPushButton()
        self.returnBtn.setIcon(QIcon('icon/Actions-edit-undo-icon.png'))
        self.returnBtn.setIconSize(QSize(32, 32))
        self.returnBtn.setFixedSize(QSize(40, 40))
        self.returnBtn.clicked[bool].connect(self.close)
        self.returnBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.nameLabel, 5)
        self.headerLayout.addWidget(self.returnBtn, 1)

        self.traitsLayout = QGridLayout()
        self.traitsLayout.setSpacing(8)

        self.btnSet = list()
        self.traits = get_traits_of_movie(self.info['IMDB'])
        for key in self.traitsOrder:
            self.btnSet.append(EditColumn(key, self.traits[key]))

        num = 0
        for btn in self.btnSet:
            # value = self.traits[key]
            row = num / 2
            column = num % 2

            self.traitsLayout.addWidget(btn, row, column)
            num = num + 1

        self.ackBtn = QPushButton('修改')
        self.ackBtn.setFixedHeight(50)
        self.ackBtn.setFixedWidth(80)
        self.ackBtn.setStyleSheet('QPushButton{font-family:"隶书"; font-size: 20px; background-color:#FFEFDB; color:#8B4513;}'
                                  'QPushButton:hover{font-family:"隶书"; font-size: 20px; background-color:#CD5B45; color:#FFDEAD;}'
                                  'QPushButton:pressed{font-family:"隶书"; font-size: 22px; background-color:#8B2252; color:#FF34B3;}')
        self.ackBtn.setCursor(Qt.PointingHandCursor)
        self.ackBtn.clicked[bool].connect(self.editValues)

        self.wholeLayout = QVBoxLayout()
        self.wholeLayout.addLayout(self.headerLayout)
        self.wholeLayout.addLayout(self.traitsLayout)
        self.wholeLayout.addWidget(self.ackBtn, alignment=Qt.AlignCenter)

        self.wholeWidget = QWidget()
        self.wholeWidget.setLayout(self.wholeLayout)
        self.setCentralWidget(self.wholeWidget)
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon('icon/Movie-icon.png'))
        self.resize(500, 300)

    def editValues(self):
        value_dict = dict()
        for btn in self.btnSet:
            value = btn.getValue()
            value_dict[value[0]] = float(value[1])

        change_movie_traits(self.info['IMDB'], value_dict)

        confirm = QMessageBox()
        confirm.setIcon(QMessageBox.Information)
        confirm.setText('修改成功！')
        self.confirmInfo = str()
        for key in self.traitsOrder:
            self.confirmInfo = self.confirmInfo + self.translation[key] + ': ' + str(value_dict[key]) + '\n'
        self.confirmInfo = self.confirmInfo[:-1]
        confirm.setDetailedText('属性已修改为:\n' + self.confirmInfo)
        confirm.setWindowTitle("属性修改成功")
        confirm.setStandardButtons(QMessageBox.Ok)
        confirm.setFixedSize(QSize(750, 500))
        confirm.setWindowIcon(QIcon('icon/information-icon.png'))
        confirm.exec_()
