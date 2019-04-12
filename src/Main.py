# coding=utf-8
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
import sys
from src.MoviesArchive import MoviesArchive

class FelKub(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        mainMenu = self.menuBar()

        indexMenu = mainMenu.addMenu('主页')
        moviesMenu = mainMenu.addMenu('电影')
        directorsMenu = mainMenu.addMenu('导演')
        starringMenu = mainMenu.addMenu('演员')
        genresMenu = mainMenu.addMenu('类别')
        '''

        self.setCentralWidget(MoviesArchive())
        self.resize(1080, 750)
        self.setFixedSize(self.width(), self.height())
        self.move(150, 20)
        self.setWindowIcon(QIcon('icon/1-Movies-icon.png'))
        self.setWindowTitle('费库电影档案系统 - FelKub Movies Archive')
        # self.center()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FelKub()
    ex.setWindowOpacity(0.95)
    sys.exit(app.exec_())