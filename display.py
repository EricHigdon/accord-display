from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread
import tkinter as tk
import time
import os
import requests

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        root.overrideredirect(True)
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        root.focus_set()  # <-- move focus to this widget
        root.bind("<Escape>", lambda e: e.widget.quit())
        self.pack(fill=tk.BOTH)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.url = 'http://accordapp.com/display/slides'
        self.headers = {'AUTHORIZATION': 'Basic ZndiYzpMMHYzVzBya3M='}
        response = requests.get(self.url, headers=self.headers)
        self.photos = [
            slide['image'] for slide in response.json()
        ] 
        self.index = 0

        self.create_widgets()
        
    def create_widgets(self):
        self.label = tk.Label(self, bd=0)
        self.label.pack()
        Thread(target=self.animate).start()
        Thread(target=self.update).start()

    def animate(self):
        img_response = requests.get(self.photos[self.index].replace('https', 'http'))
        img = Image.open(BytesIO(img_response.content))
        basewidth = 1920
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img_obj = ImageTk.PhotoImage(img)
        self.label.config(image=img_obj)
        self.label.image=img_obj
        if self.index >= len(self.photos)-1:
            self.index = 0
        else:
            self.index += 1
        self.after(1000, self.animate)

    def update(self):
        response = requests.get(self.url, headers=self.headers)
        self.photos = [
            slide['image'] for slide in response.json()
        ] 
        print(self.photos)
        self.index = 0
        self.after(600000, self.update)

    def close(self):
        os._exit(0)

root = tk.Tk()
app = Application(root)

root.mainloop()
