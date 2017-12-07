#!/usr/bin/env python3
# -*- coding:utf-8 -*-
u"""
2017.12.07
学习使用PyQt5
"""
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


__dir__ = os.path.dirname(os.path.abspath(__file__))


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        u"""
        设置GUI
        """
        # 打开在桌面中心
        self.center()

        # 添加菜单栏
        self._add_menubar_()

        # 设置状态栏，左下角的状态信息
        self.statusBar().showMessage('Ready')

        # 设定布局
        self._set_grid_()

        # 调整窗口大小，设定窗口标题等
        self.resize(1000, 500)
        self.setWindowTitle('Kcptun GUI')
        self.setWindowIcon(QIcon(os.path.join(__dir__, 'icon/k.png')))
        self.show()

    def _set_grid_(self):
        u"""
        设定布局
        """
        widget = QWidget()          # 由于使用的是QMainWindow，而最终的grid只能针对QWidget，因此需要先设定Widget
        grid = QGridLayout()

        # 添加按钮
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        grid.addWidget(self._add_quit_button_(), 5, 5)
        grid.addWidget(self._add_run_button_(), 4, 5)

        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def _add_quit_button_(self):
        u"""
        添加退出按钮
        """
        qbtn = QPushButton('Quit', self)
        qbtn.setToolTip("退出")
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        # qbtn.move(850, 450)
        return qbtn

    def _add_run_button_(self):
        u"""
        添加运行按钮
        """
        rbtn = QPushButton("Run", self)
        rbtn.setToolTip("运行")
        rbtn.resize(rbtn.sizeHint())
        # rbtn.move(750, 450)
        return rbtn

    def _add_menubar_(self):
        u"""
        添加工具栏
        """
        # 退出选项
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        # 菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

    def closeEvent(self, event):
        u"""
        quit 退出消息
        """
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        u"""
        窗口初始化居中
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    print(os.path.join(__dir__, 'icon/k.png'))
    app = QApplication(sys.argv)

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()

    ex = Example()
    sys.exit(app.exec_())
