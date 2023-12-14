from tkinter import *
import os

def btn_clicked():
    print("Registring New Student")
    os.system('E:/ImageProcessing/GUI.py')
def on_enter(e):
    e.widget['background'] = '#84756B'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

def dispaly_Attendance():
    print("لسه معملتهاش")
    # with open('E:/FaceRecognitionProject/attendance.csv') as File:
    #     Line_reader = csv.reader(File)

window = Tk()

window.geometry("842x524")
window.configure(bg = "#edf6f9")
canvas = Canvas(
    window,
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
    command = dispaly_Attendance,
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
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 78, y = 274,
    width = 251,
    height = 53)

b1.bind("<Enter>", on_enter)
b1.bind("<Leave>", on_leave)

window.resizable(False, False)
window.mainloop()
