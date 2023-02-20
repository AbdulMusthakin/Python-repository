import tkinter

# Create the main window.
main_window = tkinter.Tk()

# Create a label widget containing the text "Hello World".
label = tkinter.Label(main_window, text="Hello World", font=("Arial", 72))

# Pack the label.
label.pack()

# Enter the tkinter main loop.
tkinter.mainloop()
