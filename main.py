import json
import re
import sys, os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from main_window import *
import random



class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
        # super().__init__()
        # uic.loadUi('data/ui/test_fielder.ui', self)
        self.files = {'даты': 'data/json/dates.json', 'определения': 'data/json/definitions.json',
                      'имена': 'data/json/names.json'}
        self.box_list = [['data/json/dates.json', self.date_box_tool_menu, self.date_box, 'Д'],
                         ['data/json/definitions.json', self.definition_box_tool_menu, self.definition_box, 'О'],
                         ['data/json/names.json', self.name_box_tool_menu, self.name_box, 'И']]

        self.number_b.clicked.connect(self.number_window)
        self.back_b.clicked.connect(self.back)
        self.get_number_b.clicked.connect(self.get_number)

        self.text_b.clicked.connect(self.answer_ddn)
        self.klass_box.activated.connect(self.chage_klass)
        self.select_b.clicked.connect(self.select_text)

        self.pictures_b.clicked.connect(self.answer_pictures)
        self.select_map_b.clicked.connect(self.select_map)
        self.select_portrait_b.clicked.connect(self.select_portrait)
        self.select_monument_b.clicked.connect(self.select_monument)
        self.portrait_klass_box.activated.connect(self.chage_portrait_klass)

        self.add_window_b.clicked.connect(self.add_window)
        self.minus_b.clicked.connect(self.minus_theme_b)
        self.plus_b.clicked.connect(self.plus_theme_b)
        self.save_b.clicked.connect(self.save_submit)
        self.type_box.activated.connect(self.type_edit)
        self.klass_box_edit.activated.connect(self.chage_klass_edit)
        self.theme_box_edit.activated.connect(self.theme_change_edit)

        self.digits_window = [self.digits_label, self.spinbox, self.back_b, self.get_number_b, self.random_number]
        self.answer_text = [self.count_d, self.klass_box, self.klass_label, self.text_field, self.definition_box,
                            self.back_b, self.select_b, self.date_box, self.date_label, self.definition_label,
                            self.name_box, self.name_label, self.type_random_check_box]
        self.answer_pictures = [self.back_b, self.pictures_label, self.portrait_label, self.map_label,
                                self.portrait_klass_label, self.map_klass_label, self.portrait_klass_box,
                                self.map_klass_box, self.portrait_theme_label, self.portrait_theme_box,
                                self.select_portrait_b, self.select_map_b, self.count_portrain, self.monument_label,
                                self.monument_klass_label, self.monument_klass_box, self.select_monument_b]
        self.add = [self.klass_box_edit, self.klass_label_edit, self.main_text_edit, self.minus_b, self.plus_b,
                    self.save_b, self.theme_box_edit, self.theme_edit, self.theme_label_edit,
                    self.type_label, self.type_box, self.back_b]
        for i in self.digits_window + self.answer_text + self.add + self.answer_pictures: i.hide()
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
        for i in self.digits_window + self.answer_text + self.add + self.answer_pictures: i.hide()

    def answer_ddn(self):
        self.text_field.clear()
        # self.theme_box_tool_menu.clear()
        for i in self.answer_text: i.show()
        for i in reversed(range(self.Main_layout.count())):
            self.Main_layout.itemAt(i).widget().hide()
        self.add_window_b.hide()
        for type in self.box_list:
            type[1].clear()
            with open(type[0], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                first_theme = True
                self.klass_box.clear()
                for keys in text:
                    self.klass_box.addItem(keys)
                    if first_theme:
                        if len(text[keys]) != 0:
                            font = type[1].font()
                            font.setPointSize(30)
                            type[1].setFont(font)
                            for theme in text[keys]:
                                action = type[1].addAction(theme)
                                action.setFont(font)
                                action.setCheckable(True)
                                #self.theme_box.addItem(theme)
                            type[2].setMenu(type[1])
                            type[2].setPopupMode(QtWidgets.QToolButton.InstantPopup)
                        first_theme = False

    def answer_pictures(self):
        for i in self.answer_pictures: i.show()
        for i in reversed(range(self.Main_layout.count())):
            self.Main_layout.itemAt(i).widget().hide()
        self.map_klass_box.clear()
        self.portrait_klass_box.clear()
        self.portrait_theme_box_tool_menu.clear()
        self.add_window_b.hide()
        self.map_classes_list = sorted([int(i) for i in os.listdir('data/pictures/maps')], reverse=True)
        for klass in self.map_classes_list: self.map_klass_box.addItem(str(klass))
        self.monument_classes_list = sorted([int(i) for i in os.listdir('data/pictures/monuments')], reverse=True)
        for klass in self.monument_classes_list: self.monument_klass_box.addItem(str(klass))
        self.portrait_classes_list = sorted([int(i) for i in os.listdir('data/pictures/personality')], reverse=True)
        for klass in self.portrait_classes_list: self.portrait_klass_box.addItem(str(klass))
        self.portrait_theme_list = os.listdir(f'data/pictures/personality/{self.portrait_klass_box.currentText()}')
        if len(self.portrait_theme_list) != 0:
            font = self.portrait_theme_box_tool_menu.font()
            font.setPointSize(30)
            self.portrait_theme_box_tool_menu.setFont(font)
            for theme in self.portrait_theme_list:
                action =  self.portrait_theme_box_tool_menu.addAction(theme)
                action.setFont(font)
                action.setCheckable(True)
            self.portrait_theme_box.setMenu(self.portrait_theme_box_tool_menu)
            self.portrait_theme_box.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def chage_portrait_klass(self):
        self.portrait_theme_box_tool_menu.clear()
        self.portrait_theme_list = os.listdir(f'data/pictures/personality/{self.portrait_klass_box.currentText()}')
        if len(self.portrait_theme_list) != 0:
            font = self.portrait_theme_box_tool_menu.font()
            font.setPointSize(30)
            self.portrait_theme_box_tool_menu.setFont(font)
            for theme in self.portrait_theme_list:
                action =  self.portrait_theme_box_tool_menu.addAction(theme)
                action.setFont(font)
                action.setCheckable(True)
            self.portrait_theme_box.setMenu(self.portrait_theme_box_tool_menu)
            self.portrait_theme_box.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def select_portrait(self):
        portrait_theme_list = []
        for theme in self.portrait_theme_box_tool_menu.actions():
            if theme.isChecked():
                portrait_theme_list.append(theme.text())
        if len(portrait_theme_list) != 0:
            portrait_list = []
            for portrait in portrait_theme_list:
                portrait_list += [fr'{portrait}\{i}' for i in os.listdir(f'data/pictures/personality/{self.portrait_klass_box.currentText()}/{portrait}')]
            if int(self.count_portrain.value()) > len(portrait_list):
                for portrait_path in portrait_list:
                    os.startfile(fr'data\pictures\personality\{self.portrait_klass_box.currentText()}\{portrait_path}')
            else:
                for portrait_path in random.sample(portrait_list, int(self.count_portrain.value())):
                    os.startfile(fr'data\pictures\personality\{self.portrait_klass_box.currentText()}\{portrait_path}')

    def select_map(self):
        if len(self.map_klass_box.currentText()) != 0:
            map_list = os.listdir(f'data/pictures/maps/{self.map_klass_box.currentText()}')
            if len(map_list) != 0:
                os.startfile(fr'data\pictures\maps\{self.map_klass_box.currentText()}\{random.choice(map_list)}')

    def select_monument(self):
        if len(self.map_klass_box.currentText()) != 0:
            monument_list = os.listdir(f'data/pictures/monuments/{self.monument_klass_box.currentText()}')
            if len(monument_list) != 0:
                os.startfile(fr'data\pictures\monuments\{self.monument_klass_box.currentText()}\{random.choice(monument_list)}')

    def get_number(self):
        self.random_number.setText(str(random.randint(1, self.spinbox.value())))

    def select_text(self):
        answer_text_dict = {'Д': [], 'О': [], 'И': []}
        answer_text_list = []
        for type in self.box_list:
            theme_list = []
            for theme in type[1].actions():
                if theme.isChecked():
                    theme_list.append(theme.text())
            with open(type[0], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                for theme in theme_list:
                    answer_text_dict[type[3]] += text[self.klass_box.currentText()][theme]
        if len(self.klass_box.currentText()) != 0 and sum([len(value) for value in answer_text_dict.values()]) > 0:
            self.text_field.clear()
            if self.type_random_check_box.isChecked():
                not_zero_item = sum([1 for value in answer_text_dict.values() if len(value) != 0])
                count_list = []
                for i in range(not_zero_item):
                    if i != not_zero_item - 1:
                        count_list.append((self.count_d.value() + 1)// not_zero_item)
                    else:
                        count_list.append(self.count_d.value() - ((self.count_d.value() + 1) // not_zero_item) * (not_zero_item - 1))
                if count_list[-1] == 0: count_list.remove(0)
                counter = 0
                pop_dict_list = []
                for key in answer_text_dict:
                    if len(answer_text_dict[key]) == 0:
                        pop_dict_list.append(key)
                for key in pop_dict_list:
                    del answer_text_dict[key]
                for key in answer_text_dict:
                    if len(answer_text_dict[key]) < count_list[counter]:
                        [answer_text_list.append(f'({key}){i}') for i in answer_text_dict[key]]
                        if counter != not_zero_item - 1:
                            count_list[counter + 1] += count_list[counter] - len(answer_text_dict[key])
                    else:
                        [answer_text_list.append(f'({key}){i}') for i in random.sample(answer_text_dict[key], count_list[counter])]
                    counter += 1
            else:
                vr_sp = []
                for key in answer_text_dict:
                    for value in answer_text_dict[key]:
                        vr_sp.append(f'({key}){value}')
                if len(vr_sp) >= self.count_d.value():
                    answer_text_list = random.sample(vr_sp, int(self.count_d.value()))
                else:
                    answer_text_list = vr_sp.copy()
            count = 1
            for item in answer_text_list:
                self.text_field.append(f'{str(count)}.{item}')
                count += 1

    def chage_klass(self):
        for type in self.box_list:
            type[1].clear()
            with open(type[0], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                type[1].clear()
                font = type[1].font()
                font.setPointSize(30)
                type[1].setFont(font)
                for theme in text[str(self.klass_box.currentText())]:
                    action = type[1].addAction(theme)
                    action.setFont(font)
                    action.setCheckable(True)
                    # self.theme_box.addItem(theme)
                type[2].setMenu(type[1])
                type[2].setPopupMode(QtWidgets.QToolButton.InstantPopup)

    def type_edit(self):
        self.theme_box_edit.clear()
        self.klass_box_edit.clear()
        self.main_text_edit.clear()
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            first_theme = True
            for keys in text:
                self.klass_box_edit.addItem(keys)
                if first_theme:
                    if len(text[keys]) != 0:
                        for theme in text[keys]:
                            self.theme_box_edit.addItem(theme)
                        #####################
                        #self.theme_change_edit()
                        self.theme_edit.setText(self.theme_box_edit.currentText())
                        ##################self.current_theme = self.theme_box_edit.currentText()
                        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
                            text = json.load(file)
                            self.main_text_edit.clear()
                            for obj in text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]:
                                self.main_text_edit.append(f'{obj}')
                        ########################
                    first_theme = False
            # self.current_type = self.type_box.currentText().lower()
            # self.current_theme = self.theme_box_edit.currentText()
            # self.current_klass = self.klass_box_edit.currentText()

    def chage_klass_edit(self):
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            #
            self.theme_box_edit.clear()
            for theme in text[str(self.klass_box_edit.currentText())]:
                self.theme_box_edit.addItem(theme)
            self.theme_edit.setText(self.theme_box_edit.currentText())
            #
            self.main_text_edit.clear()
            if len(text[self.klass_box_edit.currentText()]) > 0:
                for obj in text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]:
                    self.main_text_edit.append(f'{obj}')
            # self.current_theme = self.theme_box_edit.currentText()
            # self.current_klass = self.klass_box_edit.currentText()


    def theme_change_edit(self):
        self.theme_edit.setText(self.theme_box_edit.currentText())
        # self.current_theme = self.theme_box_edit.currentText()
        with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
            text = json.load(file)
            self.main_text_edit.clear()
            for obj in text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]:
                self.main_text_edit.append(f'{obj}')

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
                    if len(text[keys]) != 0:
                        for theme in text[keys]:
                            self.theme_box_edit.addItem(theme)
                        self.theme_edit.setText(self.theme_box_edit.currentText())
                        for obj in text[keys][self.theme_box_edit.currentText()]:
                            self.main_text_edit.append(f'{obj}')
                    first_theme = False
            # self.current_theme = self.theme_box_edit.currentText()
            # self.current_klass = self.klass_box_edit.currentText()
            # self.current_type = self.type_box.currentText().lower()

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
        theme = self.theme_box_edit.currentText()
        self.submit(f'Удалить тему {theme}?', 'Удалённые данные будет невозможно восстановить',
                    f'{theme} -> Delite', self.delite_theme)

    def delite_theme(self, btn):
        if btn.text().lower() == 'ok':
            with open(self.files[self.type_box.currentText().lower()], mode="r", encoding="utf-8") as file:
                text = json.load(file)
                del text[self.klass_box_edit.currentText()][self.theme_box_edit.currentText()]
                self.theme_box_edit.clear()
                for theme in text[self.klass_box_edit.currentText()]:
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
                # if self.theme_edit.text() != self.current_theme:
                    # print(self.theme_edit.text(), self.current_theme)
                    # text[self.current_klass][self.theme_edit.text()] = text[self.current_klass][self.current_theme]
                    # del text[self.current_klass][self.current_theme]
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
