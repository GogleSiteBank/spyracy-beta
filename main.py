import tkinter
import youtube_search
import json
import yt_dlp
import PIL
from tkinter import ttk
import sv_ttk
from tkinter import filedialog
import os
import time
import webbrowser
import re
import sys
from tkinter import messagebox
import ast

def rgb(r: int, b: int, g: int):
    return "#%02x%02x%02x" % (r, g, b)

class spyracy():
    def __init__(self):
        self.cached_songs = []
        self.codec = "flac"
        self.config = open("%s\\config.spyc" % os.getenv("appdata"), "a+")
        self.configurated_options = None
        with open("%s\\config.spyc" % os.getenv("appdata"), "a+") as config:
            config.seek(0)
            self.configurated_options = str(config.read()) if not os.stat("%s\\config.spyc" % os.getenv("appdata")).st_size == 0 else "000|0.9"

    def getData(self, URL: str):
        data = youtube_search.YoutubeSearch(search_terms=URL, max_results=1).to_json()
        return data

    def get(self, ITEM: str, URL: str):
        jLoads = json.loads(self.getData(URL=URL))
        return jLoads["videos"][0][ITEM]

    def download(self, video: str, album: bool=False):
        output_renamer = lambda s: re.sub(r'[^\w\s]', '', s.strip().replace('[', '').replace(']', ''))[:255]
        config = {"outtmpl": output_renamer(video) if not album else "%(title)s",
         "write_thumbnail": True,
         'embed-metadata': True,
         'parse-metadata': '%(artist)s - %(title)s',
          "format": "bestaudio/best",
          "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": self.codec,
          },
            {
                "key": 'FFmpegMetadata'
            }
          ]}
        if album:
            config.update({"yes-playlist": True})
        video_url = video if album else self.get("id", video)
        yt_dlp.YoutubeDL(config).download(video_url)
        print("[LOG] Downloaded Song '%s'" % output_renamer(video) if not album else "%(title)s")

    def switch_config(self):
        self.codec = "flac" if self.codec == "mp4" else "mp4"
        print("[LOG] Codec Changed to '%s'" % self.codec)

    def load_search_terms(self, filename):
        for index, line in enumerate(open(filename, "r").readlines()):
            try:
                self.cached_songs.append(line)
                print("[LOG] Loaded Search Term #%s successfully!" % str(index + 1))
            except Exception as e:
                print("[LOG] Failed to load Search Term #%s! (%s)" % (str(index + 1)), e)

    def download_search_terms(self, album=False):
        for url in self.cached_songs:
            self.download(url, album=album)
        print("[LOG] Downloaded %s %s!" % (str(len(self.cached_songs)), "Albums" if album else "Songs"))
        self.cached_songs.clear() # WHY WAS THIS COMMENTED? HOW STUPID.


sPYracy = spyracy()

root = tkinter.Tk()
root.geometry("900x625")
# root.configure(bg=rgb(30, 30, 30))
root.title("sPYracy")

root.attributes("-alpha", 0.9)  
root.resizable(0,0)

sv_ttk.set_theme("dark")
branding = ttk.Label(root, text="sPYracy", width=100, anchor=tkinter.CENTER, font=("Arial", 12))
branding.grid(column=0, row=0, pady=(10, 0))

basics = ttk.LabelFrame(root, text="Basic Downloads", padding=10)
basics.grid(column=0, row=1, pady=(5,5))

download_box = ttk.Entry(basics, width=72)
download_box.grid(column=0, row=0, pady=(5, 5))

download_button = ttk.Button(basics, text="Download", command=lambda: sPYracy.download(download_box.get()), width=72)
download_button.grid(column=0, row=1, pady=(5, 5))

playlist_button = ttk.Button(basics, text="Download As Playlist/Album (requires playlist URL/ID)", width=72, command=lambda: sPYracy.download(download_box.get(), album=True))
playlist_button.grid(column=0, row=2, pady=(5,5))



file_stuff = ttk.LabelFrame(root, text="Downloads From File", padding=10)
file_stuff.grid(column=0, row=2, pady=(5, 5))

get_search_terms = ttk.Button(file_stuff, text="Load Songs from file to cache", command=lambda: sPYracy.load_search_terms(filedialog.askopenfilename()), width=52)
get_search_terms.grid(column=0, row=0, pady=(5, 5))

download_lsearch_terms = ttk.Button(file_stuff, text="Download Songs from cache", command=lambda: sPYracy.download_search_terms(), width=52)
download_lsearch_terms.grid(column=0, row=1, pady=(5, 5))

download_lsearch_albums = ttk.Button(file_stuff, text="Download from cache (as albums)", width=72, command=lambda: sPYracy.download_search_terms(True))
download_lsearch_albums.grid(column=0, row=2, pady=(5, 5), columnspan=2)

clear_lsearch_terms = ttk.Button(file_stuff, text="Clear cache", width=72, command=lambda: (sPYracy.cached_songs.clear(), print("[LOG] Cleared cached Search Terms!")))
clear_lsearch_terms.grid(column=0, row=3, pady=(5, 5), columnspan=2)

