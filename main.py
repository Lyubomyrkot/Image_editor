from PIL import Image, ImageFilter, ImageEnhance
from PyQt6 import QtWidgets, uic
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from qt_material import apply_stylesheet




#with Image.open("jonatan-pie-_b2hvhIXGI8-unsplash.jpg") as img:
    #print("Розмір:", img.size)
    #print("Формат:", img.format)
    #print("Тип:", img.mode)
    #black_img = img.convert("L") #чорнобіле фото робить
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

    #color_img = ImageEnhance.Color(img)enhance(2)#насиченість кольору
    #color_img.save(name + "color_img.jpg")
    #color_img.show()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('window.ui', self)

class ImageEditor():
    def __init__(self,):
        self.origiinal = None
        self.image = None
        self.save_path = 'edited/'
        self.ui = Ui()
        self.ui.show()

    def open(self, filename):
        self.image = Image.open(filename)
        self.original = self.image

    def do_black_white(self):
        self.img = self.img.convert("L") #чорнобіле фото робить
    
    def do_blur(self):
        self.image = self.img.filter(ImageFilter.BLUR)
    
    def do_rotate_90(self):
        self.img = self.img.transpose(Image.ROTATE_90)
    
    def do_sharpen(self):
        self.img = self.img.filter(ImageFilter.SHARPEN)
    
    #def do_bright(self):

app = QApplication([])
editor= ImageEditor()
apply_stylesheet(app, theme='light_red.xml')
app.exec()

#editor.open("rachel-harvey-JlW6UIFG1es-unsplash.jpg")
#editor.do_black_white()
#editor.image.save("result.jpg")