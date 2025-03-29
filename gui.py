import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk

class PostureApp:
    print("Script is running...")

    def __init__(self, root):
        self.root = root
        self.root.title("Posture Checker")
        self.root.geometry("800x600")

        self.label = Label(self.root)
        self.label.pack()

        self.status_label = Label(self.root, text="Posture: Waiting...", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.start_btn = Button(self.root, text="Start Camera", command=self.start_camera)
        self.start_btn.pack()

        self.cap = None
        self.running = False

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_frame()

    def update_frame(self):
        if self.cap and self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)

                # TODO: Add AI analysis here later
                self.status_label.config(text="Posture: Good ✅")  # Temporary placeholder

            self.label.after(10, self.update_frame)

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
