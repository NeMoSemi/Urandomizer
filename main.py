import json
import re
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from main_window import *
import random



class MyWidget(QMainWindow, Ui_Urandomizer):
    def __init__(self):
        super(MyWidget, self).__init__()
        #self.ui = Ui_Urandomizer()
        self.setupUi(self)
        #super().__init__()
        #uic.loadUi('data/ui/main.ui', self)
        self.files = {'даты': 'data/json/dates.json', 'определения': 'data/json/definitions.json',
                      'имена': 'data/json/names.json'}
        self.state = None
        self.current_klass = None
        self.current_theme = None
        self.current_type = None


        self.number_b.clicked.connect(self.number_window)
        self.dates_b.clicked.connect(self.answer)
        self.definitions_b.clicked.connect(self.answer)
        self.names_b.clicked.connect(self.answer)
        self.back_b.clicked.connect(self.back)
        self.get_number_b.clicked.connect(self.get_number)
        self.select_b.clicked.connect(self.select)
        self.add_window_b.clicked.connect(self.add_window)
        self.minus_b.clicked.connect(self.minus_theme_b)
        self.plus_b.clicked.connect(self.plus_theme_b)
        self.save_b.clicked.connect(self.save_submit)
        self.klass_box.activated.connect(self.chage_klass)
        self.type_box.activated.connect(self.type_edit)
        self.klass_box_edit.activated.connect(self.chage_klass_edit)
        self.theme_box_edit.activated.connect(self.theme_change_edit)
        self.digits_window = [self.digits_label, self.spinbox, self.back_b, self.get_number_b, self.random_number]
        self.answer = [self.count_d, self.count_l, self.form_answer, self.klass_box, self.klass_label,
                       self.text_field, self.theme_box, self.theme_label, self.back_b, self.select_b]
        self.add = [self.klass_box_edit, self.klass_label_edit, self.main_text_edit, self.minus_b, self.plus_b,
                    self.save_b, self.theme_box_edit, self.theme_edit, self.theme_label_edit,
                    self.type_label, self.type_box, self.back_b]
        for i in self.digits_window + self.answer + self.add: i.hide()
        #self.ColumnNumber.setText(str(1))
        #self.noteEdit.setReadOnly(True)

    def number_window(self):
        for i in self.digits_window: i.show()
        for i in reversed(range(self.Main_layout.count())):
            self.Main_layout.itemAt(i).widget().hide()
        self.add_window_b.hide()
        self.spinbox.cleanText()
        self.random_number.setText('0')

    def back(self):
        for i in reversed(range(self.Main_layout.count())):
            self.Main_layout.itemAt(i).widget().show()
        self.add_window_b.show()
        for i in self.digits_window + self.answer + self.add: i.hide()

    def answer(self):
        self.form_answer.setText(self.sender().text())
        self.state = self.files[self.sender().text().lower()]
        self.text_field.clear()
        self.theme_box_tool_menu.clear()
        self.klass_box.clear()
        for i in self.answer: i.show()
        for i in reversed(range(self.Main_layout.count())):
            self.Main_layout.itemAt(i).widget().hide()
        self.add_window_b.hide()
        with open(self.state, mode="r", encoding="utf-8") as file:
            text = json.load(file)
            first_theme = True
            for keys in text:
                self.klass_box.addItem(keys)
                if first_theme:
                    font = self.theme_box_tool_menu.font()
                    font.setPointSize(30)
                    self.theme_box_tool_menu.setFont(font)
                    for theme in text[keys]:
                        action = self.theme_box_tool_menu.addAction(theme)
                        action.setFont(font)
                        action.setCheckable(True)
                        #self.theme_box.addItem(theme)
                    self.theme_box.setMenu(self.theme_box_tool_menu)
                    self.theme_box.setPopupMode(QtWidgets.QToolButton.InstantPopup)
                    first_theme = False

    def get_number(self):
        self.random_number.setText(str(random.randint(1, self.spinbox.value())))

    def select(self):
        sp = []
        for i in self.theme_box_tool_menu.actions():
            if i.isChecked(): sp.append(i.text())
        if len(self.klass_box.currentText()) != 0 and len(sp) != 0:
            self.text_field.clear()
            with open(self.state, mode="r", encoding="utf-8") as file:
                text = json.load(file)
                items = []
                for i in sp:
                    items += text[self.klass_box.currentText()][i]
                count = 1
                count_questions = self.count_d.value()
                if self.count_d.value() > len(items):
                    count_questions = len(items)
                for obj in random.sample(items, count_questions):
                    self.text_field.append(f'{str(count)}.{obj}')
                    count += 1

    def chage_klass(self):
        with open(self.state, mode="r", encoding="utf-8") as file:
            text = json.load(file)
            self.theme_box_tool_menu.clear()
            font = self.theme_box_tool_menu.font()
            font.setPointSize(30)
            self.theme_box_tool_menu.setFont(font)
            for theme in text[str(self.klass_box.currentText())]:
                action = self.theme_box_tool_menu.addAction(theme)
                action.setFont(font)
                action.setCheckable(True)
                # self.theme_box.addItem(theme)
            self.theme_box.setMenu(self.theme_box_tool_menu)
            self.theme_box.setPopupMode(QtWidgets.QToolButton.InstantPopup)
            #self.theme_box.addItem(theme)
            #if text[str(self.klass_box.currentText())] == {}:
            #    self.theme_box.clear()

    def type_edit(self):
        self.submit('Сохранить изменения?', 'Поле "Тема" было изменено',
                    f'{self.current_theme} -> {self.theme_edit.text()}', self.different_themes,
                    self.theme_edit.text() != self.current_theme)
        self.theme_box_edit.clear()
        self.klass_box_edit.clear()
        self.main_text_edit.clear()
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            first_theme = True
            for keys in text:
                self.klass_box_edit.addItem(keys)
                if first_theme:
                    for theme in text[keys]:
                        self.theme_box_edit.addItem(theme)
                    first_theme = False
                    #####################
                    #self.theme_change_edit()
                    self.theme_edit.setText(self.theme_box_edit.currentText())
                    self.current_theme = self.theme_box_edit.currentText()
                    with open(self.files[self.current_type.lower()], mode="r", encoding="utf-8") as file:
                        text = json.load(file)
                        self.main_text_edit.clear()
                        for obj in text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]:
                            self.main_text_edit.append(f'{obj}')
                    ########################
            self.current_type = self.type_box.currentText().lower()
            self.current_theme = self.theme_box_edit.currentText()
            self.current_klass = self.klass_box_edit.currentText()

    def chage_klass_edit(self):
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            #
            self.submit('Сохранить изменения?', 'Поле "Тема" было изменено',
                        f'{self.current_theme} -> {self.theme_edit.text()}', self.different_themes,
                        self.theme_edit.text() != self.current_theme)
            self.theme_box_edit.clear()
            for theme in text[str(self.klass_box_edit.currentText())]:
                self.theme_box_edit.addItem(theme)
            self.theme_edit.setText(self.theme_box_edit.currentText())
            #
            self.main_text_edit.clear()
            if len(text[self.klass_box_edit.currentText()]) > 0:
                for obj in text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]:
                    self.main_text_edit.append(f'{obj}')
            self.current_theme = self.theme_box_edit.currentText()
            self.current_klass = self.klass_box_edit.currentText()


    def theme_change_edit(self):
        self.submit('Сохранить изменения?', 'Поле "Тема" было изменено',
                    f'{self.current_theme} -> {self.theme_edit.text()}', self.different_themes,
                    self.theme_edit.text() != self.current_theme)
        self.theme_edit.setText(self.theme_box_edit.currentText())
        self.current_theme = self.theme_box_edit.currentText()
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            self.main_text_edit.clear()
            for obj in text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]:
                self.main_text_edit.append(f'{obj}')

    def different_themes(self, btn):
        if btn.text().lower() == 'ok':
            with open(self.files[self.current_type.lower()], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                text[self.current_klass][self.theme_edit.text()] = text[self.current_klass][self.current_theme]
                del text[self.current_klass][self.current_theme]
                self.theme_box_edit.clear()
                for theme in text[self.current_klass]:
                    self.theme_box_edit.addItem(theme)
                self.theme_edit.setText(self.theme_box_edit.currentText())
                with open(self.files[self.current_type.lower()], mode="w", encoding="utf-8") as f:
                    json.dump(text, f, indent=4, ensure_ascii=False)

    def add_window(self):
        for i in self.add: i.show()
        for i in reversed(range(self.Main_layout.count())):
            self.Main_layout.itemAt(i).widget().hide()
        self.add_window_b.hide()
        self.theme_box_edit.clear()
        self.klass_box_edit.clear()
        self.main_text_edit.clear()
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            first_theme = True
            for keys in text:
                self.klass_box_edit.addItem(keys)
                if first_theme:
                    for theme in text[keys]:
                        self.theme_box_edit.addItem(theme)
                    self.theme_edit.setText(self.theme_box_edit.currentText())
                    first_theme = False
                    for obj in text[keys][self.theme_box_edit.currentText()]:
                        self.main_text_edit.append(f'{obj}')
            self.current_theme = self.theme_box_edit.currentText()
            self.current_klass = self.klass_box_edit.currentText()
            self.current_type = self.type_box.currentText().lower()

    def submit(self, text, info, details, func, condition=True):
        if condition:
            submit = QMessageBox()
            submit.setWindowTitle('Подтжерждение')
            submit.setText(text)
            submit.setIcon(QMessageBox.Information)
            submit.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            submit.setDefaultButton(QMessageBox.Ok)
            submit.setInformativeText(info)
            submit.setDetailedText('Детали')
            submit.setDetailedText(details)
            submit.buttonClicked.connect(func)


            submit.exec_()

    def minus_theme_b(self):
        self.submit(f'Удалить тему {self.current_theme}?', 'Удалённые данные будет невозможно восстановить',
                    f'{self.current_theme} -> Delite', self.delite_theme)

    def delite_theme(self, btn):
        if btn.text().lower() == 'ok':
            with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                del text[self.current_klass][self.current_theme]
                self.theme_box_edit.clear()
                for theme in text[self.current_klass]:
                    self.theme_box_edit.addItem(theme)
                self.theme_edit.setText(self.theme_box_edit.currentText())
                with open(self.files[self.type_box.currentText().lower()], mode="w", encoding="utf-8") as f:
                    json.dump(text, f, indent=4, ensure_ascii=False)
            self.back()

    def plus_theme_b(self):
        theme_name, ok_pressed = QInputDialog.getText(self, "Добавить тему", "Введите название темы:")
        if ok_pressed:
            with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                if theme_name in text[self.klass_box_edit.currentText()]:
                    submit = QMessageBox()
                    submit.setWindowTitle('Ошибка')
                    submit.setText('Такая тема уже существует!')
                    submit.setIcon(QMessageBox.Information)
                    submit.setStandardButtons(QMessageBox.Ok)
                    submit.setDefaultButton(QMessageBox.Ok)
                    submit.setInformativeText('Выберите другое не занятое название')
                    submit.setDetailedText('Детали')
                    submit.setDetailedText(f'{theme_name} -> already exists')

                    submit.exec_()
                else:
                    text[self.klass_box_edit.currentText()][theme_name] = []
                    with open(self.files[self.type_box.currentText().lower()], mode="w", encoding="utf-8") as f:
                        json.dump(text, f, indent=4, ensure_ascii=False)
                    self.theme_box_edit.clear()
                    for theme in text[self.klass_box_edit.currentText()]:
                        self.theme_box_edit.addItem(theme)
                    self.theme_edit.setText(self.theme_box_edit.currentText())

    def save_submit(self):
        self.submit('Сохранить изменения?', 'Текущие изменения будут сохранены', 'items -> update', self.save_text)

    def save_text(self, btn):
        if btn.text().lower() == 'ok':
            themes = self.main_text_edit.toPlainText().split('\n')
            del_elements = []
            for i in themes:
                if re.sub('\s+', '', i.strip()) == '': del_elements.append(i)
            for i in del_elements:
                themes.remove(i)
            with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                #
                if self.theme_edit.text() != self.current_theme:
                    print(self.theme_edit.text(), self.current_theme)
                    text[self.current_klass][self.theme_edit.text()] = text[self.current_klass][self.current_theme]
                    del text[self.current_klass][self.current_theme]
                #
                text[self.klass_box_edit.currentText()][self.theme_edit.text()] = themes
                with open(self.files[self.type_box.currentText().lower()], mode="w", encoding="utf-8") as f:
                    json.dump(text, f, indent=4, ensure_ascii=False)
            self.back()


#pyinstaller.exe --onefile --windowed main.py
if __name__ == "__main__":
    apps = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(apps.exec_())
