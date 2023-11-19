import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from main import process_image


class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Parking System")
        self.image1 = None
        self.image2 = None
        self.file_path1 = None
        self.file_path2 = None

        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Smart Parking System", font=("Arial", 20))
        self.title_label.pack(pady=20)

        self.frame_left = tk.Frame(self.root, width=200, height=200)
        self.frame_left.pack_propagate(False)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_right = tk.Frame(self.root, width=200, height=200)
        self.frame_right.pack_propagate(False)
        self.frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

        self.upload_button1 = tk.Button(self.frame_left, text="Entry Gate", command=self.upload_image1)
        self.upload_button1.pack(pady=(10, 0), padx=10)

        self.upload_button2 = tk.Button(self.frame_right, text="Exit Gate", command=self.upload_image2)
        self.upload_button2.pack(pady=(10, 0), padx=10)

        self.image_label1 = tk.Label(self.root)
        self.image_label1.pack(fill=tk.BOTH, expand=True)

        self.image_label2 = tk.Label(self.root)
        self.image_label2.pack(fill=tk.BOTH, expand=True)

        self.frame_bottom = tk.Frame(self.root)
        self.frame_bottom.pack(pady=10)

        self.match_result_button = tk.Button(self.frame_bottom, text="Match Result", command=self.show_alert)
        self.match_result_button.pack()
        self.match_result_button['state'] = 'disabled'

    def check_images_uploaded(self):
        if self.image1 and self.image2:
            self.match_result_button['state'] = 'normal'  # Enable the button
        else:
            self.match_result_button['state'] = 'disabled'  # Keep the button disabled

    def center_window(self):
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def upload_image1(self):
        self.file_path1 = filedialog.askopenfilename()
        if self.file_path1:
            self.image1 = Image.open(self.file_path1)
            self.show_image_in_label(self.image1, self.image_label1)
            self.check_images_uploaded()

    def upload_image2(self):
        self.file_path2 = filedialog.askopenfilename()
        if self.file_path2:
            self.image2 = Image.open(self.file_path2)
            self.show_image_in_label(self.image2, self.image_label2)
            self.check_images_uploaded()

    def show_image_in_label(self, img, label_widget):
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)
        label_widget.config(image=img)
        label_widget.image = img

    def show_alert(self):
        recognised_text_1 = process_image(self.file_path1)
        recognised_text_2 = process_image(self.file_path2)
        if recognised_text_1 is not None and recognised_text_2 is not None:
            if recognised_text_1.__eq__(recognised_text_2):
                messagebox.showinfo("SUCCESS",
                                    "The recognised licence plate number is - " + recognised_text_1)
            else:
                messagebox.showerror("ERROR",
                                     "The recognised licence plate numbers are - " + recognised_text_1 + " and "
                                     + recognised_text_2 + " which are not identical.")
        else:
            messagebox.showerror("ERROR",
                                 "Unable to recognize the characters on licence plates!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()
