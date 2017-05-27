#!/usr/bin/env python

import tkinter as tk

from scripts.generate import generate_secret


class Application(tk.Tk):

    MODES = [
        ("Words", "Words"),
        ("Numbers", "Numbers"),
        ("Mixed", "Mixed"),
    ]

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.grid()
        self._create_message()
        self._create_buttons()

    def _create_buttons(self):

        quit_button = tk.Button(self, text='Quit', command=self.quit)
        generate_btn = tk.Button(self, text='Generate',
                                 command=generate_secret)

        v = tk.StringVar()
        v.set("Words")

        def _sel():
            label = tk.Label()
            selection = "You selected {0} type. Click Generate".format(
                str(v.get())
            )
            label.config(text=selection)

        for text, mode in self.MODES:

            b = tk.Radiobutton(self, text=text,
                               variable=v, value=mode, command=_sel)
            b.pack(anchor=tk.CENTER)

        quit_button.pack(anchor=tk.SW)
        generate_btn.pack(anchor=tk.SE)

    def _create_message(self):

        text = "Select a secret type. For the `words` type, select the " \
               "the number of dice and how many rolls."
        m = tk.Message(self, text=text)
        m.pack(anchor=tk.N)


app = Application()
app.call('wm', 'iconphoto', app._w, tk.PhotoImage(file='lock_icon_bkgrd.png'))
app.title('Password Generator')
app.geometry('{}x{}'.format(500, 300))
app.mainloop()
