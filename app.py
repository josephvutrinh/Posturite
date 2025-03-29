import tkinter as tk
from PIL import Image, ImageTk

class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posturite")
        self.geometry("1000x700")
        self.state("zoomed")  # Makes the window start maximized
        self.resizable(True, True)

        self.frames = {}

        for F in (HomePage, AboutPage, ContactPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load and scale background image
        self.bg_image = Image.open("Hoohacks-7.jpg").resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas to layer background and text
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Background image
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        # Title (top left)
        self.canvas.create_text(40, 35, text="Posturite", fill="white",
                                font=("Helvetica", 20, "bold"), anchor="w")

        # Navigation items — manually position with custom X values
        self.nav_items = {
            "Home": self.canvas.create_text(630, 35, text="Home", fill="white",
                                            font=("Helvetica", 14, "bold"), anchor="w"),
            "About": self.canvas.create_text(730, 35, text="About", fill="white",
                                             font=("Helvetica", 14, "bold"), anchor="w"),
            "Contact": self.canvas.create_text(830, 35, text="Contact", fill="white",
                                               font=("Helvetica", 14, "bold"), anchor="w"),
            "Settings": self.canvas.create_text(1420, 35, text="Settings", fill="white",
                                                font=("Helvetica", 14, "bold"), anchor="w"),
        }

        # Click bindings
        self.canvas.tag_bind(self.nav_items["Home"], "<Button-1>", lambda e: controller.show_frame("HomePage"))
        self.canvas.tag_bind(self.nav_items["About"], "<Button-1>", lambda e: controller.show_frame("AboutPage"))
        self.canvas.tag_bind(self.nav_items["Contact"], "<Button-1>", lambda e: controller.show_frame("ContactPage"))
        self.canvas.tag_bind(self.nav_items["Settings"], "<Button-1>", lambda e: controller.show_frame("SettingsPage"))

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="About Page", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack()

class ContactPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Contact Page", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack()

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Settings Page", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack()

if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()
