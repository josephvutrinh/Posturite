import tkinter as tk
from PIL import Image, ImageTk

class PosturiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posturite")
        self.geometry("1000x700")
        self.resizable(False, False)

        # Load and resize background
        self.bg_image = Image.open("Hoohacks-7.jpg").resize((1000, 700))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas and place background image
        self.canvas = tk.Canvas(self, width=1000, height=700, highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        self.canvas.pack()


        # Settings label (top-right)
        self.settings_text = self.canvas.create_text(920, 35, text="Settings", fill="white",
                                                     font=("Helvetica", 14, "bold"), anchor="w")

        # Dropdown settings panel (initially hidden)
        self.dropdown = tk.Frame(self, bg="#1e1e1e", highlightbackground="white", highlightthickness=1)
        self.dropdown.place(x=850, y=50, width=130, height=60)
        self.dropdown.lower()

        # Lockdown Mode toggle
        self.lockdown_var = tk.BooleanVar()

        label = tk.Label(self.dropdown, text="Lockdown Mode", bg="#1e1e1e", fg="white", font=("Helvetica", 10))
        label.pack(side="left", padx=(10, 5), pady=10)

        self.toggle = tk.Checkbutton(self.dropdown, variable=self.lockdown_var, bg="#1e1e1e",
                                     activebackground="#1e1e1e", fg="white", selectcolor="#1e1e1e",
                                     highlightthickness=0, bd=0, command=self.on_lockdown_toggle)
        self.toggle.pack(side="right", padx=(5, 10))

        # Bind hover behavior to show/hide dropdown
        self.canvas.tag_bind(self.settings_text, "<Enter>", self.show_dropdown)
        self.canvas.tag_bind(self.settings_text, "<Leave>", self.hide_dropdown_delayed)
        self.dropdown.bind("<Enter>", self.cancel_hide)
        self.dropdown.bind("<Leave>", self.hide_dropdown_delayed)

        self._hide_timer = None
        print("App launched from app.py ✅")

    def show_dropdown(self, event=None):
        self.dropdown.lift()
        self.dropdown.place(x=850, y=50)

    def hide_dropdown_delayed(self, event=None):
        if self._hide_timer:
            self.after_cancel(self._hide_timer)
        self._hide_timer = self.after(300, self.hide_dropdown)

    def cancel_hide(self, event=None):
        if self._hide_timer:
            self.after_cancel(self._hide_timer)
            self._hide_timer = None

    def hide_dropdown(self):
        self.dropdown.lower()

    def on_lockdown_toggle(self):
        state = self.lockdown_var.get()
        print("Lockdown Mode is", "ON" if state else "OFF")

if __name__ == "__main__":
    app = PosturiteApp()
    app.mainloop()
