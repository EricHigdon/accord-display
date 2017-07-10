from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread
import tkinter as tk
import time
import os
import shutil
import requests
import settings
from datetime import datetime, timedelta

class Application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        root.overrideredirect(True)
        self.width = getattr(settings, 'WIDTH', root.winfo_screenwidth())
        self.height = getattr(settings, 'HEIGHT', root.winfo_screenheight()) 
        root.geometry("{0}x{1}+0+0".format(self.width, self.height))
        root.focus_set()  # <-- move focus to this widget
        self.pack(fill=tk.BOTH)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.index = 0
        self.ready = False
        logo = Image.open('slide1.jpg')
        logo = logo.resize((self.width, self.height))
        self.logo_obj = ImageTk.PhotoImage(logo)
        self.photos = []
        self.countdown_to = None
        self.counting_down = False
        self.countdown_image = None
        self.countdown_position = None

        self.create_canvas()
        
    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bd=0)
        self.canvas.pack(side='top', fill='both', expand=True)
        self.image = self.canvas.create_image(
            0,
            0,
            anchor='nw',
            image=self.logo_obj
        )
        self.timeleft = self.canvas.create_text(
            self.width-5,
            self.height-2,
            anchor="se",
        )
        Thread(target=self.get_slides).start()
        Thread(target=self.animate).start()
        Thread(target=self.countdown).start()

    def countdown(self):
        if self.countdown_to and self.countdown_image is not None:
            time_left = self.countdown_to - datetime.now()
            if time_left < timedelta(minutes=5) and time_left > timedelta():
                minutes = int(time_left.seconds/60)
                seconds = time_left.seconds - minutes * 60
                options = {}
                if self.countdown_position == 'topleft':
                    options = {
                        'x': 5,
                        'y': 5
                    }
                elif self.countdown_position == 'topright':
                    options = {
                        'x': 5,
                        'y': self.width-5
                    }
                elif self.countdown_position == 'center':
                    options = {
                        'x': 0,
                        'y': 0,
                        'anchor': 'center'
                    }
                elif self.countdown_position == 'bottomleft':
                    options = {
                        'x': self.height-5,
                        'y': 5
                    }
                elif self.countdown_position == 'bottomright':
                    options = {
                        'x': self.height-5,
                        'y': self.widht-5
                    }
                self.canvas.itemconfig(
                    self.timeleft,
                    text='{}:{:02d}'.format(minutes, seconds),
                    **options
                )

                # Display the countdown image
                self.counting_down = True
                global img
                img = ImageTk.PhotoImage(file=self.countdown_image)
                self.canvas.itemconfig(self.image, image=img)
            else:
                self.canvas.itemconfig(self.timeleft, text='')
                self.counting_down = False
        self.after(1000, self.countdown)
        

    def animate(self):
        global img
        if not self.counting_down:
            if self.ready:
                img = ImageTk.PhotoImage(file=self.photos[self.index]['image'])
                self.canvas.itemconfig(self.image, image=img)
                if self.index >= len(self.photos)-1:
                    self.index = 0
                else:
                    self.index += 1
                if self.photos[self.index]['wait']:
                    self.after(10000, self.animate)
                else:
                    self.after(1, self.animate)
            else:
                self.canvas.itemconfig(self.image, image=self.logo_obj)
                self.after(5000, self.animate)

    def get_slides(self):
        url = getattr(settings, 'SLIDES_URL', 'http://accordapp.com/display/slides')
        headers = {'AUTHORIZATION': 'Basic {}'.format(getattr(settings, 'KEY', 'ZndiYzpMMHYzVzBya3M='))}
        response = requests.get(url, headers=headers)
        data = response.json()
        self.empty_slides_folder()
        anim_index = 0
        while anim_index < len(data):
            countdown_position = None
            img1 = self.get_img(data[anim_index]['image'])
            countdown_position = data[anim_index].get('countdown_position', None)
            anim_index += 1
            try:
                img2 = self.get_img(data[anim_index]['image'])
            except IndexError:
                img2 = self.get_img(data[0]['image'])
            if animation is not None:
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
            else:
                image_name = 'slides/slide'+str(anim_index)+'.jpg'
                img1.save(image_name)
                self.photos.append({'image': image_name, 'wait': True})

        # Get countdown information
        countdown_url = getattr(settings, 'COUNTDOWN_URL', 'http://accordapp.com/display/countdown')
        response = requests.get(countdown_url, headers=headers).json()
        self.countdown_to = datetime.strptime(response[0]['countdown'], '%Y-%m-%dT%H:%M:%S') 
        img_url = response[0]['countdown_image']
        if img_url is not None:
            image = self.get_img()
            self.countdown_image = 'slides/slide'+str(anim_index)+'.jpg'
            image.save(self.countdown_image)
            self.countdown_position = response[0]['countdown_position']

        self.ready = True
        self.after(60000, self.get_slides)

    def get_img(self, url):
        img_response = requests.get(url.replace('https', 'http'))
        img = Image.open(BytesIO(img_response.content))
        img = img.resize((self.width, self.height))
        return img

    def empty_slides_folder(self):
        folder = 'slides'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    def close(self):
        self.empty_slides_folder()
        os._exit(0)

animation = None
root = tk.Tk()
app = Application(root)

root.mainloop()
