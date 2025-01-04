from PIL import Image, ImageFilter, ImageEnhance
from PyQt6 import QtWidgets, uic

import sys
import os
import tempfile

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from qt_material import apply_stylesheet


#with Image.open("jonatan-pie-_b2hvhIXGI8-unsplash.jpg") as img:
    #print("Розмір:", img.size)
    #print("Формат:", img.format)
    #print("Тип:", img.mode)
    #black_img = img.convert("L") 
    #black_img.show()

    #blur_image = img.filter(ImageFilter.BLUR)
    #name = img.filename.split(".")[0]
    #blur_image.save(name + "blur.jpg")
    
    #rotate_img = img.transpose(Image.ROTATE_90)
    #rotate_img.save(name + "rotate.jpg")

    #sharpen_img = img.filter(ImageFilter.SHARPEN)
    #sharpen_img.save(name + "sharpen.jpg")

    #bright_obj = ImageEnhance.Brightness(img)
    #bright_img = bright_obj.enhance(1.5)
    #bright_img.save(name + "bright_img.jpg")
    #bright_img.show()

    #contraster = ImageEnhance.Contrast(img)
    #contraster_img = contraster.enhance(2)
    #contraster_img.save(name + "contraster_img.jpg")
    #contraster_img.show()

    #color_img = ImageEnhance.Color(img)enhance(2)
    #color_img.save(name + "color_img.jpg")
    #color_img.show()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('window.ui', self)

