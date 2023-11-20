import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from main import process_image

class ImageTimestampApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Smart Parking System")
        self.image1 = None
        self.image2 = None
        self.file_path1 = None
        self.file_path2 = None
        self.timestamp1 = None
        self.timestamp2 = None

        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Image Timestamps", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Buttons for uploading images
        self.upload_button1 = tk.Button(self.root, text="Entry Gate", command=self.upload_image1)
        self.upload_button1.pack(pady=(10, 0), padx=10)

        self.upload_button2 = tk.Button(self.root, text="Exit Gate", command=self.upload_image2)
        self.upload_button2.pack(pady=(10, 0), padx=10)

    def center_window(self):
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def upload_image1(self):
        self.file_path1 = filedialog.askopenfilename()
        if self.file_path1:
            self.image1 = Image.open(self.file_path1)
            self.timestamp1 = datetime.now()
            self.display_image_with_timestamp(self.image1, self.timestamp1.strftime("%Y-%m-%d %H:%M:%S"))

    def upload_image2(self):
        self.file_path2 = filedialog.askopenfilename()
        if self.file_path2:
            self.image2 = Image.open(self.file_path2)
            self.timestamp2 = datetime.now()
            self.display_image_with_timestamp(self.image2, self.timestamp2.strftime("%Y-%m-%d %H:%M:%S"))
            self.show_alert()

    def display_image_with_timestamp(self, img, timestamp):
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)

        # Display image
        image_label = tk.Label(self.root, image=img)
        image_label.image = img
        image_label.pack(pady=10)

        # Display timestamp
        timestamp_label = tk.Label(self.root, text=f"Timestamp: {timestamp}", font=("Arial", 12))
        timestamp_label.pack(pady=5)

    def show_alert(self):
        recognised_text_1 = process_image(self.file_path1)
        recognised_text_2 = process_image(self.file_path2)
        if recognised_text_1 is not None and recognised_text_2 is not None:
            if recognised_text_1._eq_(recognised_text_2):
                difference = self.timestamp2 - self.timestamp1
                total_seconds = difference.total_seconds()
                messagebox.showinfo("SUCCESS",
                                    "The recognised licence plate number is - " + recognised_text_1 + ". Proceed to pay $" + str(total_seconds * 10))
            else:
                messagebox.showerror("ERROR",
                                     "The recognised licence plate numbers are - " + recognised_text_1 + " and "
                                     + recognised_text_2 + " which are not identical.")
        else:
            messagebox.showerror("ERROR",
                                 "Unable to recognize the characters on licence plates!")

if _name_ == "_main_":
    root = tk.Tk()
    app = ImageTimestampApp(root)
    root.mainloop()
