from tkinter import *

root = Tk()
root.title('Text Editor')
root.geometry('1200x620+10+10')
root.resizable(False, False)
menubar = Menu(root)
#root.config(menu=menubar)
root.config(menu=menubar)

filemenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='File',menu=filemenu)
#menubar.add_cascade(label='Save', menu=filemenu)

filemenu.add_command(label='Open', accelerator='Control+O')
filemenu.add_command(label='Save', accelerator='Control+S')

filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q')
root.mainloop()
