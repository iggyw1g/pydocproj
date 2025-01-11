from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import requests


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

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        definitions = [
            meaning["definitions"][0]["definition"]
            for meaning in data[0]["meanings"]
        ]

        return definitions
    else:
        return [f"Error: Unable to find the word '{word}'"]
    

def on_highlight_and_click(event):
    try:
        selected_word = text_area.get(SEL_FIRST, SEL_LAST).strip()
        if selected_word:
            definitions = get_definition(selected_word)
            messagebox.showinfo(
                f"Definition of '{selected_word}'",
                "\n".join([f"{i+1}. {definition}" for i, definition in enumerate(definitions)]),
            )
    except TclError:
        pass
                

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
text_area.bind("<ButtonRelease-1>", on_highlight_and_click)


root.mainloop()