class ImageEditor():
    def __init__(self,):
        self.original = None
        self.image = None
        self.history = []
        self.history_index = -1
        self.image_path = None
        self.workdir = None
        self.temp_folder = tempfile.TemporaryDirectory()
        self.ui = Ui()
        self.connects()
        self.ui.show()

    def connects(self):
        self.ui.folder_btn.clicked.connect(self.open_folder) #Підключення кнопок до функції
        self.ui.open_folder.triggered.connect(self.open_folder)
        self.ui.open_file.triggered.connect(self.open_file)
        self.ui.image_list.currentRowChanged.connect(self.choose_image)
        self.ui.save_btn.clicked.connect(self.save_file)
        self.ui.save.triggered.connect(self.save_file)
        self.ui.back_btn.clicked.connect(self.back)
        self.ui.forward_btn.clicked.connect(self.forward)
        self.ui.reset.triggered.connect(self.reset)
        #self.ui.back.triggered.connect(self.back)
        self.ui.del_btn.clicked.connect(self.delete_file)


        self.ui.black_white.triggered.connect(self.do_black_white)
        self.ui.blur.triggered.connect(self.do_blur)
        self.ui.rotate_left.clicked.connect(self.do_rotate_left)
        self.ui.rotate_right.clicked.connect(self.do_rotate_right)
        self.ui.sharpen.triggered.connect(self.do_sharpen)
        self.ui.bright.triggered.connect(self.do_bright)
        self.ui.contrast.triggered.connect(self.do_contrast)
        self.ui.saturation.triggered.connect(self.do_saturation)





    def get_images(self):
        self.folder_images = []
        if self.workdir: #Перевірка чи є файл
            filenames = os.listdir(self.workdir) #Отрмання файлів
            for file in filenames:
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    self.folder_images.append(file)


    def open_folder(self):
        self.workdir = QFileDialog.getExistingDirectory() #Відкриття папки
        if self.workdir:
            self.get_images()
            self.ui.image_list.clear()
            self.ui.image_list.addItems(self.folder_images) #Додавання картинки в список файлів 

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "Виберіть фото", "", "Зображення (*.png *.jpg *.jpeg)") #Відкриття файлу
        if file_path:
            self.open(file_path)
            self.show_image(file_path)

    def open(self, filename):
        self.image = Image.open(filename)
        self.original = self.image.copy()
        self.history = [self.image.copy()]
        self.histoty_index = 0
        self.image_path = filename

    def choose_image(self):
        if self.ui.image_list.currentRow()>=0:
            title = self.ui.image_list.currentItem().text()
            image_path = os.path.join(self.workdir, title)
            self.open(image_path)
            self.show_image(image_path)

    def show_image(self, image_path):
        self.ui.current_image.hide()
        w, h = self.ui.current_image.width(), self.ui.current_image.height()
        pixmap = QPixmap(image_path).scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.current_image.setPixmap(pixmap)
        self.ui.current_image.show()

    def back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index]
            self.show_image(self.temp_save())
    
    def forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.image = self.history[self.history_index]
            self.show_image(self.temp_save())

    def add_to_history(self):
        self.history.append(self.image.copy())
        self.history_index += 1    

    def temp_save(self):
        temp_path = os.path.join(self.temp_folder.name, f"temp_image_{self.history_index}.png")
        self.image.save(temp_path)
        return temp_path

    def reset(self):
        if self.image:
            self.image = self.original
            self.history_index = 0
            self.show_image(self.temp_save())

    def save_file(self):
        if self.image:
            save_path, _ = QFileDialog.getSaveFileName(self.ui, "Зберегти фото", "", "Зображення (*.png *.jpg *.jpeg)") #Відкриття файлу
            
            if save_path:
                self.image.save(save_path)
                print("Файл збережено")
                if self.workdir:
                    self.get_images()
                    self.ui.image_list.clear()
                    self.ui.image_list.addItems(self.folder_images) #Додавання картинки в список файлів  

    def delete_file(self):
        if self.image_path:
            check = QMessageBox.question(self.ui, "Видалити фото", "Ви впевнені, що хочете видалити фото?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if check == QMessageBox.StandardButton.Yes:
                try:
                    os.remove(self.image_path)
                    print("Файл видалено")
                    if self.workdir:
                        self.get_images()
                        self.ui.image_list.clear()
                        self.ui.image_list.addItems(self.folder_images) #Додавання картинки в список файлів 

                    self.ui.current_image.setPixmap(QPixmap("")) #Очищення відображення фото
                    self.image = None
                    self.image_path = None
                    self.original = None
                    self.history = []
                    self.history_index = -1
                except:
                    err = QMessageBox.critical(self.ui, "Помилка", "Помилка видалення файлу", "Спробуйте ще раз" QMessageBox.StandardButton.Ok)

    def do_black_white(self):
        if self.image:
            self.image = self.image.convert("L") #Робить фото чорно-білим
            self.add_to_history()
            self.show_image(self.temp_save())

    def do_blur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR) #Блюрить фото
            self.add_to_history()
            self.show_image(self.temp_save())

    def do_rotate_left(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_90) #Повертає фото на 90
            self.add_to_history()
            self.show_image(self.temp_save())

    def do_rotate_right(self):
        if self.image:
            self.image = self.image.transpose(Image.ROTATE_270) #Повертає фото на 90 в ліво
            self.add_to_history()
            self.show_image(self.temp_save())

    def do_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN) #Підвищення різкості
            self.add_to_history()
            self.show_image(self.temp_save())

    def do_bright(self):
        if self.image:
            bright = ImageEnhance.Brightness(self.image)  #Підвищення яскравості
            self.add_to_history()
            self.img = bright.enhance(1.5)
            self.show_image(self.temp_save())

    def do_contrast(self):
        if self.image:
            contrast = ImageEnhance.Contrast(self.image)  #Підвищення контрасту
            self.add_to_history()
            self.img = contrast.enhance(2)
            self.show_image(self.temp_save())

    def do_saturation(self):
        if self.image:
            color = ImageEnhance.Color(self.image)  #Підвищення насиченості кольору
            self.add_to_history()
            self.img = color.enhance(2)
            self.show_image(self.temp_save())


app = QApplication([])
editor= ImageEditor()

# Завантаження з темою
#apply_stylesheet(app, theme='light_red.xml')
# Завантаження з кастомними параметрами
#extra = {
    #'primaryColor': '#cb24db', # Це колір кнопок
    #'secondaryColor': '#383838', # Це колір фону
    #'fontFamily': 'Arial', # Це шрифт
#}
#apply_stylesheet(app, theme='dark_red.xml', extra=extra)

apply_stylesheet(app, theme='dark_lightgreen.xml')
app.exec()

#editor.open("rachel-harvey-JlW6UIFG1es-unsplash.jpg")
#editor.do_black_white()
#editor.image.save("result.jpg")