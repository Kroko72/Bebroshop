import sys
import os
import sqlite3
import PIL.ImageOps
import time
from glitch_this import ImageGlitcher
from PIL import Image, ImageFilter
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import *


# Класс выбора эффекта
class ChooseEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.offset = False
        self.size = (1041, 591)  # Размер (в пикселях) окна, куда загружается фото

        # Загрузка дизайна
        uic.loadUi("with/ui/choose_effect.ui", self)

        # Удаление встроенного тайтл бара
        self.delete_title_bar()

        # Обработка изменений чекбоксов
        self.cb_anaglif.stateChanged.connect(self.enable_accept_button)
        self.cb_blur.stateChanged.connect(self.enable_accept_button)
        self.cb_black.stateChanged.connect(self.enable_accept_button)
        self.cb_contour.stateChanged.connect(self.enable_accept_button)
        self.cb_relief.stateChanged.connect(self.enable_accept_button)
        self.cb_flashback.stateChanged.connect(self.enable_accept_button)

        # Обработка нажатий кнопок
        self.btn_accept.clicked.connect(self.effect_done)
        self.close_button.clicked.connect(self.close_app)
        self.hide_button.clicked.connect(self.hide_app)
        self.btn_back.clicked.connect(self.go_back)
        self.btn_more.clicked.connect(self.more)

    # Ещё эффекты
    def more(self):
        # Создание предпросмотра фото
        glitcher = ImageGlitcher()
        im = Image.open("outfile.jpg")
        im_bit = PIL.ImageOps.posterize(im, 1)
        im_bit.save("temp_image7.jpg")
        im_grey = im.convert('L')
        im_grey.save("temp_image8.jpg")
        im_equalize = PIL.ImageOps.equalize(im, mask=None)
        im_equalize.save("temp_image9.jpg")
        im_solarize = PIL.ImageOps.solarize(im, 128)
        im_solarize.save("temp_image10.jpg")
        im_negative = PIL.ImageOps.invert(im)
        im_negative.save("temp_image11.jpg")
        im_glitch = glitcher.glitch_image(im, 5, color_offset=True)
        im_glitch.save("temp_image12.jpg")
        Choose_Window2.show_1.setPixmap(QPixmap("temp_image7.jpg"))
        Choose_Window2.show_2.setPixmap(QPixmap("temp_image8.jpg"))
        Choose_Window2.show_3.setPixmap(QPixmap("temp_image9.jpg"))
        Choose_Window2.show_4.setPixmap(QPixmap("temp_image10.jpg"))
        Choose_Window2.show_5.setPixmap(QPixmap("temp_image11.jpg"))
        Choose_Window2.show_6.setPixmap(QPixmap("temp_image12.jpg"))
        Choose_Window2.show()
        self.hide()

    # Удаление встроенного тайтл бара и белого заднего фона
    def delete_title_bar(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    # Функция возвращения назад
    def go_back(self):
        Main_Window.show()
        self.hide()

    # Делает кнопку применения кликабельной
    def enable_accept_button(self):
        self.btn_accept.setEnabled(True)

    # Добавление эффекта на картинку пользователя
    def effect_done(self):
        im = ""
        if self.cb_anaglif.isChecked():
            im = Image.open("temp_image1.jpg")
        if self.cb_contour.isChecked():
            im = Image.open("temp_image2.jpg")
        elif self.cb_black.isChecked():
            im = Image.open("temp_image3.jpg")
        elif self.cb_relief.isChecked():
            im = Image.open("temp_image4.jpg")
        elif self.cb_blur.isChecked():
            im = Image.open("temp_image5.jpg")
        elif self.cb_flashback.isChecked():
            im = Image.open("temp_image6.jpg")
        im.save("outfile.jpg")
        Main_Window.window.setPixmap(QPixmap("outfile.jpg"))
        Main_Window.show()
        self.hide()

    # Функция закрытия приложения
    def close_app(self):
        # Очистка временных файлов, если они есть
        try:
            os.remove("outfile.jpg")
            os.remove("temp_image1.jpg")
            os.remove("temp_image2.jpg")
            os.remove("temp_image3.jpg")
            os.remove("temp_image4.jpg")
            os.remove("temp_image5.jpg")
            os.remove("temp_image6.jpg")
            os.remove("temp_image7.jpg")
            os.remove("temp_image8.jpg")
            os.remove("temp_image9.jpg")
            os.remove("temp_image10.jpg")
            os.remove("temp_image11.jpg")
            os.remove("temp_image12.jpg")
            os.remove("temp_image13.jpg")
            os.remove("temp_image14.jpg")
            os.remove("temp_image15.jpg")
            os.remove("temp_gif1.gif")
        except FileNotFoundError:  # Если файл не существует или файл открыт
            pass
        except PermissionError:
            pass
        self.close()

    # Функция сворачивания приложения в трей
    def hide_app(self):
        self.showMinimized()

    # Обработка нажатия левой кнопки мыши
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    # Обработка перемещения мыши с зажатой левой кнопкой мыши
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    # Обработка окончания перемещения(отжатия левой кнопки мыши)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


# Класс основного окна
class MainWindow(ChooseEffect):
    def __init__(self):
        super().__init__()

        self.offset = False
        self.filename = ""

        # Загрузка дизайна
        uic.loadUi("with/ui/bebroshop.ui", self)

        # Обработка нажатий кнопок
        self.download_button.clicked.connect(self.load_file)
        self.close_button.clicked.connect(self.close_app)
        self.hide_button.clicked.connect(self.hide_app)
        self.effect_button.clicked.connect(self.choose_effect)
        self.save_button.clicked.connect(self.save)
        self.settings_button.clicked.connect(self.change_settings)

    # Функция изменения данных аккаунта
    def change_settings(self):
        settings.show()
        self.hide()

    # Функция загрузки картинки
    def load_file(self):
        try:
            self.filename = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            im = Image.open(self.filename)
            im = im.resize(self.size)
            im.save("outfile.jpg")
            self.window.setPixmap(QPixmap("outfile.jpg"))
            self.effect_button.setEnabled(True)
        except AttributeError:  # Если пользователь закрыл окно загрузки
            pass
        except OSError:  # Если фотография png меньшего размера
            im = Image.open(self.filename)
            rgb_im = im.convert('RGB')
            rgb_im.save("outfile.jpg")
            im = Image.open("outfile.jpg")
            im = im.resize(self.size)
            im.save("outfile.jpg")
            self.window.setPixmap(QPixmap("outfile.jpg"))
            self.effect_button.setEnabled(True)

    # Функция выбора эффекта, с созданием предпросмотра фото
    def choose_effect(self):
        im = ""
        try:
            im = Image.open("outfile.jpg")
            r, g, b = 0, 0, 0
            x, y = im.size
            res = Image.new('RGB', (x, y), (0, 0, 0))  # итоговое изображение в предпросмотре
            pixels2 = res.load()
            pixels = im.load()
            for i in range(x):
                for j in range(y):
                    if i < 30:
                        r, g, b = pixels[i, j]
                        pixels2[i, j] = 0, g, b
                    else:
                        pixels2[i, j] = r, g, b
                        g, b = pixels[i, j][1:]
                        r = pixels[i - 30, j][0]
            res.save("temp_image1.jpg")
        except TypeError:  # Если был применён серый фильтр
            pass

        im2 = im.filter(ImageFilter.CONTOUR)
        im2.save("temp_image2.jpg")

        im3 = im.filter(ImageFilter.FIND_EDGES)
        im3.save("temp_image3.jpg")

        im4 = im.filter(ImageFilter.EMBOSS)
        im4.save("temp_image4.jpg")

        im5 = im.filter(ImageFilter.GaussianBlur(radius=10))
        im5.save("temp_image5.jpg")

        try:
            flashback_image = Image.open("with/flashback.jpg")
            flashback_image = flashback_image.resize(self.size)
            im6 = Image.blend(im, flashback_image, alpha=0.5)
            im6.save("temp_image6.jpg")
        except ValueError:
            pass

        Choose_Window.show_1.setPixmap(QPixmap("temp_image1.jpg"))
        Choose_Window.show_2.setPixmap(QPixmap("temp_image2.jpg"))
        Choose_Window.show_3.setPixmap(QPixmap("temp_image3.jpg"))
        Choose_Window.show_4.setPixmap(QPixmap("temp_image4.jpg"))
        Choose_Window.show_5.setPixmap(QPixmap("temp_image5.jpg"))
        Choose_Window.show_6.setPixmap(QPixmap("temp_image6.jpg"))

        Choose_Window.show()
        self.hide()

    # Функция сохранения картинки
    def save(self):
        try:
            if Choose_Window3.gif is False:
                self.filename = QFileDialog.getSaveFileName(self, 'Сохранить картинку')[0]
                im = Image.open("outfile.jpg")
            else:
                self.filename = QFileDialog.getSaveFileName(self, 'Сохранить гифку')[0]
                im = Image.open("temp_gif1.gif")
            im.save(self.filename, format='GIF', save_all=True, duration=200, loop=0)
        except FileNotFoundError:
            pass
        except ValueError:
            pass


# Класс регистрации
class Registration(ChooseEffect):
    def __init__(self):
        super().__init__()
        self.usernames = list()

        # Загрузка дизайна
        uic.loadUi("with/ui/registration.ui", self)

        # Макса пароля (* вместо символов)
        self.le_password.setEchoMode(QLineEdit.Password)
        self.le_password2.setEchoMode(QLineEdit.Password)

        # Обработка нажатий кнопок и изменений чекбоксов
        self.btn_close.clicked.connect(self.close_app)
        self.btn_hide.clicked.connect(self.hide_app)
        self.btn_sign_in.clicked.connect(self.sign_in)
        self.cb_register.stateChanged.connect(self.not_registred)
        self.cb_guest.stateChanged.connect(self.guest)
        self.le_login.textChanged.connect(self.can_log)
        self.le_password.textChanged.connect(self.can_log)
        self.le_password2.textChanged.connect(self.can_log)

        # Удаление встроенного тайтл бара и скрытие не нужных изначально виджетов
        self.label_error.hide()
        self.le_password2.hide()

        # Ввод сохранённых данных
        self.write_remembered()

        # Получение списка юзернеймов зарегистрированных пользователей
        self.get_usernames()

    # Ввод сохранённых данных
    def write_remembered(self):
        with open("remembered.txt", "r") as file:
            # Если в файл не пустой, то заполняется логин и пароль
            try:
                temp_remembered = file.readline().split()
                self.le_login.setText(temp_remembered[0])
                self.le_password.setText(temp_remembered[1])
                self.btn_sign_in.setEnabled(True)
                self.cb_rem_pswrd.setChecked(True)
            except IndexError:
                pass

    # Запоминание логина и пароля
    def remember_password(self):
        with open("remembered.txt", "w") as file:
            file.write(self.le_login.text() + " " + self.le_password.text())

    # Проверка, что все данные для входа/регистрации введены
    def can_log(self):
        if self.le_password2.isHidden():
            if len(self.le_login.text()) != 0 and len(self.le_password.text()) != 0:
                self.btn_sign_in.setEnabled(True)
            else:
                self.btn_sign_in.setEnabled(False)
        elif self.le_password2.isHidden() is False:
            if len(self.le_password2.text()) != 0:
                if len(self.le_login.text()) != 0 and len(self.le_password.text()) != 0:
                    self.btn_sign_in.setEnabled(True)
                else:
                    self.btn_sign_in.setEnabled(False)
            else:
                self.btn_sign_in.setEnabled(False)
        else:
            self.btn_sign_in.setEnabled(False)

    # Получение юзернеймов зарегистрированных пользователей
    def get_usernames(self):
        con = sqlite3.connect("with/db/Usernames.db")
        cur = con.cursor()
        user_logins = cur.execute("""SELECT * FROM Usernames""").fetchall()
        for i in user_logins:
            self.usernames.append(i[0])
        con.close()

    # Вход как не зарегистрированный пользователь
    def not_registred(self):
        if self.btn_sign_in.isEnabled():
            self.btn_sign_in.setEnabled(False)
        if self.cb_guest.isChecked():
            self.cb_guest.setChecked(False)
        if self.cb_register.isChecked():
            self.le_password2.show()
        else:
            if len(self.le_password.text()) != 0 and len(self.le_login.text()) != 0:
                self.btn_sign_in.setEnabled(True)
            self.le_password2.hide()

    # Вход как гость
    def guest(self):
        if self.cb_guest.isChecked():
            self.cb_register.setChecked(False)
            self.cb_rem_pswrd.setChecked(False)
            self.btn_sign_in.setEnabled(True)
        else:
            self.btn_sign_in.setEnabled(False)

    # Создание лога
    def make_log(self):
        con = sqlite3.connect("with/db/Usernames.db")
        con.execute(f'INSERT INTO Logs(date, user) VALUES ("{time.asctime()}","{self.le_login.text()}")')
        con.commit()
        con.close()

    # Вход в приложение
    def sign_in(self):
        if self.cb_guest.isChecked():
            self.le_login.setText("-")
            self.hide()
            Main_Window.show()

        elif self.cb_register.isChecked():
            if self.le_login.text() not in self.usernames:
                temp_login = self.le_login.text()
                temp_password = self.le_password.text()
                temp_right_password = self.le_password2.text()
                if temp_password == temp_right_password:

                    # Добавление данных пользователя в БД
                    con = sqlite3.connect("with/db/Usernames.db")
                    con.execute(f'INSERT INTO Usernames(Login, Password) VALUES ("{temp_login}","{temp_password}")')
                    con.commit()
                    con.close()

                    if self.cb_rem_pswrd.isChecked():
                        self.remember_password()
                    else:
                        with open("remembered.txt", "w") as file:
                            file.truncate(0)
                    self.hide()
                    Main_Window.show()
                else:
                    self.label_error.setText("Пароли не совпадают")
                    self.label_error.show()
            else:
                self.label_error.setText("Имя уже используется")
                self.label_error.show()

        else:
            temp_login = self.le_login.text()
            temp_password = self.le_password.text()

            # Получение пароля пользователя
            con = sqlite3.connect("with/db/Usernames.db")
            temp_right_password = con.execute(f'SELECT Password from Usernames WHERE Login = "{temp_login}"').fetchall()
            con.close()

            if len(temp_right_password) != 0:
                if temp_password in temp_right_password[0]:
                    if self.cb_rem_pswrd.isChecked():
                        self.remember_password()
                    else:
                        with open("remembered.txt", "w") as file:
                            file.truncate(0)
                    self.hide()
                    Main_Window.show()
                else:
                    self.label_error.setText("Неверный логин или пароль")
                    self.label_error.show()
            else:
                self.label_error.setText("Неверный логин или пароль")
                self.label_error.show()

        self.make_log()


# Класс выбора эффекта 2
class ChooseEffect2(ChooseEffect):
    def __init__(self):
        super().__init__()

        # Загрузка дизайна
        uic.loadUi("with/ui/choose_effect2.ui", self)

        # Обработка изменений чекбоксов
        self.cb_grey.stateChanged.connect(self.enable_accept_button)
        self.cb_negative.stateChanged.connect(self.enable_accept_button)
        self.cb_bit.stateChanged.connect(self.enable_accept_button)
        self.cb_solarize.stateChanged.connect(self.enable_accept_button)
        self.cb_equalize.stateChanged.connect(self.enable_accept_button)
        self.cb_glitch.stateChanged.connect(self.enable_accept_button)

        # Обработка нажатий кнопок
        self.btn_accept.clicked.connect(self.effect_done)
        self.close_button.clicked.connect(self.close_app)
        self.hide_button.clicked.connect(self.hide_app)
        self.btn_back.clicked.connect(self.go_back)
        self.btn_more.clicked.connect(self.more)

    # Ещё эффекты
    def more(self):
        glitcher = ImageGlitcher()
        im = Image.open("outfile.jpg")
        im_mirror = PIL.ImageOps.mirror(im)
        im_mirror.save("temp_image13.jpg")
        im_glitch = glitcher.glitch_image(im, 4, color_offset=True, scan_lines=True)
        im_glitch.save("temp_image14.jpg")
        im_scan = glitcher.glitch_image(im, 1, color_offset=True, scan_lines=True)
        im_scan.save("temp_image15.jpg")
        gif = glitcher.glitch_image(im, 2, color_offset=True, gif=True)
        gif[0].save('temp_gif1.gif', format='GIF', append_images=gif[1:], save_all=True, duration=200, loop=0)
        self.movie1 = QMovie("temp_gif1.gif")
        Choose_Window3.show_1.setPixmap(QPixmap("temp_image13.jpg"))
        Choose_Window3.show_2.setPixmap(QPixmap("temp_image14.jpg"))
        Choose_Window3.show_4.setPixmap(QPixmap("temp_image15.jpg"))
        Choose_Window3.show_3.setMovie(self.movie1)
        self.movie1.start()
        Choose_Window3.show()
        self.hide()

    # Добавление эффекта на картинку пользователя
    def effect_done(self):
        im = ""
        if self.cb_bit.isChecked():
            im = Image.open("temp_image7.jpg")
        if self.cb_grey.isChecked():
            im = Image.open("temp_image8.jpg")
        elif self.cb_equalize.isChecked():
            im = Image.open("temp_image9.jpg")
        elif self.cb_solarize.isChecked():
            im = Image.open("temp_image10.jpg")
        elif self.cb_negative.isChecked():
            im = Image.open("temp_image11.jpg")
        elif self.cb_glitch.isChecked():
            im = Image.open("temp_image12.jpg")
        im.save("outfile.jpg")
        Main_Window.window.setPixmap(QPixmap("outfile.jpg"))
        Main_Window.show()
        self.hide()

    # Возвращение назад
    def go_back(self):
        Choose_Window.show()
        self.hide()


# Класс выбора эффекта 3
class ChooseEffect3(ChooseEffect):
    def __init__(self):
        super().__init__()
        self.gif = False

        # Загрузка дизайна
        uic.loadUi("with/ui/choose_effect3.ui", self)

        # Обработка изменений чекбоксов
        self.cb_mirror.stateChanged.connect(self.enable_accept_button)
        self.cb_scan_glitch.stateChanged.connect(self.enable_accept_button)
        self.cb_scan.stateChanged.connect(self.enable_accept_button)
        self.cb_glitch_gif.stateChanged.connect(self.enable_accept_button)

        # Обработка нажатий кнопок
        self.btn_accept.clicked.connect(self.effect_done)
        self.close_button.clicked.connect(self.close_app)
        self.hide_button.clicked.connect(self.hide_app)
        self.btn_back.clicked.connect(self.go_back)

    # Добавление эффекта на картинку пользователя
    def effect_done(self):
        im = ""
        Choose_Window2.movie1.stop()
        if self.cb_mirror.isChecked() or self.cb_scan_glitch.isChecked() or self.cb_scan.isChecked():
            if self.cb_mirror.isChecked():
                im = Image.open("temp_image13.jpg")
            elif self.cb_scan_glitch.isChecked():
                im = Image.open("temp_image14.jpg")
            elif self.cb_scan.isChecked():
                im = Image.open("temp_image15.jpg")
            im.save("outfile.jpg")
            Main_Window.window.setPixmap(QPixmap("outfile.jpg"))
        elif self.cb_glitch_gif.isChecked():  # Если пользователь выбрал гифку
            self.gif = True
            self.movie = QMovie("temp_gif1.gif")
            Main_Window.window.setMovie(self.movie)
            self.movie.start()
            Main_Window.effect_button.setEnabled(False)
        Main_Window.show()
        self.hide()

    # Возвращение назад
    def go_back(self):
        Choose_Window2.movie1.stop()
        Choose_Window2.show()
        self.hide()


# Класс изменения настроек аккаунта
class Settings(ChooseEffect):
    def __init__(self):
        super().__init__()
        self.new_password = ""
        self.new_login = ""
        self.login = Registration_Window.le_login.text()
        self.password = Registration_Window.le_password.text()

        # Загрузка дизайна
        uic.loadUi("with/ui/Settings.ui", self)

        # Обработка нажатий кнопок
        self.btn_change_login.clicked.connect(self.change_login)
        self.btn_change_password.clicked.connect(self.change_password)
        self.btn_go_back.clicked.connect(self.go_back)
        self.btn_close.clicked.connect(self.close_app)
        self.btn_hide.clicked.connect(self.hide_app)

    # Возвращение назад
    def go_back(self):
        Main_Window.show()
        self.hide()

    # Функция изменения пароля
    def change_password(self):
        text, ok = QInputDialog.getText(self, 'Изменить пароль', 'Введите пароль:')
        if ok:
            self.new_password = str(text)
        if len(self.new_password) > 0:
            con = sqlite3.connect("with/db/Usernames.db")
            cur = con.cursor()
            cur.execute("UPDATE Usernames SET Password = (?) WHERE Login = (?)", (self.new_password, self.login))
            con.commit()
            con.close()
        else:
            self.error_label.setText("Пустой пароль")

    # Функция изменения логина
    def change_login(self):
        text, ok = QInputDialog.getText(self, 'Изменить логин', 'Введите логин:')
        if ok:
            self.new_login = str(text)
        if len(self.new_login) > 0:
            con = sqlite3.connect("with/db/Usernames.db")
            cur = con.cursor()
            cur.execute("UPDATE Usernames SET Login = (?) WHERE Password = (?)", (self.new_login, self.password))
            con.commit()
            con.close()
        else:
            self.error_label.setText("Пустой логин")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main_Window = MainWindow()
    Choose_Window = ChooseEffect()
    Registration_Window = Registration()
    Choose_Window2 = ChooseEffect2()
    Choose_Window3 = ChooseEffect3()
    settings = Settings()
    Registration_Window.show()
    sys.exit(app.exec_())
