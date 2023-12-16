from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from customtkinter import *
from tkinter import messagebox
import cv2
import os
from PIL import Image, ImageTk
import openpyxl


def btn_clicked():
    print("Button Clicked")

def on_enter(e):
    e.widget['background'] = '#84756B'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'




def create_window1():
    window = tk.Toplevel()
    #window = tk.Tk()
    window.title("Login Form")
    # window.geometry("800x600")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d" % (w, h))
    window.configure(bg="#F2E9EA")
    frame = tk.Frame(window, bg="#F2E9EA")
    # window.attributes('-full screen', True)
    frame.pack()
    # Create and start the SelfieApp
    with SelfieApp(window, "D:\\download\\projectfinal\\tend.jpg") as selfie_app:
        window.mainloop()
        print(selfie_app.username)



def create_window2():
    window2 = tk.Toplevel()
    window2.title("Class Attendance")
    window2.geometry("842x524")
    font2 = CTkFont(size=30, weight="bold", slant='italic')
    label = Label(window2, text='Class of Today', font=font2, justify=tk.LEFT, bg="#F2E9EA")

    label.pack(pady=20)

    def load_data():
        path = "D:\\download\\projectfinal\\attendance.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)
        cols = list_values[0]
        tree = ttk.Treeview(frame, column=cols, show="headings")
        for col_name in cols:
            tree.heading(col_name, text=col_name)
        tree.pack(expand=True, fill='y')

        for value_tuple in list_values[1:]:
            tree.insert('', tk.END, values=value_tuple)

    frame =Frame(window2)
    frame.pack(pady=30)
    #tree = ttk.Treeview(frame)
    load_data()

    window2.configure(bg="#F2E9EA")
    window2.pack(pady= 100)


    window2.mainloop()


class SelfieApp:
    def __init__(self, window, bg_image_path):
        self.window = window
        self.window.title("Selfie App")

        # set background Image
        self.set_background(bg_image_path)

        # open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            tk.messagebox.showerror("Error", "Unable to open the camera. Exiting.")
            self.window.destroy()
            return

        # Create a canvas to display the selfie
        self.canvas = tk.Canvas(window, width=550, height=440, highlightthickness=0)
        self.canvas.pack(pady=1)

        font2 = CTkFont(size=30, weight="bold", slant='italic')
        # Button to capture selfie
        self.btn_capture = CTkButton(master=window, text="Capture Selfie", text_color="#5B3256", font=font2,
                                     bg_color="#8793A1", corner_radius=50, hover_color="#563C5C", fg_color="#F2E9EA",
                                     command=self.capture_selfie)
        self.btn_capture.pack(pady=0, side="top")

        self.img = None

        # Button to close application
        self.btn_quit = CTkButton(master=window, text="Submit", text_color="#5B3256", font=font2, corner_radius=50,
                                  hover_color="#563C5C", fg_color="#F2E9EA", command=self.window.destroy)
        self.btn_quit.pack(side="right", pady=20, padx=40)

        # button to remove image
        self.btn_delete = CTkButton(master=window, text="Delete", text_color="#5B3256", font=font2, corner_radius=50,
                                    hover_color="#563C5C", fg_color="#F2E9EA", command=self.delete_canvas)
        self.btn_delete.pack(padx=15, side="right")

        # Start updating the display
        self.update()

    def set_background(self, image_path):
        # Load the image
        bg_image = Image.open("D:\\download\\projectfinal\\tend.jpg")  # Replace with your image file path
        bg_image = ImageTk.PhotoImage(bg_image)

        # to resize the img
        # Open the image and resize it
        original_image = Image.open(image_path)
        resized_image = original_image.resize((1500, 750))
        # Convert the resized image to a PhotoImage
        bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label to display the background image
        bg_label = tk.Label(self.window, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Ensure that the label persists
        bg_label.image = bg_image

        # Create a login label
        login_label = tk.Label(self.window, text="JOIN ClASS", fg="#5B3256", bg="#F2E9EA", font='times 50 bold italic')
        login_label.pack(pady=20)

        # create a username label
        username_label = tk.Label(self.window, text="Username:", bg="#F2E9EA", fg="#5B3256",
                                  font='times 25 bold italic')
        username_label.pack(pady=0)

        # craete a entry label
        self.username_entry = tk.Entry(self.window, width=23, font=30, fg="#5B3256")
        self.username_entry.pack(pady=5)

        # Ensure that the labels persist
        login_label.image = bg_image
        username_label.image = bg_image
        self.username_entry.image = bg_image

    def capture_selfie(self):
        ret, frame = self.cap.read()

        # Check if the frame is valid
        if not ret:
            tk.messagebox.showerror("Error", "Unable to capture selfie.")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(frame_rgb)
        # Save the captured selfie
        self.photo = ImageTk.PhotoImage(image=self.img)
        self.username = self.username_entry.get()

        # # Update the canvas with the captured selfie
        # self.canvas.create_image(0, 0, anchor=tk.NW , image=self.photo)
        # self.canvas.create_image = self.photo

        self.submit_selfie()

    def submit_selfie(self):
        if self.img is not None:
            path = 'D:/download/projectfinal'
            self.photo = os.path.join(path, f"{self.username}.jpg")
            self.img.save(self.photo)
            os.startfile(self.photo)

        #     tk.messagebox.showinfo("Success", "Selfie submitted successfully!")
        # else:
        #    tk.messagebox.showwarning("Warning", "Please capture a selfie first.")
        #

    def delete_canvas(self):
        os.remove(self.photo)
        self.canvas.delete('all')
        self.photo = None
        tk.messagebox.showinfo(message="'Selfie has been deleted successfully!'")

        # self.update()

    def update(self):
        ret, frame = self.cap.read()

        # Check if the frame is valid
        if not ret:
            tk.messagebox.showerror("Error", "Unable to read camera frame.")
            self.window.destroy()
            return
        frame = cv2.resize(frame, (550, 440))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the canvas with the latest frame
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        self.canvas.image = imgtk

        # Repeat the update after 1 millisecond
        self.window.after(1, self.update)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Release the camera when the application is closed
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()




#main first window
window1=Tk()

window1.geometry("842x524")
window1.configure(bg = "#edf6f9")
canvas = Canvas(
    window1,
    bg = "#edf6f9",
    height = 524,
    width = 842,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    421.0, 262.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = create_window2,
    relief = "flat")

b0.place(
    x = 78, y = 363,
    width = 251,
    height = 53)

b0.bind("<Enter>", on_enter)
b0.bind("<Leave>", on_leave)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = create_window1,
    relief = "flat")

b1.place(
    x = 78, y = 274,
    width = 251,
    height = 53)

b1.bind("<Enter>", on_enter)
b1.bind("<Leave>", on_leave)

window1.resizable(False, False)
window1.mainloop()
