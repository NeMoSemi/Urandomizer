from PyQt5 import QtWidgets, QtGui, QtCore


class Dialog_01(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolbutton = QtWidgets.QToolButton(self)
        self.toolbutton.setText('Categories ')
        self.toolmenu = QtWidgets.QMenu(self)
        for i in range(3):
            action = self.toolmenu.addAction('Category %s' % i)
            action.setCheckable(True)
        self.toolbutton.setMenu(self.toolmenu)
        self.toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)



if __name__ == '__main__':
    app = QtWidgets.QApplication(['Test'])
    dialog_1 = Dialog_01()
    dialog_1.show()
    app.exec_()

