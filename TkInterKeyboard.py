import tkinter
from tkinter import font

class keyboard():

    DEFAULT_WIDTH = 8
    DEFAULT_HEIGHT = 3
    DEFAULT_BACKGROUND = "gray"
    DEFAULT_FOREGROUND = "white"
    DEFAULT_ACTIVE_BACKGROUND = "light gray"
    DEFAULT_ACTIVE_FOREGROUND = "white"
    DEFAULT_FONT = "DejaVuSans"
    DEFAULT_FONT_SIZE = 12

    def __init__(self, root, master, entry, buttons, alt_buttons=None, enter_function=None, **cnf):
        all_ok = self.check_values(buttons, alt_buttons)
        if not(all_ok):
            raise ValueError
        self.frame = tkinter.Frame(master)
        self.frame.pack()
        self.entry = entry
        self.keys = {}
        self.button_values = []
        self.buttons = buttons
        self.alt_buttons = alt_buttons
        self.enter_function = enter_function
        self.shift = False
        self.caps_lock = False
        self.button_width = cnf.get("button_width", self.DEFAULT_WIDTH)
        self.button_height = cnf.get("button_height", self.DEFAULT_HEIGHT)
        self.background = cnf.get("background", self.DEFAULT_BACKGROUND)
        self.foreground = cnf.get("foreground", self.DEFAULT_FOREGROUND)
        self.active_background = cnf.get("active_background", self.DEFAULT_ACTIVE_BACKGROUND)
        self.active_foreground = cnf.get("active_foreground", self.DEFAULT_ACTIVE_FOREGROUND)
        self.font = font.Font(family=cnf.get("font", self.DEFAULT_FONT),
                                      size=cnf.get("font_size", self.DEFAULT_FONT_SIZE))

    def build(self):
        i = 0
        r = 0
        c = 0
        for row in self.buttons:
            for element in row:
                value = tkinter.StringVar()
                value.set(element)
                self.button_values.append(value)
                name = value.get()
                columnspan = 1
                rowspan = 1
                wraplength = 0
                width = self.button_width
                height = self.button_height
                if name == "BLANK":
                    frame = tkinter.Frame(self.frame, width=1, height=1)
                    frame.grid(row=r, column=c, columnspan=columnspan, rowspan=rowspan)
                else:
                    callback = lambda v=value: self.key_press(v)
                    if name == "SPACE":
                        value.set(" ")
                        columnspan = 5
                        width = 5 * self.button_width
                    elif name == "CAPS LOCK":
                        callback = lambda: self.toggle_caps_lock()
                        wraplength = 50
                    elif name == "SHIFT":
                        columnspan = 2
                        width = 2 * self.button_width
                        callback = lambda: self.toggle_shift()
                    elif name == "ENTER":
                        columnspan = 2
                        rowspan = 2
                        width = 2 * self.button_width
                        height = 2 * self.button_height
                        if self.enter_function is None:
                            callback = self.enter_function
                        else:
                            callback = lambda: self.enter_function()
                    elif name == "BACKSPACE":
                        columnspan = 2
                        width = 2 * self.button_width
                        callback = lambda: self.delete()
                    button = tkinter.Button(self.frame, textvariable=value, width=width, height=height, command=callback,
                                            background=self.background, foreground=self.foreground,
                                            activebackground=self.active_background,
                                            activeforeground=self.active_foreground, font=self.font, wraplength=wraplength)
                    button.grid(row=r, column=c, columnspan=columnspan, rowspan=rowspan)
                    self.keys[name] = button
                i = i + 1
                c = c + columnspan
            r = r + 1
            c = 0

    def delete(self):
        if isinstance(self.entry, tkinter.Entry):
            self.entry.delete(self.entry.index(tkinter.INSERT) - 1)
        elif isinstance(self.entry, tkinter.Text):
            self.entry.delete("%s-1c" % tkinter.INSERT, tkinter.INSERT)

    def key_press(self, value):
        self.entry.insert(tkinter.INSERT, value.get())
        if self.shift:
            self.toggle_shift()

    def check_values(self, buttons, alt_buttons):
        if not (alt_buttons is None):
            for i in range(len(buttons)):
                for j in range(len(buttons[i])):
                    if not(isinstance(buttons[i][j], str)):
                        return False
                    try:
                        if not (isinstance(alt_buttons[i][j], str)):
                            return False
                    except IndexError:
                        print("TkInterKeyboard.py: buttons and alt_buttons do not match up")
                        raise
        else:
            for i in range(len(buttons)):
                for j in range(len(buttons[i])):
                    if not(isinstance(buttons[i][j], str)):
                        return False
        return True

    def refresh_vars(self):
        values = self.buttons
        # If shift or Caps Lock are active (but not both) then use alt buttons, if they exist
        if self.shift != self.caps_lock and not(self.alt_buttons is None):
            values = self.alt_buttons
        i = 0
        for row in values:
            for element in row:
                self.button_values[i].set(element)
                i = i + 1

    def toggle_caps_lock(self):
        self.caps_lock = not(self.caps_lock)
        if self.caps_lock:
            self.keys.get("CAPS LOCK").config(background=self.active_background, activebackground=self.background,
                                              foreground=self.active_foreground, activeforeground=self.foreground)
        else:
            self.keys.get("CAPS LOCK").config(background=self.background, activebackground=self.active_background,
                                              foreground=self.foreground, activeforeground=self.active_foreground)
        self.refresh_vars()

    def toggle_shift(self):
        self.shift = not(self.shift)
        if self.shift:
            self.keys.get("SHIFT").config(background=self.active_background, activebackground=self.background,
                                          foreground=self.active_foreground, activeforeground=self.foreground)
        else:
            self.keys.get("SHIFT").config(background=self.background, activebackground=self.active_background,
                                          foreground=self.foreground, activeforeground=self.active_foreground)
        self.refresh_vars()

    def set_entry(self, entry):
        self.entry = entry

# Example code used for testing, creates a basic keyboard with an entry box to work with
def main():
    root = tkinter.Tk()
    e = tkinter.Entry(root)
    e.pack()
    buttons = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "BACKSPACE"],
               ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "ENTER"],
               ["CAPS LOCK", "a", "s", "d", "f", "g", "h", "j", "k", "l"],
               ["SHIFT", "z", "x", "c", "v", "b", "n", "m", ",", "."],
               ["BLANK", "BLANK", "BLANK", "SPACE"]]
    alt_buttons = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "BACKSPACE"],
                   ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "ENTER"],
                   ["CAPS LOCK", "A", "S", "D", "F", "G", "H", "J", "K", "L"],
                   ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", "."],
                   ["BLANK", "BLANK", "BLANK", "SPACE"]]
    enter_function = lambda: print("enter")
    kb = keyboard(root, root, e, buttons, alt_buttons, enter_function)
    kb.build()
    root.mainloop()

if __name__ == "__main__":
    main()
