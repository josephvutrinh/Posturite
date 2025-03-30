import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import cv2
from posture_detector import PostureDetector

class PosturiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posturite")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.detector = PostureDetector()  # Posture detection module

        # Load and resize background
        self.bg_image = Image.open("Hoohacks-7.jpg").resize((1000, 700))
        self.bg_blurred = self.bg_image.filter(ImageFilter.GaussianBlur(8))  # Apply blur effect
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_blurred_photo = ImageTk.PhotoImage(self.bg_blurred)

        # Canvas
        self.canvas = tk.Canvas(self, width=1000, height=700, highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        self.canvas.pack()

        # Title
        self.title_text = self.canvas.create_text(40, 35, text="Posturite", fill="white",
                                                  font=("Helvetica", 20, "bold"), anchor="w")

        # Start button
        self.start_button_shape = self.create_rounded_rect(400, 200, 600, 240, radius=20, fill="#c0392b", outline="")
        self.start_button_text = self.canvas.create_text(500, 220, text="Start Session", fill="white",
                                                         font=("Helvetica", 12, "bold"), anchor="center")

        self.canvas.tag_bind(self.start_button_shape, "<Button-1>", lambda e: self.start_session())
        self.canvas.tag_bind(self.start_button_text, "<Button-1>", lambda e: self.start_session())

        # End Button
        self.end_button_shape = self.create_rounded_rect(400, 500, 600, 540, radius=20, fill="#c0392b", outline="")
        self.end_button_text = self.canvas.create_text(500, 520, text="End Session", fill="white",
                                                       font=("Helvetica", 12, "bold"), anchor="center")

        self.canvas.tag_bind(self.end_button_shape, "<Button-1>", lambda e: self.end_session())
        self.canvas.tag_bind(self.end_button_text, "<Button-1>", lambda e: self.end_session())

        # Hides the end session button initially
        self.canvas.itemconfig(self.end_button_shape, state="hidden")
        self.canvas.itemconfig(self.end_button_text, state="hidden")

        # Camera feed (Canvas Image)
        self.video_image_id = None  # Assigned later

        # Warning Label (For posture detection alerts)
        self.warning_label = tk.Label(self, text="", font=("Helvetica", 24, "bold"), fg="white", bg="black")
        self.warning_label.place(relx=0.5, y=90, anchor="center")
        self.warning_label.place_forget()  # Hide initially

        # Camera control
        self.cap = None
        self.running = False

    def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        """ Creates a rounded rectangle shape on the canvas """
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

    def start_session(self):
        """ Start the posture detection session """
        # Hide start button
        self.canvas.itemconfig(self.start_button_shape, state="hidden")
        self.canvas.itemconfig(self.start_button_text, state="hidden")

        # Blur background
        self.canvas.itemconfig(self.canvas_bg, image=self.bg_blurred_photo)

        # Show End Session button
        self.canvas.itemconfig(self.end_button_shape, state="normal")
        self.canvas.itemconfig(self.end_button_text, state="normal")

        # Start camera
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.show_frame()

    def show_frame(self):
        """ Capture and display video frames with posture detection and rounded corners """
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Flip for mirror effect

                # Apply Posture Detection
                frame = self.detector.findPose(frame)  # Draw pose landmarks
                lmList = self.detector.findPosition(frame)  # Get positions

                # Detect Forward Head Posture
                if self.detector.detectForwardHead(lmList):
                    warning_text = "⚠️ Forward Head Detected!"
                    self.warning_label.config(text=warning_text, fg="red")
                    self.warning_label.place(relx=0.5, y=90, anchor="center")
                else:
                    self.warning_label.config(text="Good Posture", fg="green")
                    self.warning_label.place(relx=0.5, y=90, anchor="center")

                self.warning_label.update_idletasks()

                # Convert frame for display
                frame = cv2.resize(frame, (700, 400))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)

                # Apply rounded corners
                rounded = self.add_rounded_corners(img, radius=25)

                imgtk = ImageTk.PhotoImage(image=rounded)

                if self.video_image_id:
                    self.canvas.itemconfig(self.video_image_id, image=imgtk)
                else:
                    self.video_image_id = self.canvas.create_image(500, 250, image=imgtk)

                self.video_frame_imgtk = imgtk  # Store reference to prevent garbage collection

            self.after(10, self.show_frame)  # Refresh frame every 10ms

    def end_session(self):
        """ End the session and reset UI """
        self.running = False
        if self.cap:
            self.cap.release()

        # Remove camera feed
        self.canvas.delete(self.video_image_id)
        self.video_image_id = None

        # Restore normal background
        self.canvas.itemconfig(self.canvas_bg, image=self.bg_photo)

        # Hide End Session button, show Start button
        self.canvas.itemconfig(self.end_button_shape, state="hidden")
        self.canvas.itemconfig(self.end_button_text, state="hidden")
        self.canvas.itemconfig(self.start_button_shape, state="normal")
        self.canvas.itemconfig(self.start_button_text, state="normal")

        # Hide warning label
        self.warning_label.config(text="")
        self.warning_label.place_forget()

    def add_rounded_corners(self, img, radius):
        """ Apply rounded corners to the camera feed """
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)

        img = img.convert("RGBA")
        img.putalpha(mask)

        # Create a solid background matching UI theme
        bg = Image.new("RGBA", img.size, (30, 30, 30, 255))
        rounded = Image.composite(img, bg, mask)

        return rounded.convert("RGB")  # Remove transparency for Tkinter compatibility

if __name__ == "__main__":
    app = PosturiteApp()
    app.mainloop()