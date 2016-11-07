from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
import time
import os
import requests

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        #root.attributes("-fullscreen", True)
        root.overrideredirect(True)
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        root.focus_set()  # <-- move focus to this widget
        root.bind("<Escape>", lambda e: e.widget.quit())
        self.pack(fill=tk.BOTH)
        root.protocol("WM_DELETE_WINDOW", self.close)
        url = 'http://accordapp.com/display/slides'
        headers = {'AUTHORIZATION': 'Basic ZndiYzpMMHYzVzBya3M='}
        response = requests.get(url, headers=headers)
        self.photos = [
            slide['image'] for slide in response.json()
        ] 
        self.index = 0

        self.create_widgets()
        
    def create_widgets(self):
        self.label = tk.Label(self, bd=0)
        self.label.pack()
        self.animate()

    def animate(self):
        img_response = requests.get(self.photos[self.index].replace('https', 'http'))
        img = Image.open(BytesIO(img_response.content))
        img_obj = ImageTk.PhotoImage(img)
        self.label.config(image=img_obj)
        self.label.image=img_obj
        if self.index >= len(self.photos)-1:
            self.index = 0
        else:
            self.index += 1
        self.after(10000, self.animate)

    def close(self):
        os._exit(0)

root = tk.Tk()
app = Application(root)

root.mainloop()