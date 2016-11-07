from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread
import tkinter as tk
import time
import os
import shutil
import requests

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        root.overrideredirect(True)
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        root.focus_set()  # <-- move focus to this widget
        self.pack(fill=tk.BOTH)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.index = 0
        self.ready = False
        logo = Image.open('slide1.jpg')
        self.logo_obj = ImageTk.PhotoImage(logo)
        self.photos = []

        self.create_widgets()
        
    def create_widgets(self):
        self.label = tk.Label(self, bd=0)
        self.label.pack()
        Thread(target=self.get_slides).start()
        Thread(target=self.animate).start()

    def animate(self):
        if self.ready:
            img = ImageTk.PhotoImage(file=self.photos[self.index]['image'])
            self.label.config(image=img)
            self.label.image=img
            if self.index >= len(self.photos)-1:
                self.index = 0
            else:
                self.index += 1
            if self.photos[self.index]['wait']:
                self.after(10000, self.animate)
            else:
                self.after(10, self.animate)
        else:
            self.label.config(image=self.logo_obj)
            self.label.image=self.logo_obj
            self.after(5000, self.animate)

    def get_slides(self):
        url = 'http://accordapp.com/display/slides'
        headers = {'AUTHORIZATION': 'Basic ZndiYzpMMHYzVzBya3M='}
        folder = 'slides'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        response = requests.get(url, headers=headers)
        data = response.json()
        anim_index = 0
        while anim_index < len(data):
            img1 = self.get_img(data[anim_index]['image'])
            anim_index += 1
            try:
                img2 = self.get_img(data[anim_index]['image'])
            except IndexError:
                img2 = self.get_img(data[0]['image'])
            alpha = 0
            while alpha <= 1:
                img = Image.blend(img1, img2, alpha)
                img_name = 'slides/slide' + str(anim_index) + str(alpha) + '.jpg'
                img.save(img_name)
                if alpha == 0:
                    original = True
                else:
                    original = False
                self.photos.append({'image': img_name, 'wait': original})
                alpha += .1
        self.ready = True
        self.after(600000, self.get_slides)

    def get_img(self, url):
        img_response = requests.get(url.replace('https', 'http'))
        img = Image.open(BytesIO(img_response.content))
        img = img.resize((1920, 1080))
        return img

    def close(self):
        os._exit(0)

root = tk.Tk()
app = Application(root)

root.mainloop()
