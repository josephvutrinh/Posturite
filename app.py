import tkinter as tk
from PIL import Image, ImageTk

class PosturiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posturite")
        self.geometry("1000x700")
        self.resizable(False, False)  # Disable resizing

        # Load and store original background image
        self.bg_image = Image.open("Hoohacks-7.jpg")
        self.original_bg = self.bg_image.copy()

        # Canvas for background + title
        self.canvas = tk.Canvas(self, width=1000, height=700, highlightthickness=0)
        self.canvas.pack()

        # Initial background
        self.bg_photo = ImageTk.PhotoImage(self.original_bg.resize((1000, 700)))
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        # Title (top-left)
        self.title_text = self.canvas.create_text(40, 35, text="Posturite", fill="white",
                                                  font=("Helvetica", 20, "bold"), anchor="w")

if __name__ == "__main__":
    app = PosturiteApp()
    app.mainloop()

