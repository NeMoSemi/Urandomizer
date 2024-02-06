from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt
import sys


class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            print(item.text() + " was unselected.")
        else:
            item.setCheckState(Qt.Checked)
            print(item.text() + " was selected.")
        self.check_items()

    def item_checked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == Qt.Checked

    def check_items(self):
        checkedItems = []
        for i in range(self.count()):
            if self.item_checked(i):
                checkedItems.append(self.model().item(i, 0).text())
        print(checkedItems)


class Dialog_01(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # myQWidget = QWidget()#
        # myBoxLayout = QVBoxLayout()#
        # myQWidget.setLayout(myBoxLayout)#
        # self.setCentralWidget(myQWidget)#
        self.ComboBox = CheckableComboBox()
        self.ComboBox.setGeometry(0, 0, 300, 100)
        for i in range(3):
            self.ComboBox.addItem("Combobox Item " + str(i))
            item = self.ComboBox.model().item(i, 0)
            item.setCheckState(Qt.Unchecked)
        # myBoxLayout.addWidget(self.ComboBox)#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480, 320)
    sys.exit(app.exec_())

#python -m PyQt5.uic.pyuic -x C:\Users\user\PycharmProjects\Urandomizer\data\ui\main.ui -o C:\Users\user\PycharmProjects\Urandomizer\main_window.py