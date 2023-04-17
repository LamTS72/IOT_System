from tkinter import ttk
from tkinter.ttk import *
import tkinter as tk
import sys
import io

window = tk.Tk()
window.title("IOT SYSTEM")
window.geometry("800x600")

class TextRedirector(io.TextIOBase):
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, s):
        self.textbox.insert(tk.END, s)
        self.textbox.see(tk.END)

def hello_system():
    print("hello")

lbl_title = tk.Label(window, text="WELCOME TO IOT SYSTEM", fg="blue", font=("Arial", 20))
lbl_title.place(x=200, y=10)

lbl1 = tk.Label(window, text="Period Send Data",fg="blue", font=("Arial", 8))
lbl1.place(x=10, y=70)

lbl2 = tk.Label(window, text="Period Publish Data",fg="blue", font=("Arial", 8))
lbl2.place(x=10, y=140)

combo = ttk.Combobox(window, width=8, font=("Arial", 8))
combo['value'] = ("1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s")
combo.place(x=120, y=70)

combo1 = ttk.Combobox(window, width=8, font=("Arial", 8))
combo1['value'] = ("1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s")
combo1.place(x=120, y=140)

btn = tk.Button(window, text="Apply", width=8, fg='blue', bg='yellow', command=hello_system)
btn.place(x=200, y=68)

btn1 = tk.Button(window, text="Apply", width=8,  fg='blue', bg='yellow', command=run_MQTT)
btn1.place(x=200, y=137)

textbox = tk.Text(window, height=20, width=96)
textbox.place(x=14, y=200)


sys.stdout = TextRedirector(textbox)
sys.stderr = TextRedirector(textbox)
print("Hello")
window.mainloop()


