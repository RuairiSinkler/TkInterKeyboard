import tkinter

class keyboard():

    # layout should be an array with lengths of rows
    def __init__(self, master, entry, button_width, button_height, buttons, alt_buttons=None, enter_function=None):
        all_ok = self.check_values(buttons, alt_buttons)
        if not(all_ok):
            raise ValueError
        self.frame = tkinter.Frame(master)
        self.frame.pack()
        self.entry = entry
        self.button_width = button_width
        self.button_height = button_height
        self.button_values = []
        self.buttons = buttons
        self.alt_buttons = alt_buttons
        self.enter_function = enter_function
        self.shift = False
        self.caps_lock = False

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
                    elif name == "CAPS_LOCK":
                        callback = lambda: self.toggle_caps_lock()
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
                        callback = lambda: self.entry.delete(self.entry.index(tkinter.INSERT) - 1)
                    button = tkinter.Button(self.frame, textvariable=value, width=width, height=height, command=callback)
                    button.grid(row=r, column=c, columnspan=columnspan, rowspan=rowspan)
                i = i + 1
                c = c + columnspan
            r = r + 1
            c = 0

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
        if self.shift != self.caps_lock:
            values = self.alt_buttons
        else:
            values = self.buttons
        i = 0
        for row in values:
            for element in row:
                self.button_values[i].set(element)
                i = i + 1

    def toggle_caps_lock(self):
        self.caps_lock = not(self.caps_lock)
        self.refresh_vars()

    def toggle_shift(self):
        self.shift = not(self.shift)
        self.refresh_vars()

    def set_entry(self, entry):
        self.entry = entry

def main():
    root = tkinter.Tk()
    e = tkinter.Entry(root)
    e.pack()
    buttons = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "BACKSPACE"],
               ["CAPS_LOCK", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ENTER"],
               ["SHIFT", "z", "x", "c", "v", "b", "n", "m"],
               ["BLANK", "BLANK", "BLANK", "SPACE"]]
    alt_buttons = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "BACKSPACE"],
                   ["CAPS_LOCK", "A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER"],
                   ["SHIFT", "Z", "X", "C", "V", "B", "N", "M"],
                   ["BLANK", "BLANK", "BLANK", "SPACE"]]
    enter_function = lambda: print("enter")
    kb = keyboard(root, e, 10, 5, buttons, alt_buttons, enter_function)
    kb.build()
    root.mainloop()

if __name__ == "__main__":
    main()
