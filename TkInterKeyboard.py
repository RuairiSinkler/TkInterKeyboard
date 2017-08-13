import tkinter

class keyboard():

    # layout should be an array with lengths of rows
    def __init__(self, master, entry, button_width, button_height, buttons, alt_buttons=None):
        all_ok = self.check_values(buttons, alt_buttons)
        if not(all_ok):
            raise ValueError
        self.frame = tkinter.Frame(master)
        self.frame.pack()
        self.entry = entry
        self.button_width = button_width
        self.button_height = button_height
        self.buttons = buttons
        self.alt_buttons = alt_buttons

    def build(self):
        i = 0
        r = 0
        c = 0
        for row in self.buttons:
            for element in row:
                value = element
                columnspan = 1
                rowspan = 1
                width = self.button_width
                height = self.button_height
                callback = lambda v=value: self.entry.insert(tkinter.INSERT, v)
                if value == " ":
                    columnspan = 5
                    width = 5 * self.button_width
                elif value == "SHIFT":
                    print(c)
                    columnspan = 2
                    width = 2 * self.button_width
                    # callback = TODO: add shift functionality
                elif value == "ENTER":
                    columnspan = 2
                    rowspan = 2
                    width = 2 * self.button_width
                    height = 2 * self.button_height
                    # callback = TODO: add enter functionality
                elif value == "BACKSPACE":
                    columnspan = 2
                    width = 2 * self.button_width
                    callback = lambda: self.entry.delete(self.entry.index(tkinter.INSERT) - 1)
                button = tkinter.Button(self.frame, text=value, width=width, height=height, command=callback)
                button.grid(row=r, column=c, columnspan=columnspan, rowspan=rowspan)
                i = i + 1
                c = c + columnspan
            r = r + 1
            c = 0

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

def main():
    root = tkinter.Tk()
    e = tkinter.Entry(root)
    e.pack()
    buttons = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "BACKSPACE"],
               ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ENTER"],
               ["SHIFT", "z", "x", "c", "v", "b", "n", "m"],
               [" "]]
    alt_buttons = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "BACKSPACE"],
                   ["A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER"],
                   ["SHIFT", "Z", "X", "C", "V", "B", "N", "M"],
                   [" "]]
    kb = keyboard(root, e, 10, 5, buttons, alt_buttons)
    kb.build()
    root.mainloop()

if __name__ == "__main__":
    main()
