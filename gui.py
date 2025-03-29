import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk

class PostureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Posturite")
        self.root.geometry("800x600")

        #Implement bg
        bg = ImageTk.PhotoImage(file="images/Hoohacks-7.png")
        background_label = tk.Label(root, image=bg)
        background_label.image = bg
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        ##Implement buttons
        homeButton = tk.Button(
            root, text="Home"
        )
        aboutButton = tk.Button(
            root,
            text="About",
            background='#f8796a',
            foreground="white",
            activebackground='#ea786d',
            activeforeground="white",
            borderwidth = 0,
            cursor='hand2'
        )
        contactButton = tk.Button(
            root, text="Contact"
        )
        settingsButton = tk.Button(
            root, text="Settings"
        )

        aboutButton.place(relx=0.5, rely=0.5, anchor="center")


        self.cap = None
        self.running = False

    ## Function for clicking home and logo
    ##def on_home(self):

    ## Function for closing app
    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PostureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
