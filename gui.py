import tkinter as tk
from tkinter import Label, Button, messagebox
import cv2
from PIL import Image, ImageTk

class PostureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Posture Checker")
        self.root.geometry("800x700")
        self.root.configure(bg="#f9f9f9")

        # Posture label
        self.status_label = Label(root, text="Posture: Waiting...", font=("Arial", 16), bg="#f9f9f9")
        self.status_label.pack(pady=10)

        # Buttons Frame
        self.buttons_frame = tk.Frame(root, bg="#f9f9f9")
        self.buttons_frame.pack()

        self.start_btn = Button(self.buttons_frame, text="▶ Start Camera", command=self.start_camera, width=15)
        self.start_btn.grid(row=0, column=0, padx=10, pady=5)

        self.stop_btn = Button(self.buttons_frame, text="⏹ Stop Camera", command=self.stop_camera, width=15)
        self.stop_btn.grid(row=0, column=1, padx=10, pady=5)

        self.tips_btn = Button(self.buttons_frame, text="💡 Tips", command=self.show_tips, width=15)
        self.tips_btn.grid(row=0, column=2, padx=10, pady=5)

        self.history_btn = Button(self.buttons_frame, text="📜 History", command=self.show_history, width=15)
        self.history_btn.grid(row=0, column=3, padx=10, pady=5)

        # Webcam display
        self.image_label = Label(root)
        self.image_label.pack(pady=10)

        # Camera + logic
        self.cap = None
        self.running = False
        self.history = []

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_frame()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.image_label.config(image="")  # Clear camera feed
        self.status_label.config(text="Posture: Waiting...", fg="black")

    def update_frame(self):
        if self.cap and self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)

                self.image_label.imgtk = imgtk
                self.image_label.configure(image=imgtk)

                # Simulated posture check
                posture = "Good"  # ← Replace with AI detection later
                self.history.append(posture)

                color = "green" if posture == "Good" else "red"
                self.status_label.config(text=f"Posture: {posture}", fg=color)

            self.image_label.after(10, self.update_frame)

    def show_tips(self):
        messagebox.showinfo("Posture Tips",
            "✅ Sit upright\n✅ Keep your screen at eye level\n✅ Align shoulders over hips\n✅ Avoid leaning forward")

    def show_history(self):
        if not self.history:
            messagebox.showinfo("Posture History", "No history yet.")
        else:
            history_str = "\n".join(self.history[-10:])  # Last 10 results
            messagebox.showinfo("Posture History", f"Recent Posture:\n{history_str}")

    def on_close(self):
        self.stop_camera()
        self.root.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PostureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