add_box = ttk.Entry(file_stuff, width=15)
add_box.grid(column=1, row=0, pady=(5, 5), padx=(10, 0))

add_button = ttk.Button(file_stuff, width=15, text="Add to cache", command=lambda: (sPYracy.cached_songs.append(add_box.get()), messagebox.showinfo(title="sPYracy", message="Added '%s' to cached songs!" % add_box.get())))
add_button.grid(column=1, row=1, padx=(10, 0))

val = tkinter.IntVar()

style = tkinter.IntVar()

dev_toggle = tkinter.IntVar()

def toggle_dev(dev_toggle):
    elements = [term, value, get_data, reload_spyracy, save_config]
    if dev_toggle.get() == 1:
        for index, element in enumerate(elements):
            element.grid(column=1, row=index, padx=(10, 0))
    else:
        for index, element in enumerate(elements):
            element.grid_forget()

def set_theme(style):
    if style.get() == 1:
        sv_ttk.set_theme("light")
    else: sv_ttk.set_theme("dark")

def set_transparent(value):
    root.attributes("-alpha", value)



options_values = [
    0,
    0,
    0,
    0.9
]

#try:
options_values[0] = sPYracy.configurated_options[0]
options_values[1] = sPYracy.configurated_options[1]
options_values[2] = sPYracy.configurated_options[2]
options_values[3] = float(sPYracy.configurated_options.split("|")[1])
#except: ...



options = ttk.Labelframe(root, text="Options", padding=10)
options.grid(column=0, row=6, pady=(5, 5))

developer_mode = ttk.Checkbutton(options, text="Developer Options", style='Switch.TCheckbutton', width=49, variable=dev_toggle, command=lambda: toggle_dev(dev_toggle))
developer_mode.grid(column=0, row=0, pady=(5, 5))

theme = ttk.Checkbutton(options, text="Light Theme", style='Switch.TCheckbutton', variable=style, width=49, command=lambda: set_theme(style))
theme.grid(column=0, row=1, pady=(5, 5))

mp4_mode = ttk.Checkbutton(options, text="MP4/Video Mode", style='Switch.TCheckbutton', width=49, command=lambda: sPYracy.switch_config())
mp4_mode.grid(column=0, row=2, pady=(5,5))
transparent = ttk.Label(options, text="Opacity")
transparent.grid(column=0, row=3, pady=(5,5), sticky="w")


transparency = ttk.Scale(options, from_=0.3, to=1, variable=val, command=set_transparent, length=375)
transparency.set(0.9)
transparency.grid(column=0, row=3, pady=(5,5), sticky="e")



reset_transparency = ttk.Button(options, text="Reset Opacity", command=lambda: (set_transparent(0.9), val.set(0.9)), width=52)
reset_transparency.grid(column=0, row=4, pady=(5,5))

term = ttk.Entry(options, width=15)
term.insert(0, "Term Data")

value = ttk.Entry(options, width=15)
value.insert(0, "Term")

get_data = ttk.Button(options, width=15, text="Get Term Data", command=lambda: print("[LOG] Term Data '%s' -> %s" % (term.get(), sPYracy.get(term.get(), value.get()))))   

reload_spyracy = ttk.Button(options, width=15, text="Reload sPYracy", command=lambda: (print("[LOG] sPYracy is reloading"), os.execl(sys.executable, sys.executable, *sys.argv)))

save_config = ttk.Button(options, width=15, text="Save Config", command=lambda: (sPYracy.config.truncate(0),sPYracy.config.write("%s%s%s|%s" % (str(dev_toggle.get()), str(style.get()), "1" if sPYracy.codec == "mp4" else "flac", str(transparency.get()))), print("[LOG] Config saved!"), sPYracy.config.close()))

exit_button = ttk.Button(root, text="Exit sPYracy", command=lambda: (sPYracy.config.truncate(0),sPYracy.config.write("%s%s%s|%s" % (str(dev_toggle.get()), str(style.get()), "1" if sPYracy.codec == "mp4" else "flac", str(transparency.get()))), print("[LOG] Config saved!"), sPYracy.config.close(), root.destroy()), width=10)
exit_button.place(x=780, y=585) # grid(column=0, row=100, pady=(365, 0), padx=(775,0))

src_code = ttk.Button(root, text="Source Code", command=lambda: webbrowser.open("https://github.com/GogleSiteBank/spyracy-beta"))
src_code.place(x=10, y=585)

transparency.set(options_values[3])
developer_mode.state(["selected" if options_values[0] == "1" else ""])
dev_toggle.set(1 if options_values[0] == "1" else 0)
toggle_dev(dev_toggle)
theme.state(["selected" if options_values[1] == "1" else ""])
style.set(1 if options_values[1] == "1" else 0)
set_theme(style)
mp4_mode.state(["selected" if options_values[2] == "1" else ""])
if "selected" in mp4_mode.state(): sPYracy.switch_config()

#temp = ttk.Button(options, text="test button")
#temp.grid(column=1, row=0)

root.mainloop()