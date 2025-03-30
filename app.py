import tkinter as tk
from PIL import Image, ImageTk
import cv2
from posture_detector import PostureDetector

class PosturiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posturite")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.detector = PostureDetector()

        # Load and resize background
        self.bg_image = Image.open("Hoohacks-7.jpg").resize((1000, 700))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas
        self.canvas = tk.Canvas(self, width=1000, height=700, highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        self.canvas.pack()

        # Title (top-left)
        self.title_text = self.canvas.create_text(40, 35, text="Posturite", fill="white",
                                                  font=("Helvetica", 20, "bold"), anchor="w")

        # Settings (top-right)
        self.settings_text = self.canvas.create_text(920, 35, text="Settings", fill="white",
                                                     font=("Helvetica", 14, "bold"), anchor="w")

        # Dropdown menu for Settings
        self.dropdown = tk.Frame(self, bg="#1e1e1e", highlightbackground="white", highlightthickness=1)
        self.dropdown.place(x=850, y=50, width=130, height=60)
        self.dropdown.lower()

        self.lockdown_var = tk.BooleanVar()
        label = tk.Label(self.dropdown, text="Lockdown Mode", bg="#1e1e1e", fg="white", font=("Helvetica", 10))
        label.pack(side="left", padx=(10, 5), pady=10)

        self.toggle = tk.Checkbutton(self.dropdown, variable=self.lockdown_var, bg="#1e1e1e",
                                     activebackground="#1e1e1e", fg="white", selectcolor="#1e1e1e",
                                     highlightthickness=0, bd=0, command=self.on_lockdown_toggle)
        self.toggle.pack(side="right", padx=(5, 10))

        self.canvas.tag_bind(self.settings_text, "<Enter>", self.show_dropdown)
        self.canvas.tag_bind(self.settings_text, "<Leave>", self.hide_dropdown_delayed)
        self.dropdown.bind("<Enter>", self.cancel_hide)
        self.dropdown.bind("<Leave>", self.hide_dropdown_delayed)

        self._hide_timer = None

        # Rounded rectangle button with text
        self.start_button_shape = self.create_rounded_rect(400, 200, 600, 240, radius=20,
                                                           fill="#c0392b", outline="")
        self.start_button_text = self.canvas.create_text(500, 220, text="Start Session", fill="white",
                                                         font=("Helvetica", 12, "bold"), anchor="center")

        self.canvas.tag_bind(self.start_button_shape, "<Button-1>", lambda e: self.start_session())
        self.canvas.tag_bind(self.start_button_text, "<Button-1>", lambda e: self.start_session())

        # Webcam placeholder
        self.video_frame = tk.Label(self)
        self.video_frame.place_forget()

        # End Session button
        self.end_button = tk.Button(self, text="End Session", font=("Helvetica", 10),
                                    command=self.end_session, bg="white")
        self.end_button.place_forget()

        # Camera control
        self.cap = None
        self.running = False

    def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

        # Warning Text Label (Centered)
        self.warning_label = tk.Label(self, text="", font=("Helvetica", 24, "bold"), fg="white", bg="black")
        self.warning_label.place(relx=0.5, y=90, anchor="center")

        # Hide initially
        self.warning_label.place_forget()

    def start_session(self):
        self.canvas.itemconfig(self.start_button_shape, state="hidden")
        self.canvas.itemconfig(self.start_button_text, state="hidden")
        self.dropdown.lower()

        self.video_frame.place(x=150, y=120, width=700, height=375)
        self.end_button.place(x=450, y=520)

        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.show_frame()

    def show_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (700, 375))
                frame = cv2.flip(frame, 1)  # Flip for mirror effect

                # Apply Posture Detection on frame
                frame = self.detector.findPose(frame)  # Draw pose landmarks
                lmList = self.detector.findPosition(frame)  # Get positions

                # Detect if user has forward head posture
                if self.detector.detectForwardHead(lmList):
                    warning_text = "⚠️ Forward Head Detected!"
                    self.warning_label.config(text=warning_text, fg="red")
                else:
                    self.warning_label.config(text="Good Posture", fg="green")

                self.warning_label.place(relx=0.5, y=90, anchor="center")
                self.warning_label.update_idletasks()

                # Convert processed frame for Tkinter
                frame = cv2.resize(frame, (700, 375))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_frame.imgtk = imgtk
                self.video_frame.configure(image=imgtk)

            self.after(10, self.show_frame)

    def end_session(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_frame.place_forget()
        self.end_button.place_forget()
        self.canvas.itemconfig(self.start_button_shape, state="normal")
        self.canvas.itemconfig(self.start_button_text, state="normal")

        self.warning_label.config(text="")
        self.warning_label.place_forget()

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
