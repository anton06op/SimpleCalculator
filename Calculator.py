from tkinter import *
from math import *


def setwindow(rt):
    rt.title("Calculator")
    rt.resizable(False, False)

    w = rt.winfo_reqwidth()
    ws = rt.winfo_screenwidth()
    cx = int(ws / 2.25 - w / 2.25)
    cy = 0

    rt.geometry("+{0}+{1}".format(cx, cy))


def settheme():
    global light_theme
    if light_theme:
        root["bg"] = colors['light_bg']
        display.configure(readonlybackground=colors['light_bg'], fg=colors['light_txt'])
        mini_display.configure(bg=colors['light_bg'], fg=colors['light_minilbl'])
        for btn in button_arr:
            if btn['text'] == '\u263C':
                btn.configure(image=buttonimage)
            btn.configure(bg=colors['light_btn'], activebackground=colors['light_activebtn'],
                          activeforeground=colors['light_txt'], fg=colors['light_txt'])
        light_theme = False
    else:
        root["bg"] = colors['dark_bg']
        display.configure(readonlybackground=colors['dark_bg'], fg=colors['dark_txt'])
        mini_display.configure(bg=colors['dark_bg'], fg=colors['dark_minilbl'])
        for btn in button_arr:
            if btn['text'] == '\u263C':
                btn.configure(image=buttonimagered)
            btn.configure(bg=colors['dark_btn'], activebackground=colors['dark_activebtn'],
                          activeforeground=colors['dark_txt'], fg=colors['dark_txt'])
        light_theme = True


def calculate(number):
    global result
    global lastcommand
    global entry_text

    if lastcommand == '+':
        result += number
    elif lastcommand == '-':
        result -= number
    elif lastcommand == '/':
        try:
            result /= number
        except ZeroDivisionError:
            pass
    elif lastcommand == '*':
        result *= number
    elif lastcommand == '\u2093\u02B8':
        try:
            result **= number
        except OverflowError:
            pass
    elif lastcommand == '=':
        result = number

    if str(result).endswith('.0'):
        result = int(result)

    entry_text.set(round(result, 15))


def click(text):
    global start
    global mini_display
    global result
    global lastcommand
    global entry_text

    if text.isdigit() or text == '.':
        if start:
            if text != '.':
                entry_text.set('')
                start = False
            else:
                entry_text.set('0.')
                start = False
        if text != '.' or entry_text.get().find('.') == -1:
            if len(entry_text.get()) < 13:
                entry_text.set(entry_text.get() + text)

    elif text in ['+/-', '\u221A', 'C', '\u232B', 'pi', '\u215F\u2093', '\u263C']:
        if text == '\u232B':
            if not start:
                if len(entry_text.get()) > 1:
                    entry_text.set(entry_text.get()[:-1])
                else:
                    entry_text.set('0')
                    start = True
        if text == 'C':
            start = True
            lastcommand = '='
            result = 0
            entry_text.set(str(result))
            mini_display.configure(text=lastcommand)
        if text == '+/-':
            if not start:
                if entry_text.get().find('-') == -1:
                    entry_text.set('-' + entry_text.get())
                else:
                    entry_text.set(entry_text.get()[1:])
        if text == 'pi':
            start = False
            entry_text.set(str(pi))
        if text == '\u215F\u2093':
            if float(entry_text.get()) != 0:
                start = False
                entry_text.set(str(round(1 / float(entry_text.get()), 15)))
        if text == '\u221A':
            start = False
            entry_text.set(str(round(sqrt(float(entry_text.get())), 15)))
        if text == '\u263C':
            settheme()

    else:
        if start:
            lastcommand = text
        else:
            calculate(int(entry_text.get())) if entry_text.get().isdigit() else calculate(float(entry_text.get()))

            lastcommand = text
            start = True
        mini_display.configure(text=lastcommand)


def handlerkeyclick(event):
    text = ''
    if event.char:
        if event.char == '\x08':
            text = '\u232B'
        if event.char == '\r':
            text = '='
        if event.char in '+-*/=.':
            text = event.char
        if event.char.isdigit():
            text = event.char
        if event.char in 'CcСс':
            text = 'C'
    if text != '':
        click(text)


start = True
lastcommand = '='
result = 0
light_theme = True

colors = {'light_bg': '#ddd',
          'light_btn': '#ccc',
          'light_activebtn': '#aaa',
          'light_minilbl': '#999',
          'light_txt': '#000',
          'dark_bg': '#333',
          'dark_btn': '#222',
          'dark_activebtn': '#111',
          'dark_minilbl': '#666',
          'dark_txt': '#c00'}

buttons = (('+/-', '\u221A', 'C', '\u232B'),
           ('pi', '\u215F\u2093', '\u2093\u02B8', '/'),
           ('7', '8', '9', '*'),
           ('4', '5', '6', '-'),
           ('1', '2', '3', '+'),
           ('\u263C', '0', '.', '='))

root = Tk()
setwindow(root)

buttonimage = PhotoImage(file="day-night.png")
buttonimage = buttonimage.subsample(2, 2)
buttonimagered = PhotoImage(file="day-night-red.png")
buttonimagered = buttonimagered.subsample(2, 2)

mini_display = Label(root, text='=', font="Tahoma 14", bd=10)

entry_text = StringVar()
display = Entry(root, font="Tahoma 28", state="readonly", textvariable=entry_text, justify="center", bd=1)
entry_text.set("0")

mini_display.grid(row=0, column=0, columnspan=4, sticky="nw")
display.grid(row=1, column=0, columnspan=4, pady=5, padx=6, ipadx=5)

button_arr = []

for row in range(len(buttons)):
    for column in range(len(buttons[0])):
        if buttons[row][column] == '\u263C':
            button = Button(root, text=buttons[row][column], width=3, font="Tahoma 20", image=buttonimage,
                            command=lambda text=buttons[row][column]: click(text))
        else:
            button = Button(root, text=buttons[row][column], width=3, font="Tahoma 20",
                            command=lambda text=buttons[row][column]: click(text))
        button_arr.append(button)
        button.grid(row=row+2, column=column, padx=5, pady=5, ipadx=15, ipady=15, sticky="nsew")

root.bind("<Key>", handlerkeyclick)
settheme()

root.mainloop()
