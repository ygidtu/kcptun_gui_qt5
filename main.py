#!/usr/bin/env python3
# -*- coding:utf-8 -*-
u"""
2017.12.07
学习使用PyQt5
"""
import os
import sys
import json
from copy import deepcopy
from functools import partial
from itertools import chain
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from src.base_ui import BasicWindow
from src.ico import qt_resource_data


__dir__ = os.path.dirname(os.path.abspath(__file__))
__config__ = os.path.join(os.path.join(__dir__, "config.json"))


def get_key_by_value(dict_, value_):
    for key, value in dict_.items():
        if value == value_:
            return key


class Example(BasicWindow):
    u"""
    样本
    """

    def __init__(self):
        u"""
        初始化，
        """
        super().__init__()

        self.load_default_settings()       # load default settings
        self.init_menu()
        self.init_tray()
        self.initUI()
        self.set_relation_between_inputs()

        # 绑定一堆动作
        self.exe_select.clicked.connect(partial(self.set_open_file_dialog, self.executable, True))
        self.json_select.clicked.connect(partial(self.set_open_file_dialog, self.json_path, False))

        self.start.clicked.connect(self.start_kcptun)
        self.stop.clicked.connect(self.stop_kcptun)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)

    def load_default_settings(self):
        u"""
        读取默认设置
        """
        try:
            if os.path.exists(__config__):
                with open(__config__) as r:
                    self.__config__ = json.load(r)
                return None
        except json.decoder.JSONDecodeError:
            pass
        finally:
            self.__config__ = {
                "config": True,
                "config_path": None,
                "exe": None,
                "paras": None
            }
            with open(__config__, "w+") as w:
                json.dump(self.__config__, w, indent=4)


    def initUI(self):
        u"""
        设置GUI
        """
        # 打开在桌面中心
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # 设置状态栏，左下角的状态信息
        self.statusBar.showMessage('Kcptun GUI')
        self.setWindowTitle('Kcptun GUI')
        self.setWindowIcon(QIcon(":k.ico"))

        # 根据默认参数设置，根据是否使用config来设定参数
        if self.__config__["config"] is False:
            self.json.setChecked(False)
            self.json_path.setEnabled(False)
            self.json_select.setEnabled(False)

            tem = [self.l_line, self.r_line, self.p_line]
            [x.setEnabled(True) for x in tem]

            for key, value in self.elements.items():
                key.setEnabled(True)

        # 设定程序或者json文件的路径
        if self.__config__["exe"]:
            self.executable.setText(self.__config__["exe"])
        if self.__config__["config_path"]:
            self.json_path.setText(self.__config__["config_path"])
        
        # 设定其他参数
        if self.__config__["paras"]:
            for key, value in self.__config__["paras"].items():
                element = self.parameters[key]
                if value not in ("::", ""):
                    element.setEnabled(True)

                    key1 = get_key_by_value(self.elements, element)
                    if key1:
                        key1.setEnabled(True)
                        key1.setChecked(True)

                if isinstance(element, QLineEdit):
                    element.setText(value)
                elif isinstance(element, QComboBox):
                    index = element.findText(value, Qt.MatchFixedString)
                    if index >= 0:
                        element.setCurrentIndex(index)
        self.show()

    u"""设定菜单栏"""
    def init_menu(self):
        # 添加菜单栏
        # 退出选项
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        # 菜单栏
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(exitAct)

    u"""系统托盘"""
    def init_tray(self):
        u"""
        设定系统托盘的功能
        """
        # 设定系统托盘选项
        self.tray_icon = QSystemTrayIcon(QIcon(os.path.join(__dir__, 'icon/k.png')), self)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.iconActivated)  

    def iconActivated(self, reason):
        '''
        激活托盘功能
        :param reason: 
        :return: 
        '''
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            if self.isHidden():  
                self.show()  
            else:  
                self.hide()

    def closeEvent(self, event):
        u"""
        quit 退出消息
        """
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        self.process.terminate()
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    u"""绑定各种按钮和元件"""
    def checked(self, controler, element):
        u"""
        启用某些元件
        """
        element.setEnabled(controler.isChecked())
    
    def unchecked(self, controler, element):
        u"""
        启用某些元件
        """
        element.setEnabled( not controler.isChecked())
    
    def disable(self, controlor, element):
        if self.json.isChecked():
            element.setEnabled(False)
            self.json_select.setEnabled(True)
            self.__config__.update({"config": True})
        else:
            self.__config__.update({"config": False})
            self.json_select.setEnabled(False)
            element.setEnabled(controlor.isChecked())

    def set_relation_between_inputs(self):
        u"""
        checkbox and input line relation
        """
        # 各参数与输入框联动
        for key, value in self.elements.items():
            key.toggled.connect(partial(self.disable, key, value))
            self.json.toggled.connect(partial(self.disable, key, value))

        # 将json与各子原件勾连
        tem = list(self.elements.keys()) + [self.l_line, self.r_line, self.p_line]
        self.json.toggled.connect(partial(self.checked, self.json, self.json_path))
        for value in tem:
            self.json.toggled.connect(partial(self.unchecked, self.json, value))

    def set_open_file_dialog(self, line, excutable=True):
        u"""
        设置打开文件的路径
        """

        if excutable:
            fileName, filetype = QFileDialog.getOpenFileName(
                self, "选取文件", "./", "All Files (*);;Executable Files (*.exe)"
            )
            self.__config__.update({"exe": fileName})
        else:
            fileName, filetype = QFileDialog.getOpenFileName(
                self, "选取文件", "./", "JSON Files(*.json);;All Files(*)"
            )
            self.__config__.update({
                "config": True, "config_path": fileName
            })
        
        self.save_config()
        line.setText(fileName)

    u"""运行kcptun"""
    def start_kcptun(self):
        u"""
        运行
        """
        cmds = [self.__config__['exe']]
        if self.__config__['config'] and self.__config__['config_path']:
            cmds.append("-c")
            cmds.append(self.__config__['config_path'])
        else:
            for key, value in self.extract_parameters().items():
                if value and value != "::":
                    cmds.append(key)
                    cmds.append(value)
        try:
            self.process.start(" ".join(cmds))
            self.command.setText(" ".join(cmds))
            self.start.setEnabled(False)
            self.stop.setEnabled(True)
            self.statusBar.showMessage("Kcptun started")
            self.save_config()
        except TypeError as e:
            self.output.setText("Error: %s" % e)
    
    def stop_kcptun(self):
        u"""
        停止
        """
        self.process.terminate()
        self.stop.setEnabled(False)
        self.start.setEnabled(True)
        self.statusBar.showMessage("Kcptun stoped")

    u"""将process的输出转向textEdit"""
    def append(self, text):
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)

    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput(), 'utf-8')
        self.append(text)

    def stderrReady(self):
        text = str(self.process.readAllStandardError(), 'utf-8')
        self.append(text)

    u"""提取各项参数"""
    def extract_parameters(self):
        u"""
        提取各项参数
        """
        parameters = {}

        for key, value in self.parameters.items():
            element = get_key_by_value(self.elements, value)

            if element and element.isChecked() or key in ("-l", "-r", "-p"):
                if isinstance(value, QLineEdit):
                    parameters.update({key: value.text()})
                elif isinstance(value, QComboBox):
                    parameters.update({key: value.currentText()})
        self.__config__.update({"paras": deepcopy(parameters)})
        local = parameters.pop("-l").lstrip(":")
        parameters.update({"-l": ":" + local})
        parameters.update({"-r": parameters.pop("-r") + ":" + parameters.pop("-p")})

        return parameters

    u"""保存配置"""
    def save_config(self):
        u"""
        保存config
        """
        with open(__config__, "w") as w:
            json.dump(self.__config__, w, indent=4)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
