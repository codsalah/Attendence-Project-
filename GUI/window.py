from tkinter import *
import tkinter as tk
from tkinter import ttk
from customtkinter import *
from tkinter import messagebox
import cv2
import os
from PIL import Image, ImageTk
import openpyxl

def on_enter(e):
    e.widget['background'] = '#84756B'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

def create_window1():
    window = tk.Toplevel()
   
    window.title("Login Form")
    # window.geometry("800x600")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d" % (w, h))
    window.configure(bg="#F2E9EA")
    frame = tk.Frame(window, bg="#F2E9EA")
    frame.pack()
    # Create and start the SelfieApp
    with SelfieApp(window, "tend.jpg.") as selfie_app:
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
        path = "attendance.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)
        cols = list_values[0]
        tree = ttk.Treeview(frame, column=cols, show="headings")
        tree.tag_configure("font", font=("Fixedsys", 14))
        for col_name in cols:
            tree.heading(col_name, text=col_name)
        tree.pack(expand=True, fill='y')

        for value_tuple in list_values[1:]:
            tree.insert('', tk.END, values=value_tuple, tags=("font",))

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
        

        # Set background image
        self.set_background(bg_image_path)

        # Open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Unable to open the camera. Exiting.")
            self.main_window.destroy()
            return

        # Create a canvas to display the image
        self.canvas = tk.Canvas(window, width=640, height=480,highlightthickness=0)
        self.canvas.pack(pady=0)

        # Create buttons
        font2 = CTkFont(size=32,weight="bold",slant='roman')
        self.btn_capture = CTkButton(master=window, text="Selfie", text_color="#206D77", font=font2, bg_color="#F2E9EA", corner_radius=50, hover_color="#206D77", fg_color="#F2E9EA", command=self.capture_selfie)
        self.btn_capture.pack(pady=10, side='top')
        self.img = None
        
        self.btn_delete = CTkButton(master=window, text="Delete", text_color="#206D77", font=font2, corner_radius=50, hover_color="#206D77", fg_color="#F2E9EA", command=self.delete_canvas, state='disabled')
        self.btn_delete.pack(pady=10)

        # Start updating the display
        self.update()
        

    def set_background(self, image_path):
        # Load the image
        bg_image= Image.open("tend.jpg") # Replace with your image file path
        bg_image= ImageTk.PhotoImage(bg_image)
        
        #to resize the img
      # Open the image and resize it
        original_image = Image.open(image_path)
        resized_image = original_image.resize((1500, 750))
      # Convert the resized image to a PhotoImage
        bg_image = ImageTk.PhotoImage(resized_image)
      # Create a label to display the background image
        bg_label = tk.Label(self.window,image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
      # Ensure that the label persists
        bg_label.image = bg_image
        
        # Create a login label
        login_label = tk.Label(self.window, text="JOIN CLASS", fg="#206D77", bg="#F2E9EA", font='times 50 bold roman')
        login_label.pack(pady=20)

        # Create username labels and entry
        username_label = tk.Label(self.window, text="Username:", bg="#F2E9EA", fg="#206D77", font='times 25 bold roman')
        username_label.pack(pady=0)
        self.username_entry = tk.Entry(self.window, width=23, font=40, fg="#206D77")
        self.username_entry.pack(pady=5)

    def capture_selfie(self):
        # Capture and convert the frame
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Unable to capture selfie.")
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(frame_rgb)
        self.photo = ImageTk.PhotoImage(self.img)
        self.username = self.username_entry.get()
        path = f'Attendance/{self.username}.jpg'
        self.img.save(path)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.image = self.photo

        # Enable the delete button
        self.btn_delete.configure(state='normal')
        self.update()
     

    def delete_canvas(self):
        # Remove the saved image and clear the canvas
        if os.path.exists(f'Attendance/{self.username}.jpg'):
         os.remove(f'Attendance/{self.username}.jpg')
         self.canvas.delete('all')

        # Reset captured image and update canvas with live feed
         self.img = None
         self.update()
         self.btn_delete.configure(state='disabled')
         messagebox.showinfo("Success", "Image deleted successfully!")
        else:
         messagebox.showwarning("Warning", "No image currently captured to delete.")

        

    def update(self):
        # Read the camera frame and convert it
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Error", "Unable to read camera frame.")
            self.window.destroy()
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        self.photo = ImageTk.PhotoImage(img)

        # Display the live feed or captured image based on availability
        if self.img is not None:
           self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo(self.img))
           self.canvas.image = self.photo
        else:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.image = self.photo
            self.btn_capture.configure(state='normal')
        # Schedule the next update
        self.window.after(10, self.update)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
         #Release the camera when the application is closed
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

background_img = PhotoImage(file = "background.png")
background = canvas.create_image(
    421.0, 262.0,
    image=background_img)

img0 = PhotoImage(file = "img0.png")
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

img1 = PhotoImage(file = "img1.png")
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

