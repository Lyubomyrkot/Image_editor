from PIL import Image, ImageFilter, ImageEnhance
from PyQt6 import QtWidgets, uic
import sys
import os

from PyQt6.QtWidgets import QApplication, QFileDialog
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
        self.save_path = 'edited/'
        self.ui = Ui()
        self.ui.show()
        self.connects()

    def connects(self):
        self.ui.folder_btn.clicked.connect(self.open_folder) #Підключення кнопок до функції
        self.ui.open_folder.triggered.connect(self.open_folder)
        self.ui.open_file.triggered.connect(self.open_file)

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
            self.ui.image_list.addItems(self.folder_images) #Додавання картинки в список файлів 

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "Виберіть фото", "", "Зображення (*.png *.jpg *.jpeg)") #Відкриття файлу
        if file_path:
            self.open(file_path)
            print(self.image.filename)

    def open(self, filename):
        self.image = Image.open(filename)
        self.original = self.image

    def do_black_white(self):
        self.img = self.img.convert("L") #Робить фото чорно-білим
    
    def do_blur(self):
        self.img = self.img.filter(ImageFilter.BLUR) #Блюрить фото
    
    def do_rotate_90(self):
        self.img = self.img.transpose(Image.ROTATE_90) #Повертає фото на 90
    
    def do_sharpen(self):
        self.img = self.img.filter(ImageFilter.SHARPEN) #Підвищення різкості
    
    def do_bright(self):
        bright = ImageEnhance.Brightness(self.image)  #Підвищення яскравості
        self.img = bright.enhance(1.5)

    def do_contrast(self):
        contrast = ImageEnhance.Contrast(self.image)  #Підвищення контрасту
        self.img = contrast.enhance(2)

    def do_color(self):
        color = ImageEnhance.Color(self.image)  #Підвищення насиченості кольору
        self.img = color.enhance(2)



app = QApplication([])
editor= ImageEditor()
apply_stylesheet(app, theme='light_red.xml')
app.exec()

#editor.open("rachel-harvey-JlW6UIFG1es-unsplash.jpg")
#editor.do_black_white()
#editor.image.save("result.jpg")