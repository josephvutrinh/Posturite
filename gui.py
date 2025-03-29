import tkinter as tk

class PosturiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Posturite - Posture Detection")
        self.root.geometry("500x300")

        self.label = tk.Label(root, text="Welcome to Posturite!", font=("Arial", 14))
        self.label.pack(pady=20)

        self.status_label = tk.Label(root, text="Posture Status: Good", font=("Arial", 12), fg="green")
        self.status_label.pack(pady=10)

        self.check_button = tk.Button(root, text="Check Posture", command=self.check_posture)
        self.check_button.pack(pady=10)

    def check_posture(self):
        # Placeholder function, will integrate posture detection later
        self.status_label.config(text="Posture Status: Bad", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PosturiteApp(root)
    root.mainloop()