import tkinter
import youtube_search
import json
import yt_dlp
import PIL
from tkinter import ttk
import sv_ttk
from tkinter import filedialog
import os
import quickbar
import time
import webbrowser
import re

def rgb(r: int, b: int, g: int):
    return "#%02x%02x%02x" % (r, g, b)

class spyracy():
    def __init__(self):
        self.cached_songs = []

    def getData(self, URL: str):
        data = youtube_search.YoutubeSearch(search_terms=URL, max_results=1).to_json()
        return data

    def get(self, ITEM: str, URL: str):
        jLoads = json.loads(self.getData(URL=URL))
        return jLoads["videos"][0][ITEM]

    def download(self, video: str):
        output_renamer = lambda s: re.sub(r'[^\w\s]', '', s.strip().replace('[', '').replace(']', ''))[:255]
        config = {"outtmpl": output_renamer(video),
                  "format": "bestaudio/best",
                  "postprocessors": [
                      {
                          "key": "FFmpegExtractAudio", "preferredcodec": "flac",
                      }
                  ],
                 }
        yt_dlp.YoutubeDL(config).download(self.get("id", video))

    def load_search_terms(self, filename):
        for index, line in enumerate(open(filename, "r").readlines()):
            try:
                self.cached_songs.append(line)
                print("[LOG] Loaded Search Term #%s successfully!" % str(index + 1))
            except Exception as e:
                print("[LOG] Failed to load Search Term #%s! (%s)" % (str(index + 1)), e)

    def download_search_terms(self):
        for url in self.cached_songs:
            self.download(url)
        print("[LOG] Downloaded %s Songs!" % str(len(self.cached_songs)))
        # self.cached_songs.clear()


sPYracy = spyracy()

root = tkinter.Tk()
root.geometry("900x600")
# root.configure(bg=rgb(30, 30, 30))
root.title("sPYracy ALPHA 1")

root.attributes("-alpha", 0.9)  
root.resizable(0,0)

sv_ttk.set_theme("dark")
branding = ttk.Label(root, text="sPYracy (ALPHA RECODE)", width=100, anchor=tkinter.CENTER, font=("Arial", 12))
branding.grid(column=0, row=0, pady=(10, 0))

basics = ttk.LabelFrame(root, text="Basic Downloads", padding=10)
basics.grid(column=0, row=1, pady=(50,5))

download_box = ttk.Entry(basics, width=50)
download_box.grid(column=0, row=0, pady=(5, 5))

download_button = ttk.Button(basics, text="Download", command=lambda: sPYracy.download(download_box.get()), width=52)
download_button.grid(column=0, row=1, pady=(5, 5))

file_stuff = ttk.LabelFrame(root, text="Downloads From File", width=52, padding=10)
file_stuff.grid(column=0, row=2, pady=(5, 5))

get_search_terms = ttk.Button(file_stuff, text="Load Songs from file to cache", command=lambda: sPYracy.load_search_terms(filedialog.askopenfilename()), width=52)
get_search_terms.grid(column=0, row=0, pady=(5, 5))

download_lsearch_terms = ttk.Button(file_stuff, text="Download Songs from cache", command=lambda: sPYracy.download_search_terms(), width=52)
download_lsearch_terms.grid(column=0, row=1, pady=(5, 5))

clear_lsearch_terms = ttk.Button(file_stuff, text="Clear cache", width=52, command=lambda: exec('lambda: sPYracy.cached_songs.clear(), print("[LOG] Cleared cached Search Terms!")'))
clear_lsearch_terms.grid(column=0, row=2, pady=(5, 5))

val = tkinter.IntVar()
val.set(1)

style = tkinter.IntVar()

dev_toggle = tkinter.IntVar()

def toggle_dev(dev_toggle):
    if dev_toggle.get() == 1:
        term.grid(column=1, row=0)
        value.grid(column=1, row=1)
        get_data.grid(column=1, row=2)
    else:
        term.grid_forget()
        value.grid_forget()
        get_data.grid_forget()

def set_theme(style):
    if style.get() == 1:
        sv_ttk.set_theme("light")
    else: sv_ttk.set_theme("dark")

def set_transparent(val):
    if val.get() == 1:
        root.attributes("-alpha", 0.9)
    else:
        root.attributes("-alpha", 1)


options = ttk.Labelframe(root, text="Options", padding=10)
options.grid(column=0, row=6, pady=(5, 5))

developer_mode = ttk.Checkbutton(options, text="Developer Mode", width=52, variable=dev_toggle, command=lambda: toggle_dev(dev_toggle))
developer_mode.grid(column=0, row=0, pady=(5, 5))

theme = ttk.Checkbutton(options, text="Light Theme", variable=style, width=52, command=lambda: set_theme(style))
theme.grid(column=0, row=1, pady=(5, 5))

transparent = ttk.Checkbutton(options, text="Transparent", variable=val, width=52, command=lambda: set_transparent(val))
transparent.grid(column=0, row=2, pady=(5,5))

term = ttk.Entry(options, width=15)
term.insert(0, "Term Data")

value = ttk.Entry(options, width=15)
value.insert(0, "Term")

get_data = ttk.Button(options, width=15, text="Get Term Data", command=lambda: print("[LOG] Term Data '%s' -> %s" % (term.get(), sPYracy.get(term.get(), value.get()))))   

exit_button = ttk.Button(root, text="Exit sPYracy", command=lambda: root.destroy(), width=10)
exit_button.place(x=780, y=560) # grid(column=0, row=100, pady=(365, 0), padx=(775,0))

src_code = ttk.Button(root, text="Source Code", command=lambda: webbrowser.open("https://github.com/GogleSiteBank/spyracy-beta"))
src_code.place(x=10, y=560)

#temp = ttk.Button(options, text="test button")
#temp.grid(column=1, row=0)

root.mainloop()
