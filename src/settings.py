import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox

from tkcolorpicker import askcolor

from options import Options, Colours

text_tree = ET.parse('src/screen_text.xml')
root = text_tree.getroot()


def get_text(name):
    return root.find('./settings/{}'.format(name)).get(Options.language)


class Application(tk.Frame):
    """
    A settings window with tkinter
    Grid:
             0       1
        ---------|--------|
    0         Settings
    1       mute | not log
    2    no zmbs | debug
    3          m | f
    4        nor | eng
    5        FPS | FPS Entry
    6        Map | Map Entry
    7   Tile len | Tile len slider
    8     volume | volume slider
    9        Div by 12
    10    Commit | Discard
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        master.title(get_text('header'))
        master.protocol('WM_DELETE_WINDOW', self.exit)
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.changed = False
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=get_text('header'),
                 font='helvetica 12 bold', justify='center').grid(
                     column=0, row=0, columnspan=2, sticky='nwneswse')
        self.flags()
        self.labels()
        self.gender_radio_buttons()
        self.language_radio_buttons()
        self.fps_entry()
        self.map_dropdown()
        self.volume_slider()
        self.tile_length_slider()
        self.tile_length_nearest12()
        self.colour_picker()
        tk.Button(self, text=get_text('discard'),
                  fg='red', command=self.exit).grid(
                      column=1, row=11, sticky='nwneswse')
        tk.Button(self, text=get_text('commit'),
                  command=self.commit).grid(column=0, row=11, sticky='nwneswse')

    def commit(self):
        if (Options.mapname != self.map.get() or
                Options.tile_length != int(self.tile_length.get()) or
                Options.language != self.language.get()):
            self.changed = True
        Options.fps = int(self.FPS.get())
        Options.mapname = self.map.get()
        Options.volume = float(self.volume.get())
        Options.mute = self.is_mute.get()
        Options.tile_length = int(self.tile_length.get())
        Options.gender = self.gender.get()
        Options.not_log = self.is_not_log.get()
        Options.no_zombies = self.is_no_zmbs.get()
        Options.debug = self.is_debug.get()
        Options.language = self.language.get()
        Options.loopcolour = self.loopcolour
        Options.fillcolour = self.fillcolour
        try:
            Options.assertions()
        except AssertionError as e:
            messagebox.showwarning('Error', e)
        else:
            try:
                Options.warnings()
            except AssertionError as e:
                if messagebox.askyesno('warning', str(e) + '\nVil du fortsette?'):
                    self.exit()
                else:
                    return
            else:
                self.exit()

    def flags(self):
        self.is_mute, self.is_not_log = tk.BooleanVar(None, Options.mute), tk.BooleanVar(None, Options.not_log)
        self.is_no_zmbs, self.is_debug = tk.BooleanVar(None, Options.no_zombies), tk.BooleanVar(None, Options.debug)
        variables = 'is_mute', 'is_not_log', 'is_no_zmbs', 'is_debug'
        texts = (get_text(s) for s in (
                 'mute', 'not_log', 'no_zombies', 'debug'))
        grids = (0, 1), (1, 1), (0, 2), (1, 2)
        for var, text, grid in zip(variables, texts, grids):
            button = tk.Checkbutton(self, text=text, variable=getattr(self, var))
            button.grid(column=grid[0], row=grid[1], sticky='nwneswse')

    def labels(self):
        texts = (get_text(s) for s in (
                 'fps', 'map', 'tile_length', 'volume'))
        for text, row in zip(texts, range(5, 9)):
            tk.Label(self, text=text, anchor='e').grid(column=0, row=row, sticky='nwneswse')

    def gender_radio_buttons(self):
        self.gender = tk.StringVar(None, Options.gender)
        self.male_b = tk.Radiobutton(self, text=get_text('male'),
                                     value='m', variable=self.gender)
        self.male_b.grid(column=0, row=3, sticky='nwneswse')
        self.female_b = tk.Radiobutton(self, text=get_text('female'),
                                       value='f', variable=self.gender)
        self.female_b.grid(column=1, row=3, sticky='nwneswse')
    
    def language_radio_buttons(self):
        self.language = tk.StringVar(None, Options.language)
        self.norwegian_b = tk.Radiobutton(self, text=get_text('norwegian'),
                                          value='norsk', variable=self.language)
        self.norwegian_b.grid(column=0, row=4, sticky='nwneswse')
        self.english_b = tk.Radiobutton(self, text=get_text('english'),
                                        value='english', variable=self.language)
        self.english_b.grid(column=1, row=4, sticky='nwneswse')

    def fps_entry(self):
        self.FPS = tk.Entry(self)
        self.FPS.insert(0, Options.fps)
        self.FPS.grid(column=1, row=5, sticky='nwneswse')

    def map_dropdown(self):
        options = os.listdir('assets/Maps/')
        self.map = tk.StringVar(self, Options.mapname)
        self.dropdown = tk.OptionMenu(self, self.map, *options)
        self.dropdown.grid(column=1, row=6, sticky='nwneswse')

    def volume_slider(self):
        self.volume = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.05)
        self.volume.set(Options.volume)
        self.volume.grid(column=1, row=8, sticky='nwneswse')

    def tile_length_slider(self):
        self.tile_length = tk.Scale(self, from_=12, to=100, orient=tk.HORIZONTAL)
        self.tile_length.set(Options.tile_length)
        self.tile_length.grid(column=1, row=7, sticky='nwneswse')

    def tile_length_nearest12(self):
        self.tile_length_button = tk.Button(self, text=get_text('div12'),
                                            command=self.tl_button_command)
        self.tile_length_button.grid(column=0, row=9, columnspan=2, sticky='nwneswse')

    def tl_button_command(self):
        curr_tile_length = int(self.tile_length.get())
        tl_mod12 = curr_tile_length % 12
        if tl_mod12 <= 6:
            self.tile_length.set(curr_tile_length - tl_mod12)
        else:
            self.tile_length.set(curr_tile_length + 12 - tl_mod12)

    def colour_picker(self):
        self.loopcolour, self.fillcolour = Options.loopcolour, Options.fillcolour
        self.loopcolour_button = tk.Button(self, text=get_text('loopcolour'),
                                      command=self.change_loopcolour, bg=Colours.get_hex(self.loopcolour))
        self.loopcolour_button.grid(column=0, row=10, sticky='nwneswse')
        self.fillcolour_button = tk.Button(self, text=get_text('fillcolour'),
                                      command=self.change_fillcolour, bg=Colours.get_hex(self.fillcolour))
        self.fillcolour_button.grid(column=1, row=10, sticky='nwneswse')

    def change_loopcolour(self):
        new_colour = askcolor(self.loopcolour, self)[0]
        if new_colour is None:  # If you press cancel
            return
        self.loopcolour = new_colour
        self.loopcolour_button.config(bg=Colours.get_hex(new_colour),
                                      fg=Colours.contrasting(*new_colour))

    def change_fillcolour(self):
        new_colour = askcolor(self.fillcolour, self)[0]
        if new_colour is None:  # If you press cancel
            return
        self.fillcolour = new_colour
        self.fillcolour_button.config(bg=Colours.get_hex(new_colour),
                                      fg=Colours.contrasting(*new_colour))

    def exit(self):
        self.master.destroy()
        self.master.quit()


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    return app.changed


if __name__ == '__main__':
    main()
