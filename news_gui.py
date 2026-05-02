import io
import webbrowser
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image
import xml.etree.ElementTree as ET
import re


class NewsApp:

    def __init__(self):

        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url)
        root_xml = ET.fromstring(response.content)

        self.articles = []

        for item in root_xml.findall('.//item')[:20]:
            title = item.find('title').text
            desc = item.find('description').text or ""
            clean_desc = re.sub('<.*?>', '', desc)

            self.articles.append({
                "title": title,
                "description": clean_desc,
                "url": item.find('link').text
            })

        self.load_gui()
        self.load_news_item(0)
        self.root.mainloop()

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('600x700')
        self.root.title('Mera News App')
        self.root.configure(background='black')

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_news_item(self, index):

        self.clear()
        article = self.articles[index]

        try:
            raw_data = urlopen("https://picsum.photos/600/250").read()
            im = Image.open(io.BytesIO(raw_data))
        except:
            im = Image.new("RGB", (600, 250), color="gray")

        photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo, bg='black')
        label.image = photo
        label.pack(pady=10)

        heading = Label(
            self.root,
            text=article['title'],
            bg='black',
            fg='white',
            wraplength=550,
            justify='center',
            font=('verdana', 16, 'bold')
        )
        heading.pack(pady=10)

        frame = Frame(self.root, bg='black')
        frame.pack(pady=10)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        text = Text(
            frame,
            height=10,
            width=70,
            wrap=WORD,
            yscrollcommand=scrollbar.set
        )
        text.insert(END, article['description'])
        text.config(state=DISABLED)
        text.pack()

        scrollbar.config(command=text.yview)

        btn_frame = Frame(self.root, bg='black')
        btn_frame.pack(pady=20)

        if index > 0:
            Button(
                btn_frame,
                text='⬅ Prev',
                width=15,
                command=lambda: self.load_news_item(index - 1)
            ).pack(side=LEFT, padx=5)

        Button(
            btn_frame,
            text='Read More',
            width=15,
            command=lambda: self.open_link(article['url'])
        ).pack(side=LEFT, padx=5)

        if index < len(self.articles) - 1:
            Button(
                btn_frame,
                text='Next ➡',
                width=15,
                command=lambda: self.load_news_item(index + 1)
            ).pack(side=LEFT, padx=5)

    def open_link(self, url):
        webbrowser.open(url)


NewsApp()