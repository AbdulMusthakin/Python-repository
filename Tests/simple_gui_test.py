import tkinter

# How would I have my text rpg game run in a window?
# I would need to create a window, and then have the game run in that window.
# I would need to create a window, and then have the game run in that window.


class Display:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Text RPG")
        self.root.geometry("800x600")
        self.root.resizable()

        tkinter.Label(self.root, text="Welcome to the game!").pack()
        tkinter.Button(self.root, text="Start Game").pack()
        tkinter.Button(self.root, text="Load Game").pack()
        tkinter.Button(self.root, text="Options").pack()
        tkinter.Button(self.root, text="Quit").pack()
