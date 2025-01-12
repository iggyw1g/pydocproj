from tkinter import *
from tkinter import filedialog
import requests
import re
import languagemodels as lm
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.decomposition import LatentDirichletAllocation
import spacy

nlp = spacy.load("en_core_web_sm")

def quitapp(event=None):
    root.destroy()

def openfile():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        text_area.insert(1.0, content)

#def addBullet():


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

def visualize(doc):
    visual_window = Toplevel(root)
    visual_window.title("Visualization of topic")
    visual_window.geometry("1200x620+10+10")

    entities = [f"{entity.text}" for entity in doc.ents]
    texts = "\n".join(entities) if entities else "No entities found."

    label = Label(visual_window, text=texts)
    label.pack(padx=0, pady=0, fill="both", expand=True)

def start_chat(event, chat_area, messages):

    user_msg = chat_area.get()
    if user_msg.strip():
        chatbot_response = lm.do(user_msg)
        messages.config(state=NORMAL)
        messages.insert(END,f"You: {user_msg}\n")
        messages.insert(END,f"Bot: {chatbot_response}\n")
        messages.config(state=DISABLED)
        messages.see(END)
        

    chat_area.delete(0, END)
    return "break"


def chatBot():
    visual_window = Toplevel(root)
    visual_window.title("ChatBot")
    visual_window.geometry("1200x620+10+10")
    visual_window.resizable(False,False)

    messages = Text(visual_window, state=DISABLED, wrap=WORD, bg = "lightgray")
    messages.pack(fill=BOTH,expand=True)
    #chat_window.title("ChatBot")
    #chat_window.geometry("1200x620+10+10")
    #user_input = StringVar()
    chat_area = Entry(visual_window)
    chat_area.pack(fill=X)

    chat_area.bind("<Return>", lambda event: start_chat(event,chat_area, messages))



def create_non_modal_message(selected_word, definitions):
    # Create a new Toplevel window for the custom message box
    message_window = Toplevel(root)
    message_window.title(f"Definition of '{selected_word}'")
    message_window.geometry("300x200")
    
    frame = Frame(message_window)
    frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

    text_widget = Text(frame, wrap=WORD, height = 10, width = 40, state=DISABLED)
    text_widget.pack(side=LEFT, expand=True, fill=BOTH)

    label = Label(message_window, text="\n".join([f"{i+1}. {definition}" for i, definition in enumerate(definitions)]), justify=LEFT)
    label.pack(padx=10, pady=10)

    scrollbar = Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.config(state=NORMAL)
    for i, definition in enumerate(definitions):
        text_widget.insert(END, f"{i+1}. {definition}\n")
    text_widget.config(state=DISABLED)


def on_highlight_and_click(event):
    try:
        selected_word = text_area.get(SEL_FIRST, SEL_LAST).strip()
        cleaned_word = re.sub(r'[^a-zA-Z\s]', ' ', selected_word) #Getting rid of non-letters
        if cleaned_word:
            definitions = get_definition(cleaned_word)
            create_non_modal_message(cleaned_word, definitions)
    except TclError:
        pass

def getText():
    try:
        text = text_area.get("1.0", END).strip() 
        doc = nlp(text)
        visualize(doc)
    except TclError:
        pass



root = Tk()
root.title('Text Editor')
root.geometry('1200x620+10+10')
root.resizable(True, True)

menubar = Menu(root)
root.config(menu=menubar)

filemenu = Menu(menubar, tearoff=False)
formatmenu = Menu(menubar, tearoff=False)
visualizemenu = Menu(menubar, tearoff= False)

menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label="Format", menu=formatmenu)

menubar.add_command(label="Visualize", command=getText) #visualizing the subtopics
menubar.add_command(label="ChatBot", command=chatBot)


filemenu.add_command(label='Open', accelerator='Control+O', command=openfile)
filemenu.add_command(label='Save', accelerator='Control+S')

filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q', command=quitapp)
root.bind('<Control-q>', quitapp)

text_area = Text(root, wrap="word")
text_area.pack(expand=True, fill="both")

text_area.bind("<Control-r>", on_highlight_and_click)


root.mainloop()
