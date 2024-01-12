import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QStandardItem, QStandardItemModel

class CheckableComboBoxDemo(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.combo_box = QComboBox()

        model = QStandardItemModel()

        item1 = QStandardItem("Option 1")
        item1.setCheckable(True)
        model.appendRow(item1)

        item2 = QStandardItem("Option 2")
        item2.setCheckable(True)
        model.appendRow(item2)

        item3 = QStandardItem("Option 3")
        item3.setCheckable(True)
        model.appendRow(item3)

        self.combo_box.setModel(model)

        layout.addWidget(self.combo_box)

        self.setLayout(layout)

        self.setWindowTitle("Checkable ComboBox Demo")
        self.setGeometry(300, 300, 300, 200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = CheckableComboBoxDemo()
    demo.show()
    sys.exit(app.exec_())
