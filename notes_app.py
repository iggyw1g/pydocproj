from tkinter import *
from tkinter import filedialog

def quitapp(event=None):
    root.destroy()

def openfile():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()

        text_area.insert(1.0, content)



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

filemenu.add_command(label='Open', accelerator='Control+O', command=openfile)
filemenu.add_command(label='Save', accelerator='Control+S')

filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q', command=quitapp)
root.bind('<Control-q>', quitapp)

text_area = Text(root, wrap="word")
text_area.pack(expand=True, fill="both")

root.mainloop()
