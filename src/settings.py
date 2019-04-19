import os
import sys
import json
import tkinter as tk
from tkinter import messagebox

from tkcolorpicker import askcolor
import pygame as pg
from options import Options
from color import Color, RED

data = json.load(open("src/screen_text.json"))


def get_text(name):
    return data["settings"][name][Options.language]


# noinspection PyAttributeOutsideInit
class Application(tk.Frame):
    """
    A settings window with tkinter
    Grid:
              0       1
         ---------|--------|
     0         Settings
     1       mute | not log
     2    no zmbs | debug
     3      night | pitch black
     4          m | f
     5        nor | eng
     6        FPS | FPS Entry
     7        Map | Map Entry
     8     volume | volume slider
     9   Tile len | Tile len slider
    10        Div by 12
    11 Fillcolor | Loopcolor
    12     Commit | Discard
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        master.title(get_text("header"))
        master.protocol("WM_DELETE_WINDOW", self.exit)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=1, uniform="a")
        self.changed = False
        self.my_grid = {"settings":    (0,  0),
                        "is_mute":     (0,  1), "is_not_log":      (1, 1),
                        "is_no_zmbs":  (0,  2), "is_debug":        (1, 2),
                        "is_night":    (0,  3), "is_pitch_black":  (1, 3),
                        "m":           (0,  4), "f":               (1, 4),
                        "nor":         (0,  5), "eng":             (1, 5),
                        "fps":         (0,  6), "FPS Entry":       (1, 6),
                        "map":         (0,  7), "Map Entry":       (1, 7),
                        "volume":      (0,  8), "volume slider":   (1, 8),
                        "tile_length": (0,  9), "Tile len slider": (1, 9),
                        "Div by 12":   (0, 10),
                        "Fillcolor":  (0, 11), "Loopcolor":     (1, 11),
                        "Commit":      (0, 12), "Discard":        (1, 12)}
        self.create_widgets()

    def create_widgets(self):
        c, r = self.my_grid["settings"]

        tk.Label(self, text=get_text("header"),
                 font="helvetica 12 bold", justify="center").grid(
                     column=c, row=r, columnspan=2, sticky="nwneswse")
        self.flags()
        self.labels()
        self.gender_radio_buttons()
        self.language_radio_buttons()
        self.fps_entry()
        self.map_dropdown()
        self.volume_slider()
        self.tile_length_slider()
        self.tile_length_nearest12()
        self.color_picker()
        c, r = self.my_grid["Discard"]
        tk.Button(self, text=get_text("discard"),
                  fg=RED.get_rgb_hex(), command=self.exit).grid(
                      column=c, row=r, sticky="nwneswse")
        c, r = self.my_grid["Commit"]
        tk.Button(self, text=get_text("commit"),
                  command=self.commit).grid(column=c, row=r, sticky="nwneswse")

    def commit(self):
        if (Options.mapname != self.map.get() or
                Options.tile_length != int(self.tile_length.get()) or
                Options.language != self.language.get()):
            self.changed = True
        Options.fps = int(self.FPS.get())
        Options.mapname = self.map.get()
        Options.volume = float(self.volume.get())
        Options.mute = self.is_mute.get()
        Options.night = self.is_night.get()
        Options.pitch_black = self.is_pitch_black.get()
        Options.tile_length = int(self.tile_length.get())
        Options.gender = self.gender.get()
        Options.not_log = self.is_not_log.get()
        Options.no_zombies = self.is_no_zmbs.get()
        Options.debug = self.is_debug.get()
        Options.language = self.language.get()
        Options.loopcolor = self.loopcolor
        Options.fillcolor = self.fillcolor
        try:
            Options.assertions()
        except AssertionError as e:
            messagebox.showwarning("Error", e)
        else:
            try:
                Options.warnings()
            except AssertionError as e:
                if messagebox.askyesno("warning", str(e) + "\nVil du fortsette?"):
                    self.exit()
                else:
                    return
            else:
                self.exit()

    def flags(self):
        self.is_mute, self.is_not_log = tk.BooleanVar(None, Options.mute), tk.BooleanVar(None, Options.not_log)
        self.is_no_zmbs, self.is_debug = tk.BooleanVar(None, Options.no_zombies), tk.BooleanVar(None, Options.debug)
        self.is_night, self.is_pitch_black = tk.BooleanVar(None, Options.night), tk.BooleanVar(None, Options.pitch_black)
        variables = "is_mute", "is_not_log", "is_no_zmbs", "is_debug", "is_night", "is_pitch_black"
        texts = (get_text(s) for s in (
                 "mute", "not_log", "no_zombies", "debug", "night", "pitch_black"))
        for var, text in zip(variables, texts):
            button = tk.Checkbutton(self, text=text, variable=getattr(self, var))
            c, r = self.my_grid[var]
            button.grid(column=c, row=r, sticky="nwneswse")

    def labels(self):
        eng_texts = "fps", "map", "tile_length", "volume"
        texts = (get_text(s) for s in eng_texts)
        for text, eng_text in zip(texts, eng_texts):
            c, r = self.my_grid[eng_text]
            tk.Label(self, text=text, anchor="e").grid(column=c, row=r, sticky="nwneswse")

    def gender_radio_buttons(self):
        self.gender = tk.StringVar(None, Options.gender)
        self.male_b = tk.Radiobutton(self, text=get_text("male"),
                                     value="m", variable=self.gender)
        c, r = self.my_grid["m"]
        self.male_b.grid(column=c, row=r, sticky="nwneswse")
        self.female_b = tk.Radiobutton(self, text=get_text("female"),
                                       value="f", variable=self.gender)
        c, r = self.my_grid["f"]
        self.female_b.grid(column=c, row=r, sticky="nwneswse")

    def language_radio_buttons(self):
        self.language = tk.StringVar(None, Options.language)
        self.norwegian_b = tk.Radiobutton(self, text=get_text("norwegian"),
                                          value="norsk", variable=self.language)
        c, r = self.my_grid["nor"]

        self.norwegian_b.grid(column=c, row=r, sticky="nwneswse")
        self.english_b = tk.Radiobutton(self, text=get_text("english"),
                                        value="english", variable=self.language)
        c, r = self.my_grid["eng"]

        self.english_b.grid(column=c, row=r, sticky="nwneswse")

    def fps_entry(self):
        self.FPS = tk.Entry(self)
        self.FPS.insert(0, Options.fps)
        c, r = self.my_grid["FPS Entry"]
        self.FPS.grid(column=c, row=r, sticky="nwneswse")

    def map_dropdown(self):
        map_filter = lambda m: m.endswith(".txt") and "test" not in m
        options = filter(map_filter, os.listdir("assets/Maps/"))
        self.map = tk.StringVar(self, Options.mapname)
        self.dropdown = tk.OptionMenu(self, self.map, *options)
        c, r = self.my_grid["Map Entry"]
        self.dropdown.grid(column=c, row=r, sticky="nwneswse")

    def volume_slider(self):
        self.volume = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.05)
        self.volume.set(Options.volume)
        c, r = self.my_grid["volume slider"]

        self.volume.grid(column=c, row=r, sticky="nwneswse")

    def tile_length_slider(self):
        self.tile_length = tk.Scale(self, from_=12, to=100, orient=tk.HORIZONTAL)
        self.tile_length.set(Options.tile_length)
        c, r = self.my_grid["Tile len slider"]

        self.tile_length.grid(column=c, row=r, sticky="nwneswse")

    def tile_length_nearest12(self):
        self.tile_length_button = tk.Button(self, text=get_text("div12"),
                                            command=self.tl_button_command)
        c, r = self.my_grid["Div by 12"]

        self.tile_length_button.grid(column=c, row=r, columnspan=2, sticky="nwneswse")

    def tl_button_command(self):
        curr_tile_length = int(self.tile_length.get())
        tl_mod12 = curr_tile_length % 12
        if tl_mod12 <= 6:
            self.tile_length.set(curr_tile_length - tl_mod12)
        else:
            self.tile_length.set(curr_tile_length + 12 - tl_mod12)

    def color_picker(self):
        self.loopcolor, self.fillcolor = Options.loopcolor, Options.fillcolor
        self.loopcolor_button = tk.Button(self,
                                           text=get_text("loopcolor"),
                                           command=self.change_loopcolor,
                                           bg=self.loopcolor.get_rgb_hex(),
                                           fg=self.loopcolor.contrasting().get_rgb_hex())
        c, r = self.my_grid["Loopcolor"]

        self.loopcolor_button.grid(column=c, row=r, sticky="nwneswse")
        self.fillcolor_button = tk.Button(self,
                                           text=get_text("fillcolor"),
                                           command=self.change_fillcolor,
                                           bg=self.fillcolor.get_rgb_hex(),
                                           fg=self.fillcolor.contrasting().get_rgb_hex())
        c, r = self.my_grid["Fillcolor"]

        self.fillcolor_button.grid(column=c, row=r, sticky="nwneswse")

    def change_loopcolor(self):
        new_color_tuple = askcolor(self.loopcolor, self)[0]
        new_color = Color(*new_color_tuple)
        if new_color is None:  # If you press cancel
            return
        self.loopcolor = new_color
        self.loopcolor_button.config(bg=new_color.get_rgb_hex(),
                                      fg=new_color.contrasting().get_rgb_hex())

    def change_fillcolor(self):
        new_color_tuple = askcolor(self.fillcolor, self)[0]
        new_color = Color(*new_color_tuple)
        if new_color is None:  # If you press cancel
            return
        self.fillcolor = new_color
        self.fillcolor_button.config(bg=new_color.get_rgb_hex(),
                                      fg=new_color.contrasting().get_rgb_hex())

    def exit(self):
        self.master.destroy()
        self.master.quit()


def main():
    root = tk.Tk()
    app = Application(master=root)
    root.bind("<Control-c>", lambda _: (pg.quit(), app.exit(), sys.exit()))
    app.mainloop()
    return app.changed


if __name__ == "__main__":
    main()
